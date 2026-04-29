# Eventing GCP Pubsub

Load this stack for Google Cloud eventing in accb-derived repos. It owns Pub/Sub topics, subscriptions, ordering, retry, dead-letter topics, Eventarc routing, Cloud Tasks delayed work, and validation.

## Capability Surface

- Primary bus: Pub/Sub.
- Routing layer: Eventarc.
- Delayed work: Cloud Tasks.
- Dev topic names: `<repo>-dev-<event>`.
- Test topic names: `<repo>-test-<event>`.
- Dev DLQ topic: `<repo>-dev-<source>-dlq`.
- Test DLQ topic: `<repo>-test-<source>-dlq`.
- Reference `context/doctrine/eventing-and-dlq-discipline.md`.

## Pub/Sub Topic Pattern

- Use one topic per event family.
- Enable message ordering only when handlers require it.
- Use schema validation when event contracts are stable.
- Set retention deliberately.
- Use labels for project, environment, and owner.
- Keep publisher IAM scoped to the topic.

## Subscription Pattern

- Use pull subscriptions for worker services.
- Use push subscriptions for HTTP endpoints such as Cloud Run.
- Configure ack deadline above normal processing time.
- Configure retry policy with bounded backoff.
- Configure a dead-letter topic for retrying subscriptions.
- Keep max delivery attempts explicit.
- Include correlation and trace fields in message attributes.

## Eventarc Pattern

- Use Eventarc for provider-native event routing to Cloud Run and GKE.
- Filter by exact event type and resource.
- Keep trigger service accounts environment-specific.
- Document audit-log event sources when they are used.
- Route Eventarc failures into observable retry paths where supported.

## Cloud Tasks Pattern

- Use Cloud Tasks for delayed or rate-limited work.
- Do not use Pub/Sub as an ad hoc delay queue.
- Configure dispatch deadline and retry settings.
- Use OIDC tokens for authenticated HTTP targets.
- Keep queue names environment-specific.

## Identity Binding

- Publishers receive topic publisher permissions only.
- Consumers receive subscriber permissions only.
- Push subscriptions use a dedicated service account.
- DLQ readers are separate from primary consumers.
- Reference `context/stacks/identity-gcp-iam-sa.md`.

## CLI Surface

```bash
gcloud pubsub topics describe <repo>-dev-<topic>
gcloud pubsub subscriptions describe <repo>-test-<subscription>
gcloud eventarc triggers describe <trigger> --location=<region>
```

## Observability

- Alert on undelivered message count and oldest unacked message age.
- Track dead-letter topic publish counts.
- Log message ID, ordering key, delivery attempt, trace ID, and correlation ID.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates

- Retry policy is explicit.
- Dead-letter topic exists for retrying subscriptions.
- Ordering keys are declared only when needed.
- Dev and test topics differ.
- Replay or DLQ inspection path is documented.

## Anti-Patterns

- Project-wide Pub/Sub IAM for workloads.
- Push endpoints without authentication.
- Unbounded retry behavior.
- Pub/Sub used for precise scheduling.
- DLQ messages without source metadata.
