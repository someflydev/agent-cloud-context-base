import crypto from "crypto";

export type Clients = {
  storeRawEvent: (eventId: string, payload: unknown) => Promise<boolean>;
  enqueueFulfillment: (eventId: string, payload: unknown) => Promise<void>;
  getSigningSecret: () => Promise<string>;
};

export async function handler(req: any, clients?: Clients) {
  const started = Date.now();
  const activeClients = clients ?? gcpClients();
  const body = typeof req.body === "string" ? req.body : JSON.stringify(req.body ?? {});
  const payload = JSON.parse(body);
  const eventId = payload.id;
  const signature = req.headers?.["stripe-signature"] ?? req.headers?.["Stripe-Signature"];
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

export function verifyStripeSignature(body: string, signature: string | undefined, signingSecret: string): boolean {
  if (!signature) return false;
  const expected = crypto.createHmac("sha256", signingSecret).update(body).digest("hex");
  return signature.includes(expected);
}

function gcpClients(): Clients {
  throw new Error("GCP clients are bound by deployment; tests inject clients.");
}

function log(started: number, correlationId: string, dedupeKey: string, decision: string, msg: string) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    severity: "INFO",
    msg,
    trace_id: process.env.TRACEPARENT ?? "local-trace",
    request_id: correlationId,
    correlation_id: correlationId,
    provider: "gcp",
    runtime_tier: "function",
    function_name: process.env.FUNCTION_TARGET ?? "accb-dev-gcp-stripe-handler",
    dedupe_key: dedupeKey,
    decision,
    latency_ms: Date.now() - started
  }));
}
