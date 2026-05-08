from pathlib import Path


def test_tfvars_example_is_test_scoped():
    text = Path("fixtures/test.auto.tfvars.example").read_text(encoding="utf-8")
    assert 'environment = "test"' in text
