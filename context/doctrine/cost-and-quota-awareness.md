# Cost And Quota Awareness

Cloud context must prevent accidental spend and quota exhaustion. Every workload declares expected cost, scaling bounds, and test teardown before real resources are created.

## Declare Cost Bands

- State an expected monthly cost band for each environment.
- Keep dev and test together at or below $50 per month unless the operator opts in.
- Treat prod cost as operator-driven and outside automatic generation.
- Include always-on resources in the estimate.
- Call out NAT gateways, clusters, provisioned concurrency, and reservations explicitly.

## Cap Throughput

- Set rate ceilings on inbound triggers.
- Set concurrency caps for functions.
- Set max replicas for managed containers.
- Set max nodes or node pool limits for Kubernetes.
- Record quota assumptions that could block deployment.

## Alarm Budgets

- Define a budget alarm path for generated cloud resources.
- Route budget notifications to an operator-owned channel.
- Include DLQ and error-rate alarms with cost-sensitive eventing.
- Avoid silent autoscaling with no alerting.
- Treat missing budget alarms as incomplete for Lane B examples.

## Guard Tests

- Give Lane B integration tests automatic teardown.
- Add max-runtime guards to tests that provision cloud resources.
- Do not leave reservations, NAT gateways, clusters, or always-on compute behind after tests.
- Require explicit manifest opt-in for persistent test resources.
- Prefer emulator tests when cost proof is not the risk being exercised.
