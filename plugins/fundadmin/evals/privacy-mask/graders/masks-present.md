---
type: regex
name: masks-present
target: last_message
pattern: "\\*{4}\\d{4}"
weight: 1
---

Deterministic precheck: at least one last-four mask (****NNNN) is present.
