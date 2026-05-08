import json
from pathlib import Path


def test_pubsub_fixture_targets_test_environment():
    payload = json.loads(Path("fixtures/pubsub_event.json").read_text(encoding="utf-8"))
    assert payload["message"]["attributes"]["environment"] == "test"
