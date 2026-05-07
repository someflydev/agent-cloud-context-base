const { handler } = require("../../../src/handler.js");
(async () => {
  const claimed = new Set(); const flagged = [];
  const clients = { claimObjectVersion: async k => claimed.has(k) ? false : (claimed.add(k), true), detectLabels: async () => [{Name:"Document"}], detectModerationLabels: async () => [{Name:"Explicit Nudity"}], recordDecision: async () => {}, publishFlagged: async d => flagged.push(d) };
  const event = { Records: [{ s3: { bucket: { name: "accb-dev-s3mod-images" }, object: { key: "lane-a.jpg", versionId: "v1" } } }] };
  await handler(event, clients); await handler(event, clients);
  if (claimed.size !== 1 || flagged.length !== 1) throw new Error("expected one moderation side effect");
  console.log("Lane A TypeScript S3 moderation passed");
})().catch(err => { console.error(err); process.exit(1); });
