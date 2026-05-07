package replay

import (
	"context"
	"testing"

	handler "accb-s3-trigger-image-moderation/src"
)

type clients struct {
	claimed map[string]bool
	flagged int
}

func (c *clients) ClaimObjectVersion(ctx context.Context, key string) (bool, error) {
	if c.claimed[key] {
		return false, nil
	}
	c.claimed[key] = true
	return true, nil
}
func (c *clients) DetectLabels(ctx context.Context, bucket, key string) ([]string, error) {
	return []string{"Document"}, nil
}
func (c *clients) DetectModerationLabels(ctx context.Context, bucket, key string) ([]string, error) {
	return []string{"Explicit Nudity"}, nil
}
func (c *clients) RecordDecision(ctx context.Context, key, decision string, labels []string) error {
	return nil
}
func (c *clients) PublishFlagged(ctx context.Context, detail map[string]string) error {
	c.flagged++
	return nil
}

func TestSameObjectVersionHasOneSideEffect(t *testing.T) {
	c := &clients{claimed: map[string]bool{}}
	evt := event("v1")
	first, err := handler.Handle(context.Background(), evt, c)
	if err != nil {
		t.Fatal(err)
	}
	second, err := handler.Handle(context.Background(), evt, c)
	if err != nil {
		t.Fatal(err)
	}
	if first.Processed != 1 || second.Duplicates != 1 || c.flagged != 1 || len(c.claimed) != 1 {
		t.Fatalf("unexpected replay result: first=%+v second=%+v flagged=%d", first, second, c.flagged)
	}
}

func event(version string) handler.Event {
	var evt handler.Event
	record := handler.Record{}
	record.S3.Bucket.Name = "images"
	record.S3.Object.Key = "a.jpg"
	record.S3.Object.VersionID = version
	evt.Records = []handler.Record{record}
	return evt
}
