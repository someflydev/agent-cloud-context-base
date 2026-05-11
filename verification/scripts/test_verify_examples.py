import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import verify_examples  # noqa: E402


class VerifyExamplesTests(unittest.TestCase):
    def test_empty_registry_passes(self):
        result = subprocess.run(
            ["python3", "scripts/verify_examples.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_help(self):
        result = subprocess.run(
            ["python3", "scripts/verify_examples.py", "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)

    def test_explicit_skip_reason_from_command_output(self):
        self.assertEqual(
            verify_examples.explicit_skip_reason("setup\nskipped: emulator unavailable\n"),
            "emulator unavailable",
        )

    def test_real_cloud_gate_is_provider_specific(self):
        with mock.patch.dict(verify_examples.os.environ, {"ACCB_RUN_REAL_CLOUD": "1"}, clear=True):
            self.assertEqual(
                verify_examples.gated_skip_reason("real-cloud", {"provider": "azure"}),
                "azure cloud credentials not detected",
            )


if __name__ == "__main__":
    unittest.main()
