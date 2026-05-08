import assert from "node:assert/strict";
import { processBlob } from "../../../src/handler";

const result = processBlob({ name: "lane-a/receipt.pdf", version: "azurite-etag", total: 12.5 });
assert.equal(result.cosmos_document.id, result.idempotency_key);
