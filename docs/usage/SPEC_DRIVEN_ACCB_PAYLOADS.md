# Spec-Driven `.accb/` Payloads

The `.accb/` payload is the generated repo-local operating boundary. It records the selected cloud profile and carries enough specs, validation gates, and inspection scripts for a new assistant session to boot consistently.

## Composition Inputs

| Input | Source | Role |
| --- | --- | --- |
| Profile rules | `context/accb/profile-rules.json` | Default doctrines, routers, anchors, capability gates, and support-service capability mapping. |
| Archetype | `context/archetypes/*.md` | Repo shape and validation expectations. |
| Primary stack | `context/stacks/*.md` | Runtime and implementation guidance. |
| Manifest | `manifests/*.yaml` | Selected provider/runtime/language/IaC bundle, required context, examples, templates, and isolation declarations. |
| Scenario patterns | `context/scenarios/scenario-profile-map.yaml` | Workload pattern metadata and likely support services. |
| Support services | CLI `--support-service` flags | Storage, eventing, secrets, identity, search, or vector-store capabilities added to the profile. |

## Payload Outputs

`scripts/accb_payload.py` writes `.accb/profile/selection.json`, spec files, validation checklists, capability coverage, selected scenario metadata, `SESSION_BOOT.md`, and helper scripts. Generated repos should treat those files as the boot authority for assistant behavior.

## Drift Detection

Run this in a generated repo:

```bash
python3 .accb/scripts/accb_verify.py
```

`accb_verify` checks the payload shape, profile selection, validation surfaces, and expected files. If the generated repo changes its provider, runtime tier, IaC layout, or support services, regenerate or update the `.accb/` payload before claiming completion.
