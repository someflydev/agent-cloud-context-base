const assert = require("assert");
const { handleGcsObject } = require("../../../src/handler.js");
(async () => {
  const claimed = new Set();
  const published = [];
  const clients = {
    async claimGeneration(key) { if (claimed.has(key)) return false; claimed.add(key); return true; },
    async runOcr(bucket, name, generation) { return `ocr:${bucket}/${name}@${generation}`; },
    async writeMetadata() {},
    async publishDownstream(payload) { published.push(payload); }
  };
  const result = await handleGcsObject({ id: "evt-lane", data: { bucket: "docs", name: "scan.png", generation: "8" } }, clients);
  assert.equal(result.duplicate, false);
  assert.equal(published.length, 1);
})();
