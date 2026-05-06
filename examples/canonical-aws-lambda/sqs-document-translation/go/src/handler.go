package handler

import (
	"context"
	"encoding/json"
	"fmt"
	"time"
)

type Message struct {
	MessageID string
	Body      string
}

type Event struct {
	Records []Message
}

type Job struct {
	SourceBucket string `json:"source_bucket"`
	SourceKey    string `json:"source_key"`
	DestBucket   string `json:"dest_bucket"`
	DestKey      string `json:"dest_key"`
	SourceLang   string `json:"source_lang"`
	TargetLang   string `json:"target_lang"`
}

type Clients interface {
	Claim(ctx context.Context, key string) (bool, error)
	GetObject(ctx context.Context, bucket, key string) (string, error)
	Translate(ctx context.Context, text, sourceLang, targetLang string) (string, error)
	PutObject(ctx context.Context, bucket, key, body string) error
	Complete(ctx context.Context, key, status string) error
}

type Result struct {
	Processed  int
	Duplicates int
}

func Handle(ctx context.Context, event Event, clients Clients) (Result, error) {
	started := time.Now()
	result := Result{}
	for _, record := range event.Records {
		if deadline, ok := ctx.Deadline(); ok && time.Until(deadline) < 5*time.Second {
			return result, fmt.Errorf("visibility-timeout guard: insufficient time remains")
		}
		var job Job
		if err := json.Unmarshal([]byte(record.Body), &job); err != nil {
			return result, err
		}
		claimed, err := clients.Claim(ctx, record.MessageID)
		if err != nil {
			return result, err
		}
		if !claimed {
			result.Duplicates++
			logShape(started, record.MessageID, "DROP", "duplicate message")
			continue
		}
		source, err := clients.GetObject(ctx, job.SourceBucket, job.SourceKey)
		if err != nil {
			return result, err
		}
		translated, err := clients.Translate(ctx, source, job.SourceLang, job.TargetLang)
		if err != nil {
			return result, err
		}
		if err := clients.PutObject(ctx, job.DestBucket, job.DestKey, translated); err != nil {
			return result, err
		}
		if err := clients.Complete(ctx, record.MessageID, "COMPLETED"); err != nil {
			return result, err
		}
		result.Processed++
		logShape(started, record.MessageID, "ALLOW", "translation complete")
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
		"function_name": "accb-dev-translate-handler",
		"dedupe_key":    dedupeKey,
		"decision":      decision,
		"latency_ms":    time.Since(started).Milliseconds(),
	}
	payload, _ := json.Marshal(entry)
	fmt.Println(string(payload))
}
