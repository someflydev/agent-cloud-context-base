const assert = require("assert");
const { handler } = require("../../src/handler.js");

async function main() {
  const claimed = new Set();
  const flagged = [];
  const clients = {
    claimObjectVersion: async (key) => {
      if (claimed.has(key)) return false;
      claimed.add(key);
      return true;
    },
    detectLabels: async () => [{ Name: "Document" }],
    detectModerationLabels: async () => [{ Name: "Explicit Nudity" }],
    recordDecision: async () => {},
    publishFlagged: async (detail) => flagged.push(detail)
  };
  const event = { Records: [{ s3: { bucket: { name: "images" }, object: { key: "a.jpg", versionId: "v1" } } }] };
  const first = await handler(event, clients);
  const second = await handler(event, clients);
  assert.equal(first.duplicate, false);
  assert.equal(second.duplicate, true);
  assert.equal(claimed.size, 1);
  assert.equal(flagged.length, 1);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
