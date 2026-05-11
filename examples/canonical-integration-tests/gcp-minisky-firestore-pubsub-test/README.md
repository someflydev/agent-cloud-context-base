# GCP Minisky Firestore Pub/Sub Test

Lane: local provider (Lane A). Approximate runtime: 3-6 minutes. Approximate
cost: none when run against minisky.

## Prerequisites

- `ACCB_RUN_LOCAL_PROVIDER=1`
- Docker with the minisky provider bundle
- Python 3 with `pytest` and Functions Framework dependencies

When `ACCB_RUN_LOCAL_PROVIDER=1` is absent, `run.sh` exits 0 and reports the
lane as skipped. In this base repo the lane also reports `skipped` when the
flag is present because no automatable MiniSky emulator contract is checked in.
Derived repos must provide a concrete emulator harness before recording this
lane as passed.
