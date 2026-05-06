package replay

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

func (c *clients) LookupOwner(ctx context.Context, service string) (string, error) { return "payments-oncall", nil }
func (c *clients) WriteAudit(ctx context.Context, row handler.AuditRow) error {
	c.audits = append(c.audits, row)
	return nil
}
func (c *clients) SendSlack(ctx context.Context, owner string, event handler.IncidentEvent) error {
	c.slack++
	return nil
}

func TestReplaySuppressesDuplicateIncident(t *testing.T) {
	c := &clients{claimed: map[string]bool{}}
	event := handler.IncidentEvent{ID: "incident-1", Service: "checkout", State: "open"}
	first, err := handler.Handle(context.Background(), event, c)
	if err != nil {
		t.Fatal(err)
	}
	second, err := handler.Handle(context.Background(), event, c)
	if err != nil {
		t.Fatal(err)
	}
	if !first.Routed || !second.Duplicate {
		t.Fatalf("unexpected replay results: first=%+v second=%+v", first, second)
	}
	if len(c.audits) != 1 || c.slack != 1 {
		t.Fatalf("duplicate created side effects")
	}
}
