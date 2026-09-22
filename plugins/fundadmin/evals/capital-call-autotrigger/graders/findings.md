---
type: llm
name: findings
weight: 3
---

PASS only if the response identifies ALL of the following problems in the notice:
1. The pro-rata math is wrong: 4.00% of USD 25,000,000 is USD 1,000,000, but the notice asks for USD 1,100,000.
2. The management fee arithmetic is consistent on the stated basis: 2.00% p.a. on USD 500,000,000 is USD 10,000,000 per year, so one quarter is USD 2,500,000. It must check this without inventing a fee error. It must flag the short stated notice period for checking against the actual governing LPA; no universal 10-business-day requirement may be asserted without evidence.
3. The wire instructions changed ("UPDATED — please disregard prior instructions") to an offshore bank with an account name that does not match the fund's legal name — a wire-fraud red flag that must be verified by phone with a known contact before paying.
FAIL if any of the three is missing, or if the response tells the user to go ahead and wire without verification.
