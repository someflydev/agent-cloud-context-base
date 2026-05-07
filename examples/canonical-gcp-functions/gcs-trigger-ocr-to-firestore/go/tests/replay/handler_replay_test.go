package tests

import (
	"context"
	"testing"

	handler "accb.example.gcpfunctions/gcsocrfirestore/src"
)

type fakeClients struct {
	claimed   map[string]bool
	metadata  map[string]map[string]string
	published []map[string]string
}

func (f *fakeClients) ClaimGeneration(ctx context.Context, key string) (bool, error) {
	if f.claimed[key] {
		return false, nil
	}
	f.claimed[key] = true
	return true, nil
}
func (f *fakeClients) RunOCR(ctx context.Context, bucket, name, generation string) (string, error) {
	return "ocr:" + bucket + "/" + name + "@" + generation, nil
}
func (f *fakeClients) WriteMetadata(ctx context.Context, key string, payload map[string]string) error {
	f.metadata[key] = payload
	return nil
}
func (f *fakeClients) PublishDownstream(ctx context.Context, payload map[string]string) error {
	f.published = append(f.published, payload)
	return nil
}

func TestIdempotencyReplay(t *testing.T) {
	c := &fakeClients{claimed: map[string]bool{}, metadata: map[string]map[string]string{}}
	e := handler.GcsObjectEvent{ID: "evt-1", Bucket: "docs", Name: "scan.png", Generation: "7"}
	first, err := handler.Handle(context.Background(), e, c)
	if err != nil || first.Duplicate {
		t.Fatalf("first failed: %#v %v", first, err)
	}
	second, err := handler.Handle(context.Background(), e, c)
	if err != nil || !second.Duplicate {
		t.Fatalf("second should be duplicate: %#v %v", second, err)
	}
	if got := c.metadata["docs:scan.png:7"]["status"]; got != "OCR_COMPLETE" {
		t.Fatalf("metadata status = %s", got)
	}
	if len(c.published) != 1 {
		t.Fatalf("published = %d", len(c.published))
	}
}
