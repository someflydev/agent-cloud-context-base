import unittest

from tests.smoke.test_handler import classify


class ReplayTest(unittest.TestCase):
    def test_message_id_is_idempotent_and_dlq_is_explicit(self):
        self.assertEqual(
            classify("msg-7", "support request")["idempotency_key"],
            classify("msg-7", "support request")["idempotency_key"],
        )
        self.assertEqual(classify("msg-8", "support request", delivery_count=6)["dlq_reason"], "max-delivery-exceeded")


if __name__ == "__main__":
    unittest.main()
