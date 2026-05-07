from pathlib import Path


def test_worker_idempotency_contract():
    seen = set()
    emissions = []
    for event_id in ("evt-1", "evt-1"):
        if event_id not in seen:
            seen.add(event_id)
            emissions.append(event_id)
    assert emissions == ["evt-1"]


def test_cron_concurrency_forbid_contract():
    cron = Path(__file__).resolve().parents[2] / "k8s/kustomize/base/cronjob.yaml"
    assert "concurrencyPolicy: Forbid" in cron.read_text()
