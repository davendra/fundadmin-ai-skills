---
type: regex
name: catches-issues
target: last_message
pattern: "(?=[\\s\\S]*(?:no (?:preferred return|hurdle)|preferred return[\\s\\S]{0,80}omitted|25%\\s+of\\s+[\\s\\S]{0,60}proceeds))(?=[\\s\\S]*clawback)(?=[\\s\\S]*(?:step[- ]?down|never steps down|management fee))(?=[\\s\\S]*(?:fee offset|offsets?[\\s\\S]{0,60}discretion|discretionary))(?=[\\s\\S]*(?:exten(?:d|sion|sions)|sole discretion|without[\\s\\S]{0,40}(?:LP|Limited Partner) consent|no LP consent))(?=[\\s\\S]*(?:affiliate|advisory committee|LPAC|consultative))(?=[\\s\\S]*(?:key[- ]person|excuse|exclusion right))(?=[\\s\\S]*(?:120[- ]?day|deemed[\\s\\S]{0,40}consent|forfeit|no[- ]cure))[\\s\\S]+"
flags: i
weight: 3
---

Deterministic precheck for the eight flawed-LPA issue themes (carry/no hurdle, weak clawback, no fee step-down, discretionary offsets, unilateral extensions, affiliate/optional LPAC, key-person/excuse gaps (a bare "exclusion", such as an Investment Company Act exclusion, does not count), 120-day deemed consent / no-cure forfeiture). Passes without an LLM judge when all eight theme markers appear in the answer.
