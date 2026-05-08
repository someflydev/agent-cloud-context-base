const assert = require("node:assert/strict");
const { processBlob } = require("../../../src/handler.js");

const result = processBlob({ name: "lane-a/receipt.pdf", version: "azurite-etag", total: 12.5 });
assert.equal(result.cosmos_document.id, result.idempotency_key);
console.log("lane-a-miniblue blob receipt ocr typescript passed");
