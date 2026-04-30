# Add Cloud Runtime Image

Use this workflow when authoring or updating a container image for managed containers or Kubernetes workloads.

## Preconditions

- Runtime language, service role, target registry, and image consumers are known.
- Dev/test registry names, tags, and deployment references are disjoint where the provider requires it.
- SBOM and vulnerability scanning tools are available or explicitly marked incomplete.

## Sequence

1. Pick a minimal base image pinned by digest.
2. Use a multi-stage Dockerfile that separates build tooling from runtime contents.
3. Create and run as a non-root user.
4. Copy only the artifacts required for runtime execution.
5. Add healthcheck or keep the platform-specific health endpoint aligned with service code.
6. Build the image locally and run the container startup path.
7. Generate an SBOM with `syft` when available.
8. Run a vulnerability scan with `trivy` when available and record accepted exceptions.
9. Push to ECR, Artifact Registry, or ACR with git-SHA and semver tags when release is in scope.

## Outputs

- Dockerfile, image build command, SBOM, vulnerability scan result, registry tags, and deployment reference update.

## Validation Gates

- `container-image-buildable` from `profile-rules.json`
- `container-health-and-readiness`
- `secret-not-in-source`

## Related Docs

- `context/doctrine/container-image-discipline.md`
- `context/doctrine/cold-start-and-runtime-selection.md`
- `context/stacks/cloudrun-go-echo.md`

## Common Pitfalls

- Using floating base tags for production images.
- Leaving build tools, package caches, or secrets in the runtime layer.
- Publishing only `latest` without a git-SHA tag.
