import unittest

from tests.smoke.test_handler import process_blob


class ReplayTest(unittest.TestCase):
    def test_blob_name_and_version_are_idempotent(self):
        event = ("receipts/replay.pdf", "etag-replay")
        self.assertEqual(
            process_blob(*event)["idempotency_key"],
            process_blob(*event)["idempotency_key"],
        )


if __name__ == "__main__":
    unittest.main()
