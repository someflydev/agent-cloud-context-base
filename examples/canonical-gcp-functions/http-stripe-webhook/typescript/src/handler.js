const crypto = require("crypto");

async function handler(req, clients) {
  const started = Date.now();
  const activeClients = clients || gcpClients();
  const body = typeof req.body === "string" ? req.body : JSON.stringify(req.body || {});
  const payload = JSON.parse(body);
  const eventId = payload.id;
  const signature = (req.headers && (req.headers["stripe-signature"] || req.headers["Stripe-Signature"])) || "";
  const signingSecret = await activeClients.getSigningSecret();
  if (!verifyStripeSignature(body, signature, signingSecret)) {
    log(started, eventId, eventId, "DROP", "invalid stripe signature");
    return { statusCode: 400, body: "invalid signature" };
  }
  const inserted = await activeClients.storeRawEvent(eventId, payload);
  if (inserted) {
    await activeClients.enqueueFulfillment(eventId, payload);
  }
  log(started, eventId, eventId, inserted ? "ALLOW" : "DROP", inserted ? "accepted" : "duplicate");
  return { statusCode: 202, body: JSON.stringify({ accepted: true, duplicate: !inserted }) };
}

function verifyStripeSignature(body, signature, signingSecret) {
  if (!signature) return false;
  const expected = crypto.createHmac("sha256", signingSecret).update(body).digest("hex");
  return signature.includes(expected);
}

function gcpClients() {
  throw new Error("GCP clients are bound by deployment; tests inject clients.");
}

function log(started, correlationId, dedupeKey, decision, msg) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    severity: "INFO",
    msg,
    trace_id: process.env.TRACEPARENT || "local-trace",
    request_id: correlationId,
    correlation_id: correlationId,
    provider: "gcp",
    runtime_tier: "function",
    function_name: process.env.FUNCTION_TARGET || "accb-dev-gcp-stripe-handler",
    dedupe_key: dedupeKey,
    decision,
    latency_ms: Date.now() - started
  }));
}

module.exports = { handler, verifyStripeSignature };
