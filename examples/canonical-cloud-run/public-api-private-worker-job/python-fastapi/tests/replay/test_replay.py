import pathlib
import sys
import unittest


example = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(example / "src"))

import main


class ReplayTest(unittest.TestCase):
    def test_submission_id_is_stable_dedupe_key(self):
        first = main.submit({"submission_id": "same"})
        second = main.submit({"submission_id": "same"})
        self.assertEqual(first["state_document"], second["state_document"])


if __name__ == "__main__":
    unittest.main()
