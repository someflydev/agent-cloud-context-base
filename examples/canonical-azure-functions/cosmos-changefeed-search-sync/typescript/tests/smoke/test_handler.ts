import assert from "node:assert/strict";
import { syncProduct } from "../../src/handler";

const result = syncProduct({ id: "sku-1", _etag: "etag-1", name: "Trail Jacket" });
assert.equal(result.search_document.id, "sku-1");
