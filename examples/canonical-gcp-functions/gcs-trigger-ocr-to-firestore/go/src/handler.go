package handler

import (
	"context"
	"encoding/json"
	"fmt"
	"time"
)

type GcsObjectEvent struct {
	ID         string `json:"id"`
	Bucket     string `json:"bucket"`
	Name       string `json:"name"`
	Generation string `json:"generation"`
}

type Clients interface {
	ClaimGeneration(ctx context.Context, key string) (bool, error)
	RunOCR(ctx context.Context, bucket, name, generation string) (string, error)
	WriteMetadata(ctx context.Context, key string, payload map[string]string) error
	PublishDownstream(ctx context.Context, payload map[string]string) error
}

type Result struct {
	Duplicate bool
	Text      string
	Decision  string
}

func Handle(ctx context.Context, event GcsObjectEvent, clients Clients) (Result, error) {
	started := time.Now()
	generation := event.Generation
	if generation == "" {
		generation = "0"
	}
	eventID := event.ID
	if eventID == "" {
		eventID = event.Bucket + "/" + event.Name + "/" + generation
	}
	dedupeKey := event.Bucket + ":" + event.Name + ":" + generation
	claimed, err := clients.ClaimGeneration(ctx, dedupeKey)
	if err != nil {
		return Result{}, err
	}
	if !claimed {
		logShape(started, eventID, dedupeKey, "DROP", "duplicate object generation")
		return Result{Duplicate: true, Decision: "DROP"}, nil
	}
	text, err := clients.RunOCR(ctx, event.Bucket, event.Name, generation)
	if err != nil {
		return Result{}, err
	}
	payload := map[string]string{"bucket": event.Bucket, "name": event.Name, "generation": generation, "text": text, "status": "OCR_COMPLETE"}
	if err := clients.WriteMetadata(ctx, dedupeKey, payload); err != nil {
		return Result{}, err
	}
	if err := clients.PublishDownstream(ctx, payload); err != nil {
		return Result{}, err
	}
	logShape(started, eventID, dedupeKey, "ALLOW", "ocr metadata written")
	return Result{Text: text, Decision: "ALLOW"}, nil
}

func logShape(started time.Time, correlationID, dedupeKey, decision, msg string) {
	entry := map[string]any{"timestamp": time.Now().UTC().Format(time.RFC3339), "severity": "INFO", "msg": msg, "trace_id": "local-trace", "request_id": correlationID, "correlation_id": correlationID, "provider": "gcp", "runtime_tier": "function", "function_name": "accb-dev-gcp-gcs-ocr-go", "dedupe_key": dedupeKey, "decision": decision, "latency_ms": time.Since(started).Milliseconds()}
	payload, _ := json.Marshal(entry)
	fmt.Println(string(payload))
}
