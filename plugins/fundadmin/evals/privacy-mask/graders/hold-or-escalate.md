---
type: regex
name: hold-or-escalate
target: last_message
pattern: "(?:\\bHOLD\\b|\\bESCALATE\\b|\\bHigh Risk\\b|does not approve|not a payment approval)"
flags: i
weight: 1
---

Deterministic precheck: triage holds/escalates or explicitly withholds payment approval. Word boundaries stop "holder" or "household" from passing.
