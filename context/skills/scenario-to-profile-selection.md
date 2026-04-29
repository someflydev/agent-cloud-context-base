# Scenario To Profile Selection

Use this skill to turn an excellent-catalog-style cloud workload prompt into a concrete `accb` profile. It resolves ambiguity by matching scenario patterns, preserving explicit choices, and selecting likely manifest, archetype, support services, examples, and validation gates from the scenario map.

## Procedure

1. Extract explicit provider, runtime tier, language, IaC tool, support services, and validation demands from the prompt.
2. Match the business workload shape against `context/scenarios/scenario-profile-map.yaml`.
3. Preserve explicit provider, runtime tier, language, and IaC choices unless they conflict with the scenario.
4. Select the scenario pattern's runtime tier, archetype, likely manifest, support services, and preferred examples for unspecified axes.
5. Run provider, runtime, IaC, stack, archetype, and task routers to confirm the inferred profile.
6. Select validation gates that prove the scenario's critical cloud boundaries.
7. Stop if the scenario implies a different runtime tier than the user explicitly requested.
8. Stop if two scenario patterns tie and would produce different runtime tiers or archetypes.
9. Record inferred choices separately from explicit user choices.
10. Use the profile to drive context-bundle assembly instead of loading every scenario document.

## Good Triggers

- "turn this prompt into a repo"
- "excellent cloud prompt"
- "claims intake"
- "image moderation flow"
- "scenario-derived repo"
- "map this workload to an accb profile"

## Avoid

- overriding explicit provider or IaC choices without naming the conflict
- forcing a scenario when the prompt only names a provider service
- ignoring runtime-tier conflict between scenario and user request
- loading unrelated scenario families as background
- treating inferred choices as if the user explicitly supplied them
