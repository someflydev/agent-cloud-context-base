const assert = require("assert");
const crypto = require("crypto");
const { handler } = require("../../src/handler");

function signature(body, secret) {
  return "v1=" + crypto.createHmac("sha256", secret).update(body).digest("hex");
}

(async () => {
  const secret = "whsec_test_secret";
  const body = JSON.stringify({ id: "evt_1", type: "checkout.session.completed" });
  const stored = new Set();
  const enqueued = [];
  const clients = {
    getSigningSecret: async () => secret,
    storeRawEvent: async (eventId) => {
      if (stored.has(eventId)) return false;
      stored.add(eventId);
      return true;
    },
    enqueueFulfillment: async (eventId, payload) => enqueued.push({ eventId, payload })
  };

  const result = await handler({ body, headers: { "stripe-signature": signature(body, secret) } }, clients);

  assert.strictEqual(result.statusCode, 202);
  assert.strictEqual(stored.size, 1);
  assert.strictEqual(enqueued.length, 1);
})();
