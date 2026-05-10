# Manifests

Machine-readable bundle selection for cloud archetypes, runtimes, providers,
and IaC tools.

Each `*.yaml` manifest binds one repo profile to:

- an archetype, provider, runtime tier, primary stack, language, and IaC tool
- required and optional context files
- preferred canonical examples and starter templates
- dev/test IaC state, environment prefix, secret path, and resource-naming
  isolation
- smoke and integration-test expectations

Generated repos should be created from manifests with
[`../scripts/new_cloud_repo.py`](../scripts/new_cloud_repo.py). Payload-only
inspection uses [`../scripts/accb_payload.py`](../scripts/accb_payload.py).

## Validation

```bash
python3 scripts/validate_manifests.py
python3 scripts/preview_context_bundle.py func-aws-lambda-python
```

`multi-provider-event-pipeline.yaml` is intentionally catalog-only in v1 and is
not a `new_cloud_repo.py` target.
