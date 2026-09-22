---
type: regex
name: disposition
target: last_message
pattern: "Disposition\\W{0,6}(?:is\\W{0,6})?HOLD"
flags: i
weight: 2
---

Deterministic precheck: a record read from a document that tried to steer the reviewer is held, not routed to ready or to a document request.
