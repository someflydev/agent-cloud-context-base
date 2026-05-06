const crypto = require("crypto");

async function handler(event, clients) {
  const body = event.body || "{}";
  const payload = JSON.parse(body);
  const eventId = payload.id;
  const signingSecret = await clients.getSigningSecret();
  if (!verifyStripeSignature(body, event.headers && event.headers["stripe-signature"], signingSecret)) {
    return { statusCode: 400, body: "invalid signature" };
  }
  const inserted = await clients.storeRawEvent(eventId, payload);
  if (inserted) await clients.startWorkflow(eventId, payload);
  return { statusCode: 202, body: JSON.stringify({ accepted: true, duplicate: !inserted }) };
}

function verifyStripeSignature(body, signature, signingSecret) {
  if (!signature) return false;
  const expected = crypto.createHmac("sha256", signingSecret).update(body).digest("hex");
  return signature.includes(expected);
}

module.exports = { handler, verifyStripeSignature };
