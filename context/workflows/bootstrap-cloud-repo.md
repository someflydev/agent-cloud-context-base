# Bootstrap Cloud Repo

Use this workflow when generating a new derived cloud-native repository from `accb` through the repo generator and the operator already knows the intended archetype, provider, runtime tier, primary language, IaC tool, and dev/test isolation surface.

## Preconditions

- Archetype, provider, runtime tier, language, and IaC tool are chosen.
- Dev/test isolation is declared: state, env-var prefixes, secret paths, identities, and resource naming.
- The selected manifest is available after PROMPT_14 and `scripts/new_cloud_repo.py` is available after PROMPT_16.

## Sequence

1. Load the closest archetype, stack pack, and manifest for the requested repo shape.
2. Confirm the requested runtime tier matches the archetype and does not conflict with the scenario.
3. Print the dev/test isolation surface before generating any cloud resource.
4. Run `python3 scripts/new_cloud_repo.py` with explicit flags for archetype, provider, tier, language, IaC tool, output path, and manifest.
5. Review generated `.accb/` payload files for profile, manifest, validation contract, and session boot instructions.
6. Review generated IaC env names, state keys, secret paths, and identity names for disjoint dev/test behavior.
7. Run the generated repo verification command: `python .accb/scripts/accb_verify.py`.
8. Commit the initial scaffold only after verification passes or record completion as `incomplete`.

## Outputs

- A derived repository with a `.accb/` operating payload.
- Initial workload, IaC, test, and validation scaffolding matching the chosen manifest.
- A first commit boundary for the generated scaffold.

## Validation Gates

- `startup-rehydration` from `profile-rules.json`
- `iac-dev-test-disjoint`
- `changed-boundary-proof`

## Related Docs

- `context/doctrine/iac-dev-test-isolation.md`
- `context/doctrine/context-loading-rules.md`
- `context/stacks/iac-terraform-conventions.md`

## Common Pitfalls

- Generating before declaring dev/test state, naming, env-var prefixes, secret paths, and identities.
- Choosing a manifest because it is familiar instead of because it matches the requested runtime tier.
- Treating generated `.accb/` files as optional docs instead of repo-local operating rules.
