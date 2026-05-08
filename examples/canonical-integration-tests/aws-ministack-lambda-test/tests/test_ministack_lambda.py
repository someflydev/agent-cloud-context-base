from pathlib import Path


def test_fixture_declares_test_bucket():
    text = Path("fixtures/s3_event.json").read_text(encoding="utf-8")
    assert "accb-test-images-test" in text
