from examples.canonical_azure_functions_import import load_python_handler

handler = load_python_handler(
    "examples/canonical-azure-functions/blob-trigger-receipt-ocr/python/src/handler.py"
)
assert handler.process_blob({"name": "lane-b/receipt.pdf", "version": "real-1"})["event_grid_event"]
print("lane-b Azure blob receipt probe passed")
