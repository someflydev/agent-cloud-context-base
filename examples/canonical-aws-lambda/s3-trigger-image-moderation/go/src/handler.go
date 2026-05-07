package handler

import (
	"context"
	"encoding/json"
	"fmt"
	"time"
)

type Event struct {
	Records []Record
}

type Record struct {
	S3 struct {
		Bucket struct {
			Name string
		}
		Object struct {
			Key       string
			VersionID string
			Sequencer string
		}
	}
}

type Clients interface {
	ClaimObjectVersion(ctx context.Context, key string) (bool, error)
	DetectLabels(ctx context.Context, bucket, key string) ([]string, error)
	DetectModerationLabels(ctx context.Context, bucket, key string) ([]string, error)
	RecordDecision(ctx context.Context, key, decision string, labels []string) error
	PublishFlagged(ctx context.Context, detail map[string]string) error
}

type Result struct {
	Processed  int
	Duplicates int
	Decision   string
}

func Handle(ctx context.Context, event Event, clients Clients) (Result, error) {
	started := time.Now()
	result := Result{}
	for _, record := range event.Records {
		version := record.S3.Object.VersionID
		if version == "" {
			version = record.S3.Object.Sequencer
		}
		if version == "" {
			version = "unversioned"
		}
		dedupeKey := fmt.Sprintf("%s:%s:%s", record.S3.Bucket.Name, record.S3.Object.Key, version)
		claimed, err := clients.ClaimObjectVersion(ctx, dedupeKey)
		if err != nil {
			return result, err
		}
		if !claimed {
			result.Duplicates++
			logShape(started, dedupeKey, "DROP", "duplicate object version")
			continue
		}
		labels, err := clients.DetectLabels(ctx, record.S3.Bucket.Name, record.S3.Object.Key)
		if err != nil {
			return result, err
		}
		moderation, err := clients.DetectModerationLabels(ctx, record.S3.Bucket.Name, record.S3.Object.Key)
		if err != nil {
			return result, err
		}
		decision := "ALLOW"
		if len(moderation) > 0 {
			decision = "FLAG"
			if err := clients.PublishFlagged(ctx, map[string]string{"bucket": record.S3.Bucket.Name, "key": record.S3.Object.Key, "version": version, "decision": decision}); err != nil {
				return result, err
			}
		}
		if err := clients.RecordDecision(ctx, dedupeKey, decision, labels); err != nil {
			return result, err
		}
		result.Processed++
		result.Decision = decision
		logShape(started, dedupeKey, decision, "moderation complete")
	}
	return result, nil
}

func logShape(started time.Time, dedupeKey, decision, msg string) {
	entry := map[string]any{
		"timestamp":     time.Now().UTC().Format(time.RFC3339),
		"level":         "INFO",
		"msg":           msg,
		"trace_id":      "local-trace",
		"request_id":    dedupeKey,
		"correlation_id": dedupeKey,
		"provider":      "aws",
		"runtime_tier":  "function",
		"function_name": "accb-dev-s3mod-handler",
		"dedupe_key":    dedupeKey,
		"decision":      decision,
		"latency_ms":    time.Since(started).Milliseconds(),
	}
	payload, _ := json.Marshal(entry)
	fmt.Println(string(payload))
}
