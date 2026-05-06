const { syncProduct } = require("../../../src/handler.js");

if (!syncProduct({ id: "lane-b-sku", _etag: "real-etag", name: "Pack" }).retry_queue_message) {
  process.exit(1);
}
console.log("lane-b Azure Cosmos search sync probe passed");
