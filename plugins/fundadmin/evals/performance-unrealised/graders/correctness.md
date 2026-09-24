---
type: regex
name: correctness
target: last_message
pattern: "^(?=[\\s\\S]*PME[^\\n]{0,120}\\b1\\.10?\\b)(?=[\\s\\S]*\\bDPI\\b[^\\n]{0,60}\\b0(?:\\.00)?x?\\b)(?=[\\s\\S]*\\bRVPI\\b[^\\n]{0,60}\\b1\\.10?x?\\b)(?=[\\s\\S]*\\bTVPI\\b[^\\n]{0,60}\\b1\\.10?x?\\b)(?=[\\s\\S]*(?:fund_calculations|helper|workpaper))(?=[\\s\\S]*(?:no quartiles?|quartiles?[^\\n]{0,80}(?:unknown|not assigned|none)|no peer))(?=[\\s\\S]*(?:missing|absent)[\\s\\S]{0,400}(?:UNKNOWN|unknown_nav))(?=[\\s\\S]*Not financial, legal or tax advice)(?![\\s\\S]*(?:^|\\n)(?![^\\n]*\\b(?:not|no|nothing|never|none|without|cannot|false)\\b)[^\\n]*\\b(?:top|first|second|third|fourth|bottom|upper|lower)[- ]quartile)[\\s\\S]+"
flags: i
weight: 3
---

Deterministic check (replaces the LLM judge, which disagreed with itself across runs on equivalent answers): PME 1.10, DPI 0.00, RVPI 1.10 and TVPI 1.10 from the packaged helper; no quartile assigned; a missing NAV reported as UNKNOWN rather than zero; the advice disclaimer; and no quartile placement stated without negation.
