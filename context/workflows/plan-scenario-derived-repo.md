# Plan Scenario Derived Repo

Use this workflow when turning a business-shaped cloud workload prompt, including excellent-cloud-style catalog prompts, into a concrete `new_cloud_repo.py` invocation and first prompt sequence.

## Preconditions

- User scenario text is available and explicit provider, runtime, language, or IaC choices are preserved.
- `context/router/scenario-router.md` and `context/scenarios/scenario-profile-map.yaml` exist.
- Generation waits if the scenario conflicts with the requested runtime tier.

## Sequence

1. Run the scenario through `context/router/scenario-router.md`.
2. Load `context/scenarios/scenario-profile-map.yaml` and identify candidate archetype, support services, and examples.
3. Preserve explicit user choices for provider, runtime tier, language, and IaC tool.
4. Infer only missing choices and label them as assumptions.
5. Stop if the scenario implies a different runtime tier than the user requested.
6. Choose the likely manifest, archetype, support services, stack packs, and canonical examples.
7. Declare the dev/test isolation surface: state, env-var prefixes, secret paths, resource names, and identities.
8. Print the exact `python3 scripts/new_cloud_repo.py ...` command with explicit flags.
9. Draft the first prompt sequence for the derived repo using actual generated-state expectations.

## Outputs

- Scenario routing decision, chosen manifest/profile, exact bootstrap command, and initial prompt sequence outline.

## Validation Gates

- `startup-rehydration` from `profile-rules.json`
- `iac-dev-test-disjoint`
- `changed-boundary-proof`

## Related Docs

- `context/doctrine/function-vs-container-vs-k8s.md`
- `context/doctrine/iac-dev-test-isolation.md`
- `context/stacks/iac-terraform-aws.md`

## Common Pitfalls

- Overriding an explicit user choice because a scenario mapping prefers another stack.
- Generating a repo after a runtime-tier contradiction.
- Printing a vague bootstrap command that leaves provider or IaC choices implicit.
