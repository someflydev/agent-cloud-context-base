import crypto from "crypto";

export type Clients = {
  storeRawEvent: (eventId: string, payload: unknown) => Promise<boolean>;
  startWorkflow: (eventId: string, payload: unknown) => Promise<void>;
  getSigningSecret: () => Promise<string>;
};

export async function handler(event: any, clients?: Clients) {
  const started = Date.now();
  const activeClients = clients ?? awsClients();
  const body = event.body ?? "{}";
  const payload = JSON.parse(body);
  const eventId = payload.id;
  const requestId = event.requestContext?.requestId ?? "local-request";
  const signingSecret = await activeClients.getSigningSecret();
  if (!verifyStripeSignature(body, event.headers?.["stripe-signature"], signingSecret)) {
    log(started, requestId, eventId, eventId, "DROP", "invalid stripe signature");
    return { statusCode: 400, body: "invalid signature" };
  }
  const inserted = await activeClients.storeRawEvent(eventId, payload);
  if (inserted) {
    await activeClients.startWorkflow(eventId, payload);
  }
  log(started, requestId, eventId, eventId, inserted ? "ALLOW" : "DROP", inserted ? "accepted" : "duplicate");
  return { statusCode: 202, body: JSON.stringify({ accepted: true, duplicate: !inserted }) };
}

export function verifyStripeSignature(body: string, signature: string | undefined, signingSecret: string): boolean {
  if (!signature) return false;
  const expected = crypto.createHmac("sha256", signingSecret).update(body).digest("hex");
  return signature.includes(expected);
}

function awsClients(): Clients {
  throw new Error("AWS clients are bound in the deployment package; tests inject clients.");
}

function log(started: number, requestId: string, correlationId: string, dedupeKey: string, decision: string, msg: string) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level: "INFO",
    msg,
    trace_id: process.env._X_AMZN_TRACE_ID ?? "local-trace",
    request_id: requestId,
    correlation_id: correlationId,
    provider: "aws",
    runtime_tier: "function",
    function_name: process.env.AWS_LAMBDA_FUNCTION_NAME ?? "accb-dev-stripe-handler",
    dedupe_key: dedupeKey,
    decision,
    latency_ms: Date.now() - started
  }));
}
