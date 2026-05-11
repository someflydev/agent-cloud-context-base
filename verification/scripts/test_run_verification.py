import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import run_verification  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


class RunVerificationTests(unittest.TestCase):
    def test_fast_tier_passes(self):
        result = subprocess.run(
            ["python3", "scripts/run_verification.py", "--tier", "fast"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_help(self):
        result = subprocess.run(
            ["python3", "scripts/run_verification.py", "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)

    def test_skipped_output_is_not_passed(self):
        result = subprocess.CompletedProcess(["example"], 0, stdout="skipped: missing emulator\n", stderr="")
        status, reason = run_verification.command_result_status(result)
        self.assertEqual(status, "skipped")
        self.assertEqual(reason, "missing emulator")

    def test_failed_registry_update_records_failed_lane_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.yaml"
            registry.write_text(
                yaml.safe_dump(
                    {
                        "schema_version": 1,
                        "families": [
                            {
                                "name": "canonical-test",
                                "examples": [
                                    {"name": "ok", "language": "python", "verification": {}},
                                    {"name": "bad", "language": "python", "verification": {}},
                                ],
                            }
                        ],
                    },
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            run_verification.update_registry(
                registry,
                {
                    "canonical-test|bad|python": {
                        "tier": "local_provider",
                        "status": "failed",
                        "command": "bash bad.sh",
                        "reason": "local provider harness failed",
                    }
                },
            )
            data = yaml.safe_load(registry.read_text(encoding="utf-8"))
            examples = {entry["name"]: entry for entry in data["families"][0]["examples"]}
            self.assertNotIn("local_provider", examples["ok"].get("verification", {}))
            self.assertEqual(examples["bad"]["verification"]["local_provider"]["status"], "failed")
            self.assertEqual(examples["bad"]["last_verified_status"], "failed")

    def test_real_cloud_missing_credentials_skips_provider(self):
        entry = {"provider": "gcp"}
        with mock.patch.dict(run_verification.os.environ, {"ACCB_RUN_REAL_CLOUD": "1"}, clear=True):
            self.assertEqual(run_verification.real_cloud_skip_reason(entry), "gcp cloud credentials not detected")

    def test_real_cloud_with_provider_credentials_can_run(self):
        entry = {"provider": "aws"}
        with mock.patch.dict(
            run_verification.os.environ,
            {"ACCB_RUN_REAL_CLOUD": "1", "AWS_ACCESS_KEY_ID": "test"},
            clear=True,
        ):
            self.assertIsNone(run_verification.real_cloud_skip_reason(entry))

    def test_executable_harnesses_do_not_contain_placeholder_success_text(self):
        banned = ("placeholder", "would run here")
        harness_roots = [ROOT / "examples/canonical-integration-tests"]
        executable_suffixes = {".py", ".sh"}
        offenders: list[str] = []
        for harness_root in harness_roots:
            for path in harness_root.rglob("*"):
                if path.suffix not in executable_suffixes:
                    continue
                text = path.read_text(encoding="utf-8")
                for token in banned:
                    if token in text:
                        offenders.append(f"{path.relative_to(ROOT)} contains {token!r}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
