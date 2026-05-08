# Integration Harness And Arc Docs

PROMPT_32 closed the cross-provider verification surface for accb.

The repository now has five reusable integration harness templates under
`examples/canonical-integration-tests/`: ministack for AWS Lambda, minisky for
GCP Functions, miniblue for Azure Functions, and two gated ephemeral real-cloud
lanes for Pulumi and Terraform.

Parity runners now cover functions, managed containers, Kubernetes, IaC
starters, and scenario profile resolution. The runners assert catalog/registry
alignment, expected layout, structured log fields, tiered verification metadata,
and IaC isolation through `scripts/validate_iac_isolation.py`.

The arc docs now live in `docs/`:

- `docs/iac-isolation-contract.md`
- `docs/provider-parity-matrix.md`
- `docs/functions-arc-overview.md`
- `docs/containers-arc-overview.md`
- `docs/kubernetes-arc-overview.md`

PROMPT_33 completed the final root README wiring, ARCHITECTURE_MAP, and
end-to-end generation smoke coverage.
