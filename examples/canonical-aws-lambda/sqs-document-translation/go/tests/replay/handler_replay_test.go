package replay

import (
	"context"
	"encoding/json"
	"testing"

	handler "accb-sqs-document-translation/src"
)

type fakeClients struct {
	claimed   map[string]bool
	artifacts map[string]string
}

func (f *fakeClients) Claim(ctx context.Context, key string) (bool, error) {
	if f.claimed[key] {
		return false, nil
	}
	f.claimed[key] = true
	return true, nil
}

func (f *fakeClients) GetObject(ctx context.Context, bucket, key string) (string, error) { return "hello", nil }
func (f *fakeClients) Translate(ctx context.Context, text, sourceLang, targetLang string) (string, error) {
	return "hola", nil
}
func (f *fakeClients) PutObject(ctx context.Context, bucket, key, body string) error {
	f.artifacts[bucket+"/"+key] = body
	return nil
}
func (f *fakeClients) Complete(ctx context.Context, key, status string) error { return nil }

func TestReplayCreatesOneArtifact(t *testing.T) {
	body, _ := json.Marshal(handler.Job{SourceBucket: "source", SourceKey: "a.txt", DestBucket: "dest", DestKey: "a.es.txt", SourceLang: "en", TargetLang: "es"})
	clients := &fakeClients{claimed: map[string]bool{}, artifacts: map[string]string{}}
	event := handler.Event{Records: []handler.Message{{MessageID: "msg-replay", Body: string(body)}}}
	first, err := handler.Handle(context.Background(), event, clients)
	if err != nil {
		t.Fatal(err)
	}
	second, err := handler.Handle(context.Background(), event, clients)
	if err != nil {
		t.Fatal(err)
	}
	if first.Processed != 1 || second.Duplicates != 1 || len(clients.artifacts) != 1 {
		t.Fatalf("replay was not idempotent: %#v %#v %#v", first, second, clients.artifacts)
	}
}
