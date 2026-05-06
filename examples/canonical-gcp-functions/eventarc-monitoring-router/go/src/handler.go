package handler

import (
	"context"
	"encoding/json"
	"fmt"
	"time"
)

type IncidentEvent struct {
	ID      string `json:"id"`
	Service string `json:"service"`
	State   string `json:"state"`
	Summary string `json:"summary"`
}

type Clients interface {
	Claim(ctx context.Context, key string) (bool, error)
	LookupOwner(ctx context.Context, service string) (string, error)
	WriteAudit(ctx context.Context, row AuditRow) error
	SendSlack(ctx context.Context, owner string, event IncidentEvent) error
}

type AuditRow struct {
	IncidentID string
	Service    string
	Owner      string
	State      string
	At         time.Time
}

type Result struct {
	Routed    bool
	Duplicate bool
	Owner     string
}

func Handle(ctx context.Context, event IncidentEvent, clients Clients) (Result, error) {
	started := time.Now()
	dedupeKey := event.ID + ":" + event.State
	claimed, err := clients.Claim(ctx, dedupeKey)
	if err != nil {
		return Result{}, err
	}
	if !claimed {
		logShape(started, event.ID, dedupeKey, "DROP", "duplicate incident suppressed")
		return Result{Duplicate: true}, nil
	}
	owner, err := clients.LookupOwner(ctx, event.Service)
	if err != nil {
		return Result{}, err
	}
	row := AuditRow{IncidentID: event.ID, Service: event.Service, Owner: owner, State: event.State, At: time.Now().UTC()}
	if err := clients.WriteAudit(ctx, row); err != nil {
		return Result{}, err
	}
	if err := clients.SendSlack(ctx, owner, event); err != nil {
		return Result{}, err
	}
	logShape(started, event.ID, dedupeKey, "ALLOW", "incident routed")
	return Result{Routed: true, Owner: owner}, nil
}

func logShape(started time.Time, correlationID, dedupeKey, decision, msg string) {
	entry := map[string]any{
		"timestamp":     time.Now().UTC().Format(time.RFC3339),
		"severity":      "INFO",
		"msg":           msg,
		"trace_id":      "local-trace",
		"request_id":    correlationID,
		"correlation_id": correlationID,
		"provider":      "gcp",
		"runtime_tier":  "function",
		"function_name": "accb-dev-gcp-monitoring-router",
		"dedupe_key":    dedupeKey,
		"decision":      decision,
		"latency_ms":    time.Since(started).Milliseconds(),
	}
	payload, _ := json.Marshal(entry)
	fmt.Println(string(payload))
}
