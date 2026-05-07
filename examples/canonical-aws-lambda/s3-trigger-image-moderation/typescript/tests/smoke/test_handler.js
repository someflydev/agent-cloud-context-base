const assert = require("assert");
const { handler } = require("../../src/handler.js");

async function main() {
  const claimed = new Set();
  const flagged = [];
  const result = await handler(event("v1"), {
    claimObjectVersion: async (key) => {
      if (claimed.has(key)) return false;
      claimed.add(key);
      return true;
    },
    detectLabels: async () => [{ Name: "Document" }],
    detectModerationLabels: async () => [{ Name: "Explicit Nudity" }],
    recordDecision: async () => {},
    publishFlagged: async (detail) => flagged.push(detail)
  });
  assert.equal(result.decision, "FLAG");
  assert.equal(claimed.size, 1);
  assert.equal(flagged.length, 1);
}

function event(version) {
  return { Records: [{ s3: { bucket: { name: "images" }, object: { key: "a.jpg", versionId: version } } }] };
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
