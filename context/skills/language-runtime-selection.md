# Language Runtime Selection

Use this skill to choose the application language for a function or managed container when the prompt leaves language open. It resolves ambiguity by checking provider support, cold-start expectations, repo affinity, and the smallest coherent runtime for the workload.

## Procedure

1. Identify the selected provider and runtime tier before choosing language.
2. Confirm provider runtime support for the target function or managed-container stack cell.
3. Check whether the workload needs libraries or SDKs that strongly favor Python, TypeScript/Node, Go, or .NET.
4. Weigh cold-start budget, package size, and startup behavior against the user-facing contract.
5. Read repo signals such as lockfiles, module files, project files, source directories, and imports.
6. Prefer existing repo language affinity when it does not conflict with provider runtime support.
7. For thin event handlers, prefer the smallest runtime that keeps handler, tests, and IaC cognitively coherent.
8. For managed containers, include framework fit such as FastAPI, Hono, Echo, or ASP.NET only after the language is justified.
9. Stop when provider support and repo language signals conflict and the user has not requested a migration.
10. Record the chosen language beside provider, runtime tier, IaC tool, and canonical example selection.

## Good Triggers

- "what language should this function use?"
- "Node or Python?"
- "pick the runtime"
- "cold start matters"
- "no language specified"
- "which stack file should load after runtime routing?"

## Avoid

- picking a language unsupported by the selected provider runtime
- ignoring existing lockfiles or project files
- choosing a heavy runtime for a thin trigger without cause
- using cold-start claims without tying them to the workload contract
- selecting a framework before the language decision is made
