# Add K8s Workload Role

Use this workflow when adding one Kubernetes workload role such as API, worker, job, cronjob, or control-plane to an EKS, GKE, or AKS platform repo.

## Preconditions

- Cluster provider, workload role, language, and overlay tool are chosen.
- Dev/test namespaces, state, resource names, secret paths, and workload identities are disjoint.
- The repo convention is known: Kustomize base/overlays or Helm templates/values.

## Sequence

1. Pick the matching role pack: API Deployment, worker Deployment, Job, CronJob, or control-plane workload.
2. Author the workload code or command surface for the role.
3. Add Kubernetes manifests to `base/` plus `overlays/dev` and `overlays/test`, or Helm templates plus `values.dev.yaml` and `values.test.yaml`.
4. Declare probes, resource requests and limits, service account, workload identity, and config references.
5. Bind only the provider resources required by this role.
6. Add PodDisruptionBudget, NetworkPolicy, or rollout settings when the role needs them.
7. Render and lint the manifests before applying.
8. Add smoke tests for readiness, job completion, or cron execution as appropriate.
9. Add integration tests against a real cluster or kind when provider identity is not required.

## Outputs

- Role code, Kubernetes manifests or chart changes, env overlays, probes, quotas, identity binding, and tests.

## Validation Gates

- `k8s-role-separation-evident` from `profile-rules.json`
- `k8s-rolling-rollout-and-rollback-paths`
- `identity-least-privilege-declared`
- `iac-dev-test-disjoint`

## Related Docs

- `context/doctrine/k8s-workload-role-separation.md`
- `context/doctrine/identity-and-least-privilege.md`
- `context/stacks/k8s-api-workload.md`
- `examples/canonical-eks/multi-role-platform/`

## Common Pitfalls

- Adding a second role into an existing Deployment because it is quicker.
- Copying overlays until dev and test drift silently.
- Granting one namespace-wide service account to every workload.
