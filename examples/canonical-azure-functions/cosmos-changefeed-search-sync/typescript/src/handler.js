const crypto = require("node:crypto");

function syncProduct(change) {
  const idempotencyKey = crypto.createHash("sha256").update(change._etag).digest("hex");
  const searchDocument = {
    id: change.id,
    name: change.name,
    text: [change.name, change.description || "", change.category || ""].join(" ").trim(),
    category: change.category || "uncategorized",
    price: change.price || 0,
    idempotency_key: idempotencyKey
  };
  return {
    idempotency_key: idempotencyKey,
    search_document: searchDocument,
    retry_queue_message: {
      product_id: change.id,
      etag: change._etag,
      reason: "search-update-failed"
    },
    log: {
      provider: "azure",
      service: "azure-functions",
      example: "cosmos-changefeed-search-sync",
      idempotency_key: idempotencyKey
    }
  };
}

module.exports = { syncProduct };
