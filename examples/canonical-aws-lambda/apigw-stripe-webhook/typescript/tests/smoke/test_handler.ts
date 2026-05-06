import assert from "assert";
import crypto from "crypto";
import { handler } from "../../src/handler";

async function main() {
  const started: string[] = [];
  const seen = new Set<string>();
  const body = JSON.stringify({ id: "evt_1", type: "checkout.session.completed" });
  const secret = "local-signing-secret";
  const signature = crypto.createHmac("sha256", secret).update(body).digest("hex");
  const result = await handler({ body, headers: { "stripe-signature": `v1=${signature}` }, requestContext: { requestId: "req_1" } }, {
    getSigningSecret: async () => secret,
    storeRawEvent: async (id) => {
      if (seen.has(id)) return false;
      seen.add(id);
      return true;
    },
    startWorkflow: async (id) => {
      started.push(id);
    }
  });
  assert.equal(result.statusCode, 202);
  assert.equal(seen.size, 1);
  assert.deepEqual(started, ["evt_1"]);
}

void main();
