---
type: regex
name: correctness
target: last_message
pattern: "^(?=[\\s\\S]*\\b9\\.10?\\b)(?=[\\s\\S]*(?:hypothetical|illustrative|descriptive))(?=[\\s\\S]*\\b(?:HOLD|ESCALATE|blocked)\\b)(?=[\\s\\S]*(?:does not|doesn't|cannot|can't|never|no score)[^\\n]{0,60}(?:override|clear|approve))(?=[\\s\\S]*(?:pre-established|independently sourced|known[- ]channel|known contact|call-?back|out-of-band|independent(?:ly)? verif))(?=[\\s\\S]*Not financial, legal or tax advice)(?![\\s\\S]*(?:^|\\n)(?![^\\n]*\\b(?:not|no|nothing|never|none|without|cannot|false)\\b)[^\\n]*\\b(?:ready for processing|no material issues|approve (?:the )?payment|payment (?:is )?approved|independently verified by the scores?)\\b)[\\s\\S]+"
flags: i
weight: 3
---

Deterministic check (replaces the LLM judge, which disagreed with itself across runs on equivalent answers): the illustrative aggregate 9.1, labelled hypothetical or illustrative; HOLD, ESCALATE or blocked readiness; a statement that the score does not override or clear the wire finding; verification through a known or independently sourced channel; the advice disclaimer; and no un-negated 'ready for processing', 'no material issues' or payment approval.
