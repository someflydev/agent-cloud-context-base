import unittest

from examples.canonical_azure_functions_import import load_python_handler


handler = load_python_handler(
    "examples/canonical-azure-functions/blob-trigger-receipt-ocr/python/src/handler.py"
)


class ReplayTest(unittest.TestCase):
    def test_blob_name_and_version_are_idempotent(self):
        event = {"name": "receipts/a.pdf", "version": "etag-1", "total": 9.99}
        self.assertEqual(
            handler.process_blob(event)["idempotency_key"],
            handler.process_blob(event)["idempotency_key"],
        )


if __name__ == "__main__":
    unittest.main()

