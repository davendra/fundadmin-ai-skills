---
type: regex
name: allocate-amounts
target: last_message
pattern: "^(?=[\\s\\S]*\\ba\\b(?:(?!33\\.3[34](?![\\d%]))[^\\n]){0,80}33\\.34(?![\\d%]))(?=[\\s\\S]*\\bb\\b(?:(?!33\\.3[34](?![\\d%]))[^\\n]){0,80}33\\.33(?![\\d%]))(?=[\\s\\S]*\\bc\\b(?:(?!33\\.3[34](?![\\d%]))[^\\n]){0,80}33\\.33(?![\\d%]))(?=[\\s\\S]*(?:0\\.00|excused|excluded))(?=[\\s\\S]*(?:100\\.00|sum to GBP 100))[\\s\\S]+"
flags: i
weight: 2
---

Deterministic precheck, in any order: eligible-pool allocation table (or prose) ties a to 33.34 and b and c to 33.33, shows d zero/excused/excluded, and a total of 100.00. An amount is a 33.33/33.34 figure not followed by another digit or `%`, so a percentage column such as `33.3333%` before the amount is skipped rather than read as the amount. Passes without an LLM judge when this evidence is present.
