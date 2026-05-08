import assert from "node:assert/strict";
import { processBlob } from "../../src/handler";

const event = { name: "receipts/replay.pdf", version: "etag-replay", total: 9.99 };
assert.equal(processBlob(event).idempotency_key, processBlob(event).idempotency_key);
