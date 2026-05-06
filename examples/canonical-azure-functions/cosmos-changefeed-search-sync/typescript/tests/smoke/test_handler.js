const assert = require("node:assert/strict");
const { syncProduct } = require("../../src/handler.js");

const result = syncProduct({
  id: "sku-1",
  _etag: "etag-1",
  name: "Trail Jacket",
  description: "Water resistant",
  category: "outerwear",
  price: 129
});

assert.equal(result.search_document.id, "sku-1");
assert.equal(result.retry_queue_message.reason, "search-update-failed");
console.log("cosmos changefeed search sync smoke passed");
