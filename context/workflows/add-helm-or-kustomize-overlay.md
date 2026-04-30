# Add Helm Or Kustomize Overlay

Use this workflow when adding or updating environment overlays for an existing Kubernetes workload.

## Preconditions

- Repo convention is known: Helm or Kustomize.
- Target workload and environments are identified.
- Dev/test namespace, values, secret paths, and identities are disjoint.

## Sequence

1. Confirm the repo's existing convention and do not mix Helm and Kustomize without an explicit migration.
2. For Kustomize, update `base/` and `overlays/dev` plus `overlays/test`.
3. For Helm, update templates plus `values.dev.yaml` and `values.test.yaml`.
4. Keep shared defaults in one place and environment differences in overlays or values.
5. Wire ConfigMap, Secret reference, service account, probes, resources, and NetworkPolicy changes.
6. Render manifests for dev and test.
7. Lint the rendered output and check for missing selectors, labels, and references.
8. Apply against a test cluster when the change affects runtime behavior.
9. Add or update smoke assertions for readiness, job completion, or worker processing.

## Outputs

- Helm chart or Kustomize overlay changes for dev and test plus rendered/linted verification.

## Validation Gates

- `k8s-role-separation-evident` from `profile-rules.json`
- `k8s-rolling-rollout-and-rollback-paths`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/k8s-workload-role-separation.md`
- `context/doctrine/iac-dev-test-isolation.md`
- `context/stacks/k8s-helm-conventions.md`

## Common Pitfalls

- Copying full manifests into each environment instead of overlaying the differences.
- Letting secret values leak into rendered files committed to source.
- Applying to dev only and assuming test will render the same.
