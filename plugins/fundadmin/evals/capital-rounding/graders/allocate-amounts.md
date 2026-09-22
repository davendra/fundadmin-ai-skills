---
type: regex
name: allocate-amounts
target: last_message
pattern: "33\\.34[\\s\\S]*?33\\.33[\\s\\S]*?33\\.33[\\s\\S]*?(?:0\\.00|excused|excluded)[\\s\\S]*?(?:100\\.00|sum to GBP 100)"
flags: i
weight: 2
---

Deterministic precheck: eligible-pool allocation table (or prose) shows a=33.34, b=33.33, c=33.33, d zero/excused/excluded, and total 100.00. Passes without an LLM judge when this evidence is present.
