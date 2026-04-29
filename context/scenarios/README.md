# Scenarios

Scenarios are workload taxonomies, not implementation templates. They translate business-shaped prompts into archetype, runtime-tier, provider, support-service, manifest, canonical-example, and validation choices so `accb` can route a request before later prompts generate concrete stacks.

The source catalogs are provenance references from the sibling repository, not copied runtime dependencies:

- `excellent-cloud-prompts/01--funcs--100-excellent-prompts.md`
- `excellent-cloud-prompts/03--containers--100-excellent-prompts.md`
- `excellent-cloud-prompts/05--k8s--100-excellent-prompts.md`

These files rephrase recurring workload patterns from those catalogs. They do not reproduce the full prompt entries, provider-by-provider prose, or generated app ideas.

## Files

- `function-scenarios.md` covers function-first trigger, queue, stream, webhook, identity, alert, and scheduled maintenance families.
- `container-scenarios.md` covers managed-container systems that need custom images, private services, sidecars, jobs, or partner network boundaries.
- `kubernetes-scenarios.md` covers platform shapes where API, worker, job, cron, control-plane, tenant, or compute topology warrants Kubernetes.
- `scenario-profile-map.yaml` is the machine-readable index used by routers, manifests, docs, and tests.
- `excellent-cloud-source-map.md` records traceability from reference catalogs to `accb` artifacts.

## Routing Use

Scenario routing should preserve explicit user choices for provider, language, IaC, and runtime tier. When a business prompt implies a stronger topology than the explicit runtime choice can support, stop and resolve the conflict instead of silently escalating.
