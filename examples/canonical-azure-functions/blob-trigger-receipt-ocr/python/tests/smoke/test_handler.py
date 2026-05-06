import unittest

from examples.canonical_azure_functions_import import load_python_handler


handler = load_python_handler(
    "examples/canonical-azure-functions/blob-trigger-receipt-ocr/python/src/handler.py"
)


class HandlerSmokeTest(unittest.TestCase):
    def test_receipt_blob_maps_to_cosmos_and_event_grid(self):
        result = handler.process_blob(
            {
                "name": "receipts/2026/05/06/r-1.pdf",
                "version": "v1",
                "content_type": "application/pdf",
                "bytes_len": 512,
                "merchant": "Contoso Market",
                "total": 42.37,
            }
        )
        self.assertEqual(result["cosmos_document"]["merchant"], "Contoso Market")
        self.assertEqual(result["event_grid_event"]["eventType"], "accb.receipt.ocr.completed")


if __name__ == "__main__":
    unittest.main()

