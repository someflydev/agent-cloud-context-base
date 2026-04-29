# Excellent Cloud Source Map

This note records how the sibling reference catalogs informed `accb` scenario and generation artifacts. The catalogs are provenance only; generated repos depend on `accb` files, manifests, and examples, not on the sibling reference repository.

## Catalog Mapping

- Function catalog: informs `context/scenarios/function-scenarios.md`, function stack packs, function manifests, and PROMPT_18-PROMPT_20 canonical examples.
- Container catalog: informs `context/scenarios/container-scenarios.md`, managed-container stack packs, container manifests, and PROMPT_21-PROMPT_22 canonical examples.
- K8s catalog: informs `context/scenarios/kubernetes-scenarios.md`, Kubernetes stack packs, k8s manifests, and PROMPT_23 canonical examples.

## Source Catalogs

- `excellent-cloud-prompts/01--funcs--100-excellent-prompts.md`
- `excellent-cloud-prompts/03--containers--100-excellent-prompts.md`
- `excellent-cloud-prompts/05--k8s--100-excellent-prompts.md`

## No Copying Rule

Use patterns and representative names only. Do not paste the original 100-entry catalogs into `accb`, and do not preserve the source wording as hidden template text. Scenario files should describe reusable workload families, support-service seams, routing outcomes, and validation expectations in `accb` language.
