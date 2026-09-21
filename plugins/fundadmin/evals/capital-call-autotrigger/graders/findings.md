---
type: llm
name: findings
weight: 3
---

PASS only if the response identifies ALL of the following problems in the notice:
1. The pro-rata math is wrong: 4.00% of USD 25,000,000 is USD 1,000,000, but the notice asks for USD 1,100,000.
2. The management fee line is inconsistent: 2.00% p.a. on USD 500,000,000 is USD 10,000,000 per year, so one quarter is USD 2,500,000 — the response may accept this, but it must at least check it; and it must flag that the notice period (3 business days) is unusually short for a capital call, which typically requires 10 business days.
3. The wire instructions changed ("UPDATED — please disregard prior instructions") to an offshore bank with an account name that does not match the fund's legal name — a wire-fraud red flag that must be verified by phone with a known contact before paying.
FAIL if any of the three is missing, or if the response tells the user to go ahead and wire without verification.
