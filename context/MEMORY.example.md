# MEMORY.md

## Repo Purpose

- Provider: <aws|gcp|azure>
- Runtime tier: <function|container|k8s>
- Language: <python|typescript|go|dotnet>
- IaC tool: <terraform|pulumi-typescript|pulumi-python|pulumi-go|pulumi-dotnet>
- Purpose: <short description of the generated cloud service>

## Active Boundary

- Prompt or workflow: <current prompt, workflow, or manifest>
- Archetype: <selected archetype>
- Dev/test isolation surface: <separate state, env prefix, secret path, and resource naming>

## Non-obvious Invariants

- Dev and test must use separate state backends or stack names.
- Dev and test must use separate secret paths or secret names.
- Dev and test resources must be distinguishable by name.
- Workload identity must be least-privilege and environment-scoped.
- Trigger payloads and replay behavior must stay stable.

## Known Gotchas

- <cloud-specific pitfall worth preserving>

## External References

- <provider docs, dashboards, runbooks, or tickets; no secrets>
