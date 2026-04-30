# Add Managed Container Service

Use this workflow when adding a Cloud Run, App Runner, or Azure Container Apps service, including public APIs, private workers, callbacks, or scheduled managed-container services.

## Preconditions

- Provider, managed-container platform, language, service role, and IaC tool are chosen.
- Dev/test state, names, env-var prefixes, secret paths, identities, and registry tags are disjoint.
- The service's public or private exposure model is declared.

## Sequence

1. Author service code in the chosen language with health and readiness endpoints or equivalent startup checks.
2. Author a Dockerfile per `container-image-discipline`: pinned base digest, multi-stage build, non-root user, and minimal runtime.
3. Declare service IaC: service, revision settings, identity, secret references, networking, registry permissions, and autoscaling.
4. Bind secrets through provider identity and secret store references.
5. Add probes, timeout, concurrency, CPU, memory, min/max instance, and ingress settings explicitly.
6. Add smoke tests for image build, container startup, `/healthz`, and one representative request.
7. Add integration tests against dev or test for deployed request handling and any managed-service dependency.
8. Generate SBOM and run a vulnerability scan before publish when the repo has those tools.
9. Run `terraform plan` or `pulumi preview` for dev and test.

## Outputs

- Service code, Dockerfile, IaC service resources, identity binding, probes, smoke tests, and integration tests.

## Validation Gates

- `container-image-buildable` from `profile-rules.json`
- `container-health-and-readiness`
- `secret-binding-via-identity`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/container-image-discipline.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/stacks/cloudrun-python-fastapi.md`
- `examples/canonical-cloudrun/public-api-private-worker-job/`

## Common Pitfalls

- Sharing one image across services with different runtime responsibilities.
- Exposing a private worker because the default ingress setting was accepted.
- Treating a local container run as proof of managed-container deployment.
