import assert from "node:assert/strict";
import { processBlob } from "../../src/handler";

const result = processBlob({ name: "receipts/r-1.pdf", version: "etag-1", merchant: "Contoso", total: 19.95 });
assert.equal(result.cosmos_document.blob_name, "receipts/r-1.pdf");
