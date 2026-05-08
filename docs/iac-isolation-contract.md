# IaC Isolation Contract

This is the normative accb contract for separating `dev` and `test` cloud
environments. It applies to Terraform and Pulumi in base and generated repos.

## Why Isolation Matters

Cross-environment contamination is the canonical cloud bug. A test job that
reads a dev secret, writes into a shared bucket, reuses a default profile, or
destroys a shared state key can corrupt data and hide the mistake behind normal
cloud APIs. accb therefore treats isolation as a validation requirement rather
than an operator preference.

Generated repos MUST declare this isolation surface before any cloud resource
is created:

| Surface | Dev | Test |
| --- | --- | --- |
| State | dev backend key or Pulumi stack | test backend key or Pulumi stack |
| Env var prefix | dev-specific prefix | test-specific prefix |
| Secret path | dev-only path | test-only path |
| Resource naming | name includes dev | name includes test |

## Lint Policies

| Rule | Severity | Contract |
| --- | --- | --- |
| `no-default-creds` | error | IaC MUST NOT depend on default local credential profiles. |
| `dev-test-disjoint` | error | Dev and test state, secrets, and names MUST be disjoint. |
| `secret-not-in-source` | error | IaC MUST reference secrets, not contain secret values. |
| `resource-name-env-suffixed` | error | Cloud resource names MUST include an environment signal. |
| `no-checked-in-tfvars-or-pulumi-secrets` | warning | Local tfvars and encrypted Pulumi config SHOULD NOT be checked in. |

Machine-readable policy stubs live in `verification/policies/*.policy.yaml`.
`scripts/validate_iac_isolation.py` is the executable source of enforcement.

## Terraform Conformance Shape

Terraform examples MUST use separate environment trees:

```text
iac/terraform/
  dev/
    backend.tf
    main.tf
    variables.tf
  test/
    backend.tf
    main.tf
    variables.tf
```

Terraform backend keys MUST differ by environment:

| Environment | Backend key example |
| --- | --- |
| dev | `accb/dev/<service>/terraform.tfstate` |
| test | `accb/test/<service>/terraform.tfstate` |

Terraform modules SHOULD be shared through `modules/`, but environment roots
MUST pass their own `environment` value into shared modules. Shared modules MUST
use that value in resource names or tags where the provider supports them.

Terraform examples MUST NOT commit real `terraform.tfvars`. They MAY commit
`.tfvars.example` files that contain placeholders and explicit `dev` or `test`
scope labels.

Terraform resources SHOULD use names shaped like:

```hcl
name = "${var.project}-${var.environment}-${var.component}"
```

Provider aliases MAY be used when a provider needs separate dev/test accounts
or projects. The alias and account/project mapping MUST be documented in the
example README.

## Pulumi Conformance Shape

Pulumi examples MUST use one stack per environment:

```text
Pulumi.yaml
Pulumi.dev.yaml
Pulumi.test.yaml
```

Pulumi code MUST read the stack name through the language-native API and use it
as the environment signal:

| Language | Stack API |
| --- | --- |
| TypeScript | `pulumi.getStack()` |
| Python | `pulumi.get_stack()` |
| Go | `ctx.Stack()` |
| .NET | `Deployment.Instance.StackName` |

Pulumi secret config MUST be stack-scoped. `dev` and `test` stacks MUST NOT
reuse the same secret path, password key, token key, or encrypted config blob.

Pulumi resource names SHOULD use names shaped like:

```text
<project>-<stack>-<component>
```

Pulumi examples MUST NOT commit `pulumi.config.encrypted.yaml` or equivalent
local encrypted config exports. Stack files may contain non-secret placeholders
and secret references.

## Acceptable Deviations

Deviations are rare. A generated repo MAY deviate only when all of the following
are true:

| Requirement | Meaning |
| --- | --- |
| Manifest declaration | The manifest declares the deviation and the affected rule. |
| README explanation | The example or repo README explains why the deviation is legitimate. |
| Bounded blast radius | The shared resource cannot mutate cross-env data or credentials. |
| Validation allowance | The operator passes a specific `--allow <rule>:<reason>` value. |

Acceptable examples include read-only public datasets, shared container image
registries with immutable tags, or centrally managed observability sinks that
receive environment-labeled telemetry.

Unacceptable examples include shared state backends, shared databases, shared
queues, shared secret paths, default credentials, or resource names that cannot
be attributed to one environment.

## Verification Commands

Run an individual IaC tree:

```bash
python3 scripts/validate_iac_isolation.py examples/canonical-iac-terraform/aws
```

Run the fast repository contract checks:

```bash
python3 scripts/run_verification.py --tier fast
```

Run all medium parity checks:

```bash
python3 scripts/run_verification.py --tier medium
```

Update a local-provider lane only when explicitly requested:

```bash
ACCB_RUN_LOCAL_PROVIDER=1 python3 scripts/run_verification.py --tier local-provider --update-registry
```

Real-cloud lanes MUST be operator-approved and credentialed:

```bash
ACCB_RUN_REAL_CLOUD=1 python3 scripts/run_verification.py --tier real-cloud --update-registry
```

If credentials or approval are absent, optional lanes MUST record `skipped`
with a short reason. They MUST NOT record `passed`.
