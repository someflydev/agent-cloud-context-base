# Eventing Seam Selection

Use this skill to choose queue, topic, event bus, or stream for an event-driven boundary. It resolves ambiguity by making ordering, fan-out, replay, batching, retry, and DLQ requirements visible before mapping to a provider-native primitive.

## Procedure

1. Identify the producer, consumer set, and event purpose.
2. Determine ordering needs, including whether FIFO is required and what key defines order.
3. Determine fan-out: one worker, multiple independent subscribers, routing by event type, or analytics stream.
4. Determine replay window and whether replay is operator-driven, time-bounded, or unavailable.
5. Determine batching behavior, visibility or lease timeout, and maximum processing time.
6. Define retry policy, max attempts, backoff, and DLQ destination before naming a service.
7. Select a queue for one work-claiming consumer group.
8. Select a topic or event bus for one-to-many notification or rule-based routing.
9. Select a stream when ordered partitions, replay window, or analytics ingestion is central.
10. Map the choice to AWS, GCP, or Azure primitives and document semantic gaps.

## Good Triggers

- "queue or topic?"
- "event bus or stream?"
- "add a DLQ"
- "fan-out"
- "FIFO ordering"
- "replay events"

## Avoid

- choosing eventing technology before delivery semantics are declared
- using a topic when exactly one worker should claim each message
- using a queue when multiple independent subscribers must receive every event
- ignoring DLQ inspection and replay behavior
- assuming provider eventing primitives have identical retry semantics
