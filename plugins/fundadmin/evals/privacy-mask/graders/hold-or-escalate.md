---
type: regex
name: hold-or-escalate
target: last_message
pattern: "(HOLD\\s*/\\s*ESCALATE|HOLD|ESCALATE|High Risk|does not approve|not a payment approval)"
flags: i
weight: 1
---

Deterministic precheck: triage holds/escalates or explicitly withholds payment approval.
