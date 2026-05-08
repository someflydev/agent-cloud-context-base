const assert = require("node:assert/strict");
const { processBlob } = require("../../src/handler.js");

const result = processBlob({
  name: "receipts/r-1.pdf",
  version: "etag-1",
  merchant: "Contoso",
  total: 19.95
});

assert.equal(result.cosmos_document.blob_name, "receipts/r-1.pdf");
assert.equal(result.event_grid_event.eventType, "accb.receipt.ocr.completed");
console.log("blob receipt ocr typescript smoke passed");
