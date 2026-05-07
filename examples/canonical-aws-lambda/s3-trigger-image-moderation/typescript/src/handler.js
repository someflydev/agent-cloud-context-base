"use strict";

async function handler(event, clients) {
  const started = Date.now();
  const record = event.Records[0];
  const bucket = record.s3.bucket.name;
  const object = record.s3.object;
  const version = object.versionId || object.sequencer || "unversioned";
  const dedupeKey = `${bucket}:${object.key}:${version}`;
  const requestId = event.requestContext?.requestId || "local-request";
  const active = clients || awsClients();
  const claimed = await active.claimObjectVersion(dedupeKey, { bucket, key: object.key, version });
  if (!claimed) {
    log(started, requestId, dedupeKey, dedupeKey, "DROP", "duplicate object version");
    return { ok: true, duplicate: true, decision: "DROP" };
  }
  const labels = await active.detectLabels(bucket, object.key);
  const moderation = await active.detectModerationLabels(bucket, object.key);
  const decision = moderation.length > 0 ? "FLAG" : "ALLOW";
  await active.recordDecision(dedupeKey, decision, labels);
  if (decision === "FLAG") {
    await active.publishFlagged({ bucket, key: object.key, version, decision });
  }
  log(started, requestId, dedupeKey, dedupeKey, decision, "moderation complete");
  return { ok: true, duplicate: false, decision };
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
    function_name: process.env.AWS_LAMBDA_FUNCTION_NAME || "accb-dev-s3mod-handler",
    dedupe_key: dedupeKey,
    decision,
    latency_ms: Date.now() - started
  }));
}

module.exports = { handler };
