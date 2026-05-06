import assert from "node:assert/strict";
import { syncProduct } from "../../src/handler";

const change = { id: "sku-2", _etag: "etag-replay", name: "Boot" };
assert.equal(syncProduct(change).idempotency_key, syncProduct(change).idempotency_key);
