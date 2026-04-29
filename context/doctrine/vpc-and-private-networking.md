# VPC And Private Networking

Private networking is an explicit boundary, not a default. Attach serverless or managed workloads to a private network only when a concrete private resource requires it.

## Declare The Network Boundary

- Name the private resource before adding network attachment.
- Declare whether the workload reaches a database, private endpoint, on-prem link, or in-cluster service.
- Keep public egress available only when the contract requires it.
- Include DNS behavior in the network decision.
- Record the network shape in the manifest and IaC variables.

## Use Provider Shapes

- Configure AWS Lambda with VPC config, subnets, and security groups when it must reach private AWS resources.
- Account for Lambda cold-start cost when VPC attachment is enabled.
- Configure Cloud Run and Cloud Functions with Serverless VPC Access or Direct VPC egress when private reachability is required.
- Configure Azure Container Apps with VNet integration for private resources.
- Use in-cluster networking and private endpoints for Kubernetes workloads.

## Avoid Default Attachment

- Do not attach to a VPC because it feels more secure.
- Do not hide outbound internet needs behind a NAT gateway without cost review.
- Do not route public managed-service calls through private networking unless the provider requires it.
- Prefer private endpoints when the managed service supports them and the workload requires isolation.
- Keep local emulator tests separate from private-network proof.

## Test Reachability

- Test connection to the private resource from the deployed workload.
- Test outbound DNS resolution from the same environment.
- Test failure behavior when the private endpoint is unavailable.
- Verify security groups, network policies, or firewall rules through IaC.
- Mark completion incomplete when private reachability is assumed but not proven.
