package main

import (
	"context"

	handler "accb-s3-trigger-image-moderation/src"
)

type noopClients struct{}

func (noopClients) Claim(ctx context.Context, key string) (bool, error) { return true, nil }
func (noopClients) GetObject(ctx context.Context, bucket, key string) (string, error) {
	return "", nil
}
func (noopClients) Translate(ctx context.Context, text, sourceLang, targetLang string) (string, error) {
	return text, nil
}
func (noopClients) PutObject(ctx context.Context, bucket, key, body string) error { return nil }
func (noopClients) Complete(ctx context.Context, key, status string) error { return nil }

func main() {
	_, _ = handler.Handle(context.Background(), handler.Event{}, noopClients{})
}
