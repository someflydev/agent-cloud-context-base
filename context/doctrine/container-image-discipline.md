# Container Image Discipline

Container images are deployment artifacts, not loose build byproducts. Managed container and Kubernetes workloads must produce images that are reproducible, scannable, and promotable across environments.

## Build Reproducibly

- Pin base images by digest, not tag.
- Use distroless or slim bases where feasible.
- Use multi-stage builds for compiled languages and dependency-heavy runtimes.
- Run as a non-root user.
- Keep build-time tooling out of the final runtime image.

## Keep Secrets Out

- Do not bake secrets into image layers.
- Do not copy local cloud credentials into the build context.
- Use runtime secret bindings from Secrets Manager, Secret Manager, or Key Vault.
- Keep IaC source free of secret literals.
- Scan Dockerfiles for accidental credential paths.

## Scan And Describe

- Produce an SBOM with provider-native tooling or syft.
- Run vulnerability scanning in test with Trivy or the provider registry scanner.
- Fail or mark incomplete when critical image vulnerabilities are untriaged.
- Record the image registry in the manifest.
- Use ECR, Artifact Registry, or ACR according to provider.

## Promote By Tag

- Tag images with git SHA and semver when a release version exists.
- Use `latest` only for dev.
- Promote from dev to test by immutable tag, not rebuild.
- Keep image digest visible in IaC outputs.
- Roll back by selecting a prior immutable tag.
