---
accb_origin: canonical
accb_source_path: context/validation/archetypes/cloud-iac-only-repo.md
accb_role: validation
accb_version: 1
---

# Cloud IaC Only Repo Validation

The main proof is IaC correctness across dev and test. Validate formatting,
static checks, clean plan or preview, and explicit isolation before applying
anything.

Proof commands should include Terraform or Pulumi format checks, validation,
plan or preview for dev, plan or preview for test, and
`python3 scripts/validate_iac_isolation.py <iac dir>`.

Common failure modes are shared backends, shared Pulumi stacks, provider
defaults that erase environment names, plaintext secrets, and plans that hide
destructive drift. Reference Terraform, Pulumi, secret, and IaC isolation
doctrine.
