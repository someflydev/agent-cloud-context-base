import hashlib
import unittest


def classify(message_id, body, delivery_count=1):
    key = hashlib.sha256(message_id.encode("utf-8")).hexdigest()
    team = "billing" if "billing" in body.lower() else "support"
    return {
        "idempotency_key": key,
        "team": team,
        "cosmos_id": f"ticket-{key}",
        "topic": f"team-{team}",
        "dlq_reason": "max-delivery-exceeded" if delivery_count > 5 else "",
    }


class HandlerSmokeTest(unittest.TestCase):
    def test_ticket_routes_to_team_topic(self):
        result = classify("msg-1", "billing dispute")
        self.assertEqual(result["team"], "billing")
        self.assertEqual(result["topic"], "team-billing")


if __name__ == "__main__":
    unittest.main()
