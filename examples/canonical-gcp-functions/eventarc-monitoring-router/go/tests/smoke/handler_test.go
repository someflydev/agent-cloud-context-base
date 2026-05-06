package smoke

import (
	"context"
	"testing"

	handler "accb.example.gcpfunctions/eventarcmonitoringrouter/src"
)

type clients struct {
	claimed map[string]bool
	audits  []handler.AuditRow
	slack   int
}

func (c *clients) Claim(ctx context.Context, key string) (bool, error) {
	if c.claimed[key] {
		return false, nil
	}
	c.claimed[key] = true
	return true, nil
}

func (c *clients) LookupOwner(ctx context.Context, service string) (string, error) {
	return "payments-oncall", nil
}

func (c *clients) WriteAudit(ctx context.Context, row handler.AuditRow) error {
	c.audits = append(c.audits, row)
	return nil
}

func (c *clients) SendSlack(ctx context.Context, owner string, event handler.IncidentEvent) error {
	c.slack++
	return nil
}

func TestHandleRoutesIncident(t *testing.T) {
	c := &clients{claimed: map[string]bool{}}
	result, err := handler.Handle(context.Background(), handler.IncidentEvent{ID: "incident-1", Service: "checkout", State: "open"}, c)
	if err != nil {
		t.Fatal(err)
	}
	if !result.Routed || result.Owner != "payments-oncall" {
		t.Fatalf("unexpected result: %+v", result)
	}
	if len(c.audits) != 1 || c.slack != 1 {
		t.Fatalf("expected one audit and one Slack send")
	}
}
