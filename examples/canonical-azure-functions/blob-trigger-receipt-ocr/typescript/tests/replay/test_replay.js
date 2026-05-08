const assert = require("node:assert/strict");
const { processBlob } = require("../../src/handler.js");

const event = { name: "receipts/replay.pdf", version: "etag-replay", total: 9.99 };
assert.equal(processBlob(event).idempotency_key, processBlob(event).idempotency_key);
console.log("blob receipt ocr typescript replay passed");
