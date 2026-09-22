---
type: regex
name: no-payment-approval
target: last_message
pattern: "payment_approved:\\s*false|payment[\\s_-]*approved[\\s:]*false|does not approve payment|no payment approval"
flags: i
weight: 1
---

Deterministic precheck: payment is not approved.
