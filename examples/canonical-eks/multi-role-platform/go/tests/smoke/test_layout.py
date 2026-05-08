from pathlib import Path

root = Path(__file__).resolve().parents[2]
roles = ("api", "worker", "job", "cronjob")
for role in roles:
    assert (root / "containers" / f"{role}.Dockerfile").exists()
    assert (root / "src" / role).is_dir()
assert "concurrencyPolicy: Forbid" in (root / "k8s/kustomize/base/cronjob.yaml").read_text()
print("layout ok")
