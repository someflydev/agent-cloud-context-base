# Azure Miniblue Function Test

Lane: local provider (Lane A). Approximate runtime: 3-6 minutes. Approximate
cost: none when run against miniblue.

## Prerequisites

- `ACCB_RUN_LOCAL_PROVIDER=1`
- Azure Functions Core Tools-compatible host
- .NET SDK and the miniblue local provider bundle

When `ACCB_RUN_LOCAL_PROVIDER=1` is absent, `run.sh` exits 0 and reports the
lane as skipped. The harness shape is intentionally small so derived repos can
drop in function-project-specific test assemblies.
