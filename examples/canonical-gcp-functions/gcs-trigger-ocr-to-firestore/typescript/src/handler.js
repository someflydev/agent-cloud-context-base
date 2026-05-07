async function handleGcsObject(event, clients) {
  const started = Date.now();
  const activeClients = clients ?? gcpClients();
  const generation = String(event.data.generation ?? event.data.metageneration ?? "0");
  const eventId = event.id ?? `${event.data.bucket}/${event.data.name}/${generation}`;
  const dedupeKey = `${event.data.bucket}:${event.data.name}:${generation}`;
  const claimed = await activeClients.claimGeneration(dedupeKey, { ...event.data, generation });
  if (!claimed) {
    log(started, eventId, dedupeKey, "DROP", "duplicate object generation");
    return { ok: true, duplicate: true, decision: "DROP" };
  }
  const text = await activeClients.runOcr(event.data.bucket, event.data.name, generation);
  const payload = { ...event.data, generation, text, status: "OCR_COMPLETE" };
  await activeClients.writeMetadata(dedupeKey, payload);
  await activeClients.publishDownstream(payload);
  log(started, eventId, dedupeKey, "ALLOW", "ocr metadata written");
  return { ok: true, duplicate: false, decision: "ALLOW", text };
}
function gcpClients() { throw new Error("GCP clients are bound by deployment; tests inject clients."); }
function log(started, correlationId, dedupeKey, decision, msg) {
  console.log(JSON.stringify({ timestamp: new Date().toISOString(), severity: "INFO", msg, trace_id: process.env.TRACEPARENT ?? "local-trace", request_id: correlationId, correlation_id: correlationId, provider: "gcp", runtime_tier: "function", function_name: process.env.FUNCTION_TARGET ?? "accb-dev-gcp-gcs-ocr-typescript", dedupe_key: dedupeKey, decision, latency_ms: Date.now() - started }));
}
module.exports = { handleGcsObject };
