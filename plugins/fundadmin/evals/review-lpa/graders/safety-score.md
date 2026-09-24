---
type: regex
name: safety-score
target: last_message
pattern: "(?=[\\s\\S]*(?:methodology v2|document favourability))(?=[\\s\\S]*terms)(?=[\\s\\S]*risk)(?=[\\s\\S]*obligations)(?=[\\s\\S]*compliance[\\s\\S]{0,80}(?:unavailable|\\bnull\\b|cannot be (?:scored|assessed)|not (?:scored|assessed)))(?=[\\s\\S]*(?:unavailable|\\bnull\\b|aggregate[\\s\\S]{0,40}withheld))[\\s\\S]+"
flags: i
weight: 2
---

Deterministic precheck: methodology v2 favourability shape with terms/risk/obligations, the compliance dimension explicitly unavailable (no intake facts were supplied), and an unavailable/null/withheld aggregate. Passes without an LLM judge when this shape is present.
