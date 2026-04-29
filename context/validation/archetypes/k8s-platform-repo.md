---
accb_origin: canonical
accb_source_path: context/validation/archetypes/k8s-platform-repo.md
accb_role: validation
accb_version: 1
---

# Kubernetes Platform Repo Validation

Validate that API, worker, job, and cron roles are separate Kubernetes
workloads and that each role reaches Ready or Complete under the selected
cluster lane. Run IaC isolation for cluster and supporting resources.

Proof commands should include `kubectl` readiness checks, a route or service
smoke test, a bounded worker item, a job completion check, a cron execution
check when present, and rollback or rollout proof.

Common failure modes are collapsed workload roles, missing resource limits,
namespace drift, unreachable clusters, and event workers without DLQ proof.
Reference Kubernetes role, eventing, observability, and IaC isolation doctrine.
