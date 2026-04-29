# App Runner VPC Connector

Load this stack when an App Runner service must reach private AWS resources. It owns the outbound VPC boundary, security groups, subnet selection, and private-network validation for App Runner.

## Image Surface

- The connector does not change the application image contract.
- Keep using ECR images tagged with git SHA and deployed by digest.
- Continue digest-pinning base images and running the app as non-root.
- Do not bake VPC, subnet, or security group identifiers into the image.
- Keep network configuration in IaC variables and environment-specific manifests.
- Scan the image separately from network validation.

## Service Surface

- App Runner remains HTTP request-driven after VPC attachment.
- Health checks must prove the app can start with the connector attached.
- Readiness must include required private dependencies such as RDS or ElastiCache when they are part of the request path.
- Scaling remains service min/max size and concurrency, not worker or queue scaling.
- Cold starts can include connector and dependency initialization cost.
- Background work still belongs in Lambda, ECS, or EventBridge, not App Runner.

## Networking

- Default App Runner egress is public; attach a VPC connector only for a named private resource.
- Select private subnets with routes that match required egress behavior.
- Attach security groups that allow only required outbound ports and destinations.
- Account for loss or change of public internet egress and add NAT only when justified.
- Prefer VPC endpoints for AWS APIs when private routing is required.
- Cross-reference `context/doctrine/vpc-and-private-networking.md`.

## Project Layout

```
infra/
  apprunner-service.*
  vpc-connector.*
  security-groups.*
tests/
  integration/
docs/
  network-boundary.md
```

## Local Run

```bash
docker run --rm -p 8080:8080 -e PORT=8080 <app_name>:dev
aws apprunner describe-vpc-connector --vpc-connector-arn <arn>
```

## Idempotency Pattern

- VPC attachment does not replace application idempotency.
- Private database writes still need replay-safe dedupe records.
- Include dependency reachability failures in retry classification.

## Identity Binding

- Use App Runner roles for service permissions and AWS service access.
- Keep security groups separate from IAM permissions; both must be least privilege.
- Reference `context/stacks/identity-aws-iam.md`.

## Secrets

- Store private database credentials in Secrets Manager.
- Use secret rotation compatible with connection pooling.
- Reference `context/stacks/secrets-aws-secrets-manager.md`.

## Observability

- Emit logs that distinguish DNS, connection refused, timeout, and auth failures.
- Add metrics for private dependency latency and connection errors.
- Reference `context/stacks/observability-otel-cloud.md`.

## Validation Gates (cross-reference)

- `cloudrun-revision-readiness`, `container-image-buildable`, `container-health-and-readiness`, and `container-private-network-when-required` from `context/accb/profile-rules.json`.

## Anti-Patterns

- Adding a VPC connector as a default security posture.
- Routing public AWS APIs through NAT without a cost and endpoint review.
- Claiming private reachability without testing from the deployed App Runner service.
