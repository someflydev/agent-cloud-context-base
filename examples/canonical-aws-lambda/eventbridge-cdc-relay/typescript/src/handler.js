"use strict";

async function handler(event, clients) {
  const started = Date.now();
  const active = clients || awsClients();
  const correlationId = event.id || event.detail?.change_id || "local-change";
  const dedupeKey = `${event.source || "unknown"}:${correlationId}`;
  const requestId = event.requestContext?.requestId || correlationId;
  const claimed = await active.claimChange(dedupeKey, event.detail || {});
  if (!claimed) {
    log(started, requestId, correlationId, dedupeKey, "DROP", "duplicate change");
    return { ok: true, duplicate: true, relayed: false };
  }
  await active.publishRelay({ source: event.source, detailType: event["detail-type"], detail: event.detail || {}, dedupeKey });
  await active.markRelayed(dedupeKey);
  log(started, requestId, correlationId, dedupeKey, "ALLOW", "change relayed");
  return { ok: true, duplicate: false, relayed: true };
}

function awsClients() {
  throw new Error("AWS clients are bound in the deployment package; tests inject clients.");
}

function log(started, requestId, correlationId, dedupeKey, decision, msg) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level: "INFO",
    msg,
    trace_id: process.env._X_AMZN_TRACE_ID || "local-trace",
    request_id: requestId,
    correlation_id: correlationId,
    provider: "aws",
    runtime_tier: "function",
    function_name: process.env.AWS_LAMBDA_FUNCTION_NAME || "accb-dev-cdc-handler",
    dedupe_key: dedupeKey,
    decision,
    latency_ms: Date.now() - started
  }));
}

module.exports = { handler };
