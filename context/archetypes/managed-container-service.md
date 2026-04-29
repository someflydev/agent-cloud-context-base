# Managed Container Service

Use this archetype for one Cloud Run, App Runner, or Container Apps service where a custom image is justified but the topology is still a single service. It fits APIs, adapters, renderers, or processors that need binaries, runtime control, or request duration beyond function limits without requiring Kubernetes.

## Common Goals

- Build one minimal, non-root container image.
- Expose health and readiness endpoints that match the provider runtime.
- Keep the service boundary singular and easy to smoke test.
- Bind secrets through provider-native identity and secret stores.
- Declare IaC dev/test isolation for service, image, logs, and dependencies.

## Required Context

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/container-image-discipline.md`
- `context/doctrine/cloud-secret-handling.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/doctrine/iac-dev-test-isolation.md`
- the dominant provider+container+language stack pack
- the dominant IaC stack pack
- one canonical example from `examples/canonical-cloudrun/`, `examples/canonical-apprunner/`, or `examples/canonical-aca/`

## Common Workflows

- `context/workflows/add-managed-container-service.md`
- `context/workflows/add-cloud-runtime-image.md`
- `context/workflows/add-iac-stack.md`
- `context/workflows/add-iac-isolation-pair.md`
- `context/workflows/add-secret-binding.md`
- `context/workflows/add-cloud-smoke-tests.md`

## Likely Manifests

- `manifests/container-cloudrun-fastapi.yaml`
- `manifests/container-cloudrun-go-echo.yaml`
- `manifests/container-apprunner-fastapi.yaml`
- `manifests/container-aca-dotnet.yaml`

## Likely Examples

- `examples/canonical-cloudrun/public-fastapi-service/`
- `examples/canonical-apprunner/public-hono-service/`
- `examples/canonical-aca/dotnet-public-api/`

## Typical Anti-Patterns

- Hosting multiple unrelated services in one image to save money.
- Baking secrets or per-environment config into the image.
- Skipping readiness because the service starts locally.
- Moving to Kubernetes only because the Dockerfile exists.
- Using one mutable latest tag across dev and test.

## Validation Gates (summary)

- container-image-buildable: Container image builds with a clean SBOM and non-root user.
- container-health-and-readiness: Service responds to health and readiness probes after deploy.
- iac-dev-test-disjoint: Service names, state, image tags, and secret paths are disjoint.
- secret-binding-via-identity: Runtime reads secret references via provider identity.
