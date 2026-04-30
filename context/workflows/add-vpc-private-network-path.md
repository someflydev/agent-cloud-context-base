# Add VPC Private Network Path

Use this workflow when attaching a workload to a private network path for private database, cache, service, or egress access.

## Preconditions

- The private dependency and provider network primitive are known.
- The need for private networking is justified by data, compliance, routing, or provider access constraints.
- Dev/test VPC, subnet, connector, endpoint, identity, and state naming are disjoint.

## Sequence

1. Confirm the workload cannot safely use public managed endpoints with identity and encryption alone.
2. Pick the provider primitive: Lambda VPC config, Cloud Run VPC connector, Container Apps VNet integration, or Kubernetes networking.
3. Author IaC for subnets, connectors, endpoints, route tables, security groups or firewall rules, and DNS settings.
4. Keep dev and test networks or connector names separate and auditable.
5. Update workload deployment configuration to use the private path.
6. Add least-privilege network rules for only the target dependency and required egress.
7. Test reachability to the private target.
8. Test outbound DNS and required public egress behavior.
9. Run plan/preview and isolation validation.

## Outputs

- Private networking IaC, workload network attachment, firewall/routing rules, and reachability tests.

## Validation Gates

- `container-private-network-when-required` from `profile-rules.json`
- `iac-dev-test-disjoint`
- `changed-boundary-proof`

## Related Docs

- `context/doctrine/vpc-and-private-networking.md`
- `context/doctrine/iac-dev-test-isolation.md`
- `context/stacks/apprunner-vpc-connector.md`

## Common Pitfalls

- Adding VPC attachment without testing DNS and outbound dependencies.
- Routing all egress privately when only one dependency needed it.
- Reusing the dev connector or subnet in test because names look similar.
