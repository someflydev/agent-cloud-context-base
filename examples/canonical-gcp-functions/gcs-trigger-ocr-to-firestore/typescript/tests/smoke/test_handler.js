const assert = require("assert");
const { handleGcsObject } = require("../../src/handler.js");

function clients() {
  const claimed = new Set();
  const metadata = new Map();
  const published = [];
  return {
    metadata,
    published,
    async claimGeneration(key) { if (claimed.has(key)) return false; claimed.add(key); return true; },
    async runOcr(bucket, name, generation) { return `ocr:${bucket}/${name}@${generation}`; },
    async writeMetadata(key, payload) { metadata.set(key, payload); },
    async publishDownstream(payload) { published.push(payload); }
  };
}

(async () => {
  const c = clients();
  const event = { id: "evt-1", data: { bucket: "docs", name: "scan.png", generation: "7" } };
  const first = await handleGcsObject(event, c);
  const second = await handleGcsObject(event, c);
  assert.equal(first.duplicate, false);
  assert.equal(second.duplicate, true);
  assert.equal(c.metadata.get("docs:scan.png:7").status, "OCR_COMPLETE");
  assert.equal(c.published.length, 1);
})();
