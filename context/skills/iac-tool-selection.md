# IaC Tool Selection

Use this skill to choose Terraform or a Pulumi language when infrastructure tooling is unspecified or weakly signaled. It resolves ambiguity by honoring explicit requests, reading repo evidence, applying application-language affinity, and using Terraform only when no Pulumi language is a coherent fit.

## Procedure

1. Respect an explicit user request for Terraform or Pulumi in a named language.
2. Read repo signals: `*.tf`, `terraform/`, `Pulumi.yaml`, Pulumi stack files, language-specific Pulumi imports, and IaC package dependencies.
3. Stop if Terraform and Pulumi are both signaled with no migration or comparison intent.
4. If Pulumi is selected, infer exactly one Pulumi language from user text or repo files.
5. When no tool is specified, apply application-language affinity for Python, TypeScript/Node, Go, or .NET.
6. Treat Pulumi-.NET as an Azure-skewed choice, not the default cross-cloud answer.
7. Fall back to Terraform for Java, Kotlin, unclear language cells, or cases where no Pulumi language fit exists.
8. Confirm the provider is known before loading provider-specific state, naming, identity, or secret conventions.
9. Declare dev/test isolation: separate state or stacks, env-var prefix, secret path, and resource names.
10. Record the IaC decision in the manifest and avoid emitting Terraform and Pulumi for the same non-comparative task.

## Good Triggers

- "Terraform or Pulumi?"
- "pick the IaC tool"
- "Pulumi language is unclear"
- "no IaC preference"
- "what should accb generate for infrastructure?"
- "dev and test stacks"

## Avoid

- defaulting to Terraform when a clear Pulumi language fit exists
- choosing Pulumi without identifying its language
- treating Pulumi-.NET as the neutral cross-cloud default
- generating resource code before dev/test isolation is declared
- mixing Terraform and Pulumi in one normal workload path
