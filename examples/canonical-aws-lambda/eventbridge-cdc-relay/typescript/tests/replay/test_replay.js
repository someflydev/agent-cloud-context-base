const assert = require("assert");
const { handler } = require("../../src/handler.js");

async function main() {
  const claimed = new Set();
  const relayed = [];
  const active = clients(claimed, relayed);
  const first = await handler(event("chg_replay"), active);
  const second = await handler(event("chg_replay"), active);
  assert.equal(first.relayed, true);
  assert.equal(second.duplicate, true);
  assert.equal(claimed.size, 1);
  assert.equal(relayed.length, 1);
}

function clients(claimed, relayed) {
  return {
    claimChange: async (key) => {
      if (claimed.has(key)) return false;
      claimed.add(key);
      return true;
    },
    publishRelay: async (detail) => relayed.push(detail),
    markRelayed: async () => {}
  };
}

function event(id) {
  return { id, source: "accb.database", "detail-type": "OrderChanged", detail: { table: "orders", op: "INSERT", change_id: id } };
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
