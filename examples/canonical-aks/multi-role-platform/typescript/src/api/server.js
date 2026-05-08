import { serve } from "@hono/node-server";
import { Hono } from "hono";

const app = new Hono();
app.get("/healthz", (c) => c.json({ status: "ok", env: process.env.ACCB_ENV ?? "dev" }));
app.post("/billing/events", (c) => c.json({ accepted: true, bus: "service-bus" }, 202));

serve({ fetch: app.fetch, port: 8080, hostname: "0.0.0.0" });
