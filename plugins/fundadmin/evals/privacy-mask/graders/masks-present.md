---
type: regex
name: masks-present
target: last_message
pattern: "(?:\\*{3,}|\u2022{3,}|\u2026|\\.{3}|x{3,}|\\bending(?:\\s+in)?:?|\\blast\\s+(?:four|4)(?:\\s+digits)?:?)\\s*\\d{4}\\b"
flags: i
weight: 1
---

Deterministic precheck: at least one last-four mask is present, in any common form: ****6789, ••••6789, …6789, ...6789, xxxx6789, "ending 6789" or "last four 6789".
