import { serve } from "@hono/node-server";
import { Hono } from "hono";

const app = new Hono();

app.get("/healthz", (c) => c.json({ ok: true, service: "public-api-private-worker-job" }));
app.get("/readyz", (c) => c.json({ ready: true, checks: ["firestore", "gcs", "pubsub", "secret-manager"] }));
app.get("/cleanup", (c) => c.json({ job: "nightly-cleanup", expired_items_removed: 0 }));
app.post("/submit", async (c) => {
  const body = await c.req.json().catch(() => ({} as Record<string, string>));
  const submissionId = body.submission_id ?? "demo-submission";
  return c.json(
    {
      submission_id: submissionId,
      state_document: `workflow/${submissionId}`,
      attachment_bucket: process.env.ATTACHMENT_BUCKET ?? "accb-dev-cloudrun-attachments",
      fanout_topic: process.env.REVIEW_TOPIC ?? "accb-dev-cloudrun-review",
      callback_target: process.env.WORKER_CALLBACK_URL ?? "http://127.0.0.1:8080/callback"
    },
    202
  );
});
app.post("/callback", (c) =>
  c.json({
    accepted: true,
    iam_audience: process.env.CALLBACK_AUDIENCE ?? "private-worker"
  })
);

serve({ fetch: app.fetch, port: Number(process.env.PORT ?? 8080) });
