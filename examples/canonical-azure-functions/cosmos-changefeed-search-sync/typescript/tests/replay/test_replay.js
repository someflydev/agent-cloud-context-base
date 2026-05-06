const assert = require("node:assert/strict");
const { syncProduct } = require("../../src/handler.js");

const change = { id: "sku-2", _etag: "etag-replay", name: "Boot" };
assert.equal(syncProduct(change).idempotency_key, syncProduct(change).idempotency_key);
console.log("cosmos changefeed search sync replay passed");
