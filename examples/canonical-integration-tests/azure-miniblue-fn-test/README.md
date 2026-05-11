# Azure Miniblue Function Test

Lane: local provider (Lane A). Approximate runtime: 3-6 minutes. Approximate
cost: none when run against miniblue.

## Prerequisites

- `ACCB_RUN_LOCAL_PROVIDER=1`
- Azure Functions Core Tools-compatible host
- .NET SDK and the miniblue local provider bundle

When `ACCB_RUN_LOCAL_PROVIDER=1` is absent, `run.sh` exits 0 and reports the
lane as skipped. In this base repo the lane also reports `skipped` when the
flag is present because no automatable MiniBlue provider contract is checked
in. Derived repos must provide a concrete Functions test harness before
recording this lane as passed.
