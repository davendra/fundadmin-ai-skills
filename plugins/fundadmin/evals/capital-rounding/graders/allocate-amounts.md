---
type: regex
name: allocate-amounts
target: last_message
pattern: "^(?=[\\s\\S]*\\ba\\b(?:(?!33\\.3[34])[^\\n]){0,80}33\\.34)(?=[\\s\\S]*\\bb\\b(?:(?!33\\.3[34])[^\\n]){0,80}33\\.33)(?=[\\s\\S]*\\bc\\b(?:(?!33\\.3[34])[^\\n]){0,80}33\\.33)(?=[\\s\\S]*(?:0\\.00|excused|excluded))(?=[\\s\\S]*(?:100\\.00|sum to GBP 100))[\\s\\S]+"
flags: i
weight: 2
---

Deterministic precheck, in any order: eligible-pool allocation table (or prose) ties a to 33.34 and b and c to 33.33, shows d zero/excused/excluded, and a total of 100.00. Passes without an LLM judge when this evidence is present.
