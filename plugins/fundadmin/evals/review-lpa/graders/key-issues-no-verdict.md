---
type: regex
name: key-issues-no-verdict
target: last_message
pattern: "^(?=[\\s\\S]*Key Issues and Asks)(?![\\s\\S]*Executive Summary[\\s\\S]*Key Issues and Asks)(?=[\\s\\S]*\\|[^\\n]*(?:\u00a7|\\bss?\\.\\s?\\d|\\bSections?\\s+\\d)[^\\n]*\\|\\s*\\**(?:push|trade|accept)\\**\\s*\\|)(?=[\\s\\S]*compliance[\\s\\S]{0,120}(?:unavailable|\\bnull\\b|UNKNOWN|not assessed|not scored))(?![\\s\\S]*\\b(?:Overall Recommendation|Recommendation:\\s*\\**\\s*(?:Commit|Decline|Proceed))\\b)(?![\\s\\S]*(?:^|\\n)(?![^\\n]*\\b(?:not|no|nothing|never|none|without|cannot|false)\\b)[^\\n]*(?:market[- ]standard|\\bat market\\b|below market|above market|industry[- ]standard|\\bpercentile\\b))[\\s\\S]+"
flags: i
weight: 2
---

Deterministic check (replaces the LLM judge, which disagreed with itself across runs on equivalent answers): a Key Issues and Asks section before any Executive Summary, with table rows giving a section locator (§, s., ss. or Section before a clause number; 1.3.3's first two host runs wrote "ss.1.1" and were failed for it) and a push/trade/accept stance; compliance reported unavailable; no Commit/Decline/Proceed or Overall Recommendation verdict; and no un-negated market-standard, at/below/above-market, industry-standard or percentile comparison.
