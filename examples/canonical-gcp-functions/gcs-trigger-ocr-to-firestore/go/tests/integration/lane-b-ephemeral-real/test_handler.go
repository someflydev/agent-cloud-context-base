package main

import (
	"context"
	"fmt"

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
	return fmt.Sprintf("ocr:%s/%s@%s", bucket, name, generation), nil
}

func (f *fakeClients) WriteMetadata(ctx context.Context, key string, payload map[string]string) error {
	f.metadata[key] = payload
	return nil
}

func (f *fakeClients) PublishDownstream(ctx context.Context, payload map[string]string) error {
	f.published = append(f.published, payload)
	return nil
}

func main() {
	clients := &fakeClients{claimed: map[string]bool{}, metadata: map[string]map[string]string{}}
	result, err := handler.Handle(context.Background(), handler.GcsObjectEvent{
		ID:         "evt-lane-b",
		Bucket:     "docs",
		Name:       "scan.png",
		Generation: "9",
	}, clients)
	if err != nil {
		panic(err)
	}
	if result.Duplicate || len(clients.published) != 1 || clients.metadata["docs:scan.png:9"]["status"] != "OCR_COMPLETE" {
		panic("unexpected lane-b GCS OCR effect")
	}
	fmt.Println("lane-b GCS OCR handler invocation passed")
}
