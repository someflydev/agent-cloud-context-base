# Eventing Azure Service Bus Event Grid

Load this stack for Azure eventing in accb-derived repos. It owns Service Bus, Event Grid, Event Hubs, sessions, DLQs, retry behavior, and identity-based binding.

## Capability Surface

- Queue and topics: Azure Service Bus.
- Event routing: Event Grid.
- Streaming: Event Hubs.
- Dev names: `<repo>-dev-<event-role>`.
- Test names: `<repo>-test-<event-role>`.
- Dev DLQ scope: environment-specific queue or subscription DLQ.
- Test DLQ scope: environment-specific queue or subscription DLQ.
- Reference `context/doctrine/eventing-and-dlq-discipline.md`.

## Service Bus Pattern

- Use queues for point-to-point work.
- Use topics and subscriptions for fanout.
- Use sessions when ordered processing is required.
- Set lock duration above normal handler duration.
- Configure max delivery count.
- Use built-in DLQ behavior for queues and subscriptions.
- Enable duplicate detection when producer retries can duplicate sends.

## Event Grid Pattern

- Use system topics for Azure resource events.
- Use custom topics for application domain events.
- Use partner topics only when the integration requires them.
- Configure event subscriptions with exact filters.
- Add dead-letter destination when configured delivery requires recovery.
- Use managed identity for delivery where supported.

## Event Hubs Pattern

- Use Event Hubs for high-throughput streaming.
- Define consumer groups per independent processor.
- Use Blob Storage checkpoints.
- Keep partition count aligned with throughput and ordering needs.
- Do not use Event Hubs as a generic task queue.

## Identity Binding

- Use managed identity for senders and receivers when possible.
- Grant Service Bus Data Sender or Receiver at narrow scope.
- Grant Event Grid roles only to publishers or subscription managers as needed.
- Keep DLQ inspection permissions separate.
- Reference `context/stacks/identity-azure-entra-mi.md`.

## Replay

- Service Bus DLQ replay is operator-driven.
- Event Grid replay depends on dead-letter storage or source re-emission.
- Event Hubs replay uses retained offsets and consumer groups.
- Limit replay batches.
- Re-run through idempotent handlers.

## CLI Surface

```bash
az servicebus queue show --resource-group <rg> --namespace-name <ns> --name <queue>
az eventgrid event-subscription show --name <name> --source-resource-id <id>
az eventhubs eventhub show --resource-group <rg> --namespace-name <ns> --name <hub>
```

## Observability

- Alert on active DLQ message count.
- Track lock lost, abandon, dead-letter, and complete counts.
- Log message ID, session ID, delivery count, trace ID, and correlation ID.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates

- Every retrying queue or subscription has DLQ handling.
- Session use is declared when ordering is required.
- Dev and test namespaces or entity names differ.
- Managed identities have narrow data-plane roles.
- Replay process is documented.

## Anti-Patterns

- Shared namespace entities without environment suffixes.
- Connection strings copied into app settings.
- Event Hubs used for low-volume command queues.
- Infinite retries without DLQ handling.
- Broad Contributor role for event consumers.
