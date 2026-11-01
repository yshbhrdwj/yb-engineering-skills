// Synthetic fixture: confirms a money transfer from the review screen.
// Requirements F1-F4 are in evals/cases.json (case qa-critical-transfer).

export function toCents(amount) {
  return Math.floor(parseFloat(amount) * 100);
}

export function createTransferController(api, makeKey = () => crypto.randomUUID()) {
  let inFlight = null;
  return {
    async confirm({ from, to, amount }) {
      const body = { from, to, amountCents: toCents(amount), idempotencyKey: makeKey() };
      inFlight = api.post("/transfers", body);
      try {
        return await inFlight;
      } finally {
        inFlight = null;
      }
    },
  };
}
