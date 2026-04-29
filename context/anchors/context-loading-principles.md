# Context Loading Principles Anchor

- Load one workflow as the first execution guide.
- Load one provider, runtime, and language stack as the primary implementation guide.
- Load one IaC stack when cloud resources are involved.
- Load one archetype and one canonical example as the first pass.
- Use manifests to assemble bundles instead of hand-collecting files.
- Do not load a second provider unless the task is explicitly comparative.
- Do not load a second runtime tier in the first pass.
- Do not scan `context/`, `examples/`, or `manifests/` wholesale.
