const { handler } = require("../../../src/handler.js");
(async () => {
  const claimed = new Set(); const relayed = [];
  const clients = { claimChange: async k => claimed.has(k) ? false : (claimed.add(k), true), publishRelay: async d => relayed.push(d), markRelayed: async () => {} };
  const event = { id: "chg_lane_a", source: "accb.database", "detail-type": "OrderChanged", detail: { change_id: "chg_lane_a" } };
  await handler(event, clients); await handler(event, clients);
  if (claimed.size !== 1 || relayed.length !== 1) throw new Error("expected one relay side effect");
  console.log("Lane A EventBridge CDC relay passed");
})().catch(err => { console.error(err); process.exit(1); });
