---
type: regex
name: disposition
target: last_message
pattern: "Disposition\\W{0,6}(?:is\\W{0,6})?HOLD"
flags: i
weight: 2
---

Deterministic precheck: with no rules grid, nothing is evaluated and the file is held, however clean it looks.
