import { serve } from "@hono/node-server";
import { Hono } from "hono";

const app = new Hono();

app.get("/healthz", (c) => c.json({ ok: true, service: "aca-public-api-private-worker-jobs-typescript" }));
app.get("/readyz", (c) =>
  c.json({ ready: true, checks: ["cosmos", "blob-storage", "service-bus", "key-vault", "managed-identity"] })
);
app.get("/retry", (c) =>
  c.json({ job: "servicebus-batch-retry", trigger: "servicebus", keda_rule: "queueLength >= 5", retried: 0 })
);
app.post("/submit", async (c) => {
  const body = await c.req.json().catch(() => ({} as Record<string, string>));
  const submissionId = body.submission_id ?? "demo-submission";
  return c.json(
    {
      submission_id: submissionId,
      state_container: process.env.COSMOS_CONTAINER ?? "workflow",
      attachment_container: process.env.ATTACHMENT_CONTAINER ?? "attachments",
      work_queue: process.env.SERVICEBUS_QUEUE ?? "accb-dev-aca-work",
      worker_url: process.env.WORKER_URL ?? "http://worker.internal/process",
      scale_signal: "keda-servicebus-queue-depth"
    },
    202
  );
});
app.post("/process", async (c) => {
  const body = await c.req.json().catch(() => ({} as Record<string, string>));
  return c.json({
    accepted: true,
    internal_ingress: true,
    message_id: body.message_id ?? "local-message",
    secret_ref: process.env.API_SECRET_NAME ?? "keyvaultref:api-key"
  });
});

serve({ fetch: app.fetch, port: Number(process.env.PORT ?? 8080) });
