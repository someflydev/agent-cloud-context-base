const assert = require("assert");
const crypto = require("crypto");
const { handler } = require("../../src/handler.js");

async function main() {
  const workflows = [];
  const stored = new Set();
  const body = JSON.stringify({ id: "evt_replay", type: "invoice.paid" });
  const secret = "local-signing-secret";
  const signature = crypto.createHmac("sha256", secret).update(body).digest("hex");
  const clients = {
    getSigningSecret: async () => secret,
    storeRawEvent: async (id) => {
      if (stored.has(id)) return false;
      stored.add(id);
      return true;
    },
    startWorkflow: async (id) => workflows.push(id)
  };
  const event = { body, headers: { "stripe-signature": `v1=${signature}` }, requestContext: { requestId: "req_replay" } };
  const first = await handler(event, clients);
  const second = await handler(event, clients);
  assert.equal(first.statusCode, 202);
  assert.equal(second.statusCode, 202);
  assert.equal(stored.size, 1);
  assert.equal(workflows.length, 1);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
