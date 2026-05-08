# Repo Purpose

`accb` is a foundation for cloud-native backend repositories that will be generated, modified, and verified with coding assistants. It is not an application template alone; it is the context, routing, payload, and validation layer around generated cloud repos.

## What It Optimizes For

- Cloud-native backends with explicit trigger boundaries: functions, managed containers, and Kubernetes workloads are selected as deliberate runtime tiers.
- Infrastructure as Code dev/test isolation: every cloud profile must declare separate state, environment prefixes, secret paths, and resource naming for `dev` and `test`.
- Identity-bound secrets: examples and manifests prefer provider identity bindings over copied credentials or checked-in secret values.
- Real validation gates: `done` requires proof from scripts, smoke tests, IaC isolation checks, or explicitly gated local-provider and real-cloud lanes.

## What It Does Not Try To Be

`accb` is not a frontend framework catalog. Frontend choices can be added by a generated repo, but the base exists to route backend runtime tier, cloud provider, IaC, identity, secrets, and validation decisions.

`accb` is not a local-Dokku operator. The repo models managed cloud runtimes, local-provider harnesses, and ephemeral real-cloud tests; it does not treat local deployment convenience as equivalent to the managed boundary.

`accb` is not a multi-cloud abstraction layer. Provider-specific identity, eventing, secret stores, managed databases, and deployment models remain visible because hiding them would produce weaker tests and vaguer operations.

`accb` is not a vendor portability promise. It can compare provider options and generate parallel profiles, but a Lambda/S3/DynamoDB system and a Cloud Functions/GCS/Firestore system are separate designs with separate operational truth.
