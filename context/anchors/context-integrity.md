# Context Integrity Anchor

- Run `python3 scripts/validate_context.py` before trusting metadata-heavy changes once the script exists.
- Run `python3 scripts/validate_manifests.py` when touching only manifest logic once the script exists.
- Run `python3 scripts/validate_iac_isolation.py <path>` after touching any IaC artifact once the script exists.
- Keep prompt numbering monotonic in `.prompts/`.
- Keep prompt numbering monotonic in `examples/canonical-prompts/` once examples exist.
- Keep `examples/catalog.json` aligned with the examples tree once it exists.
- Keep `verification/example_registry.yaml` aligned with the examples tree once it exists.
- Treat missing validation scripts as a prompt-sequence timing fact, not a reason to invent replacements.
