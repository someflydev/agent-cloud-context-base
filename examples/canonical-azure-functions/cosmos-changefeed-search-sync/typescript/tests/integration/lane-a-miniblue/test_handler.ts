import assert from "node:assert/strict";
import { syncProduct } from "../../../src/handler";

const result = syncProduct({ id: "lane-a-sku", _etag: "azurite-etag", name: "Hat" });
assert.equal(result.search_document.idempotency_key, result.idempotency_key);
