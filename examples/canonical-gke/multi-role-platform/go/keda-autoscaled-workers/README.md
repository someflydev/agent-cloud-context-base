# GKE Go KEDA Autoscaled Workers

This sub-example narrows the GKE Go platform to the worker autoscaling contract. Lane A uses kind plus `minisky` Pub/Sub fakes; Lane B uses an ephemeral GKE Autopilot test cluster. The worker is idempotent by message ID and the ScaledObject targets Pub/Sub backlog.
