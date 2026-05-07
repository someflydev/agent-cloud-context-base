package smoke

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

func TestHandlerFlagsImage(t *testing.T) {
	c := &clients{claimed: map[string]bool{}}
	result, err := handler.Handle(context.Background(), event("v1"), c)
	if err != nil {
		t.Fatal(err)
	}
	if result.Decision != "FLAG" || c.flagged != 1 || len(c.claimed) != 1 {
		t.Fatalf("unexpected result: %+v flagged=%d claimed=%d", result, c.flagged, len(c.claimed))
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
