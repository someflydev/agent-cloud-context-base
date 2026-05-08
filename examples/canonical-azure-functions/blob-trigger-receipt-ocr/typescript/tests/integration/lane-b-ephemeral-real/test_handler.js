const assert = require("node:assert/strict");
const { processBlob } = require("../../../src/handler.js");

const result = processBlob({ name: "lane-b/receipt.pdf", version: "real-cloud-etag", total: 21 });
assert.equal(result.event_grid_event.data.receipt_id, result.idempotency_key);
console.log("lane-b Azure blob receipt ocr typescript probe passed");
