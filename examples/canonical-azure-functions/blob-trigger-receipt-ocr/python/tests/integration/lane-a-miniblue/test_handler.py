import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[6]
sys.path.insert(0, str(root))

from examples.canonical_azure_functions_import import load_python_handler

handler = load_python_handler(
    "examples/canonical-azure-functions/blob-trigger-receipt-ocr/python/src/handler.py"
)
result = handler.process_blob({"name": "lane-a/receipt.pdf", "version": "azurite-1", "total": 12.5})
assert result["cosmos_document"]["id"] == result["idempotency_key"]
print("lane-a-miniblue blob receipt passed")
