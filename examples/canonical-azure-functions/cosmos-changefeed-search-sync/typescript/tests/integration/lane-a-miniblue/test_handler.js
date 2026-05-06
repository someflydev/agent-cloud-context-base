const assert = require("node:assert/strict");
const { syncProduct } = require("../../../src/handler.js");

const result = syncProduct({ id: "lane-a-sku", _etag: "azurite-etag", name: "Hat" });
assert.equal(result.search_document.idempotency_key, result.idempotency_key);
console.log("lane-a-miniblue cosmos search sync passed");
