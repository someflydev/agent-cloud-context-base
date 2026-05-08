import hashlib
import unittest


def process_blob(name, version="noversion", merchant="unknown", total=0):
    key = hashlib.sha256(f"{name}:{version}".encode("utf-8")).hexdigest()
    return {
        "idempotency_key": key,
        "cosmos_document": {
            "id": key,
            "blob_name": name,
            "blob_version": version,
            "merchant": merchant,
            "total": total,
            "currency": "USD",
            "ocr_status": "completed",
        },
        "event_grid_event": {
            "eventType": "accb.receipt.ocr.completed",
            "subject": name,
            "data": {"receipt_id": key, "blob_version": version},
        },
    }


class HandlerSmokeTest(unittest.TestCase):
    def test_receipt_blob_maps_to_cosmos_and_event_grid(self):
        result = process_blob("receipts/r-1.pdf", "etag-1", "Contoso", 19.95)
        self.assertEqual(result["cosmos_document"]["merchant"], "Contoso")
        self.assertEqual(result["event_grid_event"]["eventType"], "accb.receipt.ocr.completed")


if __name__ == "__main__":
    unittest.main()
