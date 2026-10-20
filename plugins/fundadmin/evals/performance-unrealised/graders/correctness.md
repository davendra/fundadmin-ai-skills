---
type: regex
name: correctness
target: last_message
pattern: "^(?=[\\s\\S]*PME[^\\n]{0,120}\\b1\\.10?\\b)(?=[\\s\\S]*\\bDPI\\b[^\\n]{0,60}\\b0(?:\\.00)?x?\\b)(?=[\\s\\S]*\\bRVPI\\b[^\\n]{0,60}\\b1\\.10?x?\\b)(?=[\\s\\S]*\\bTVPI\\b[^\\n]{0,60}\\b1\\.10?x?\\b)(?=[\\s\\S]*(?:fund_calculations|helper|workpaper))(?=[\\s\\S]*(?:no quartiles?|quartiles?[^\\n]{0,80}(?:unknown|not assigned|none)|no peer))(?=[\\s\\S]*(?:\\b(?:missing|absent|unsupplied)\\b[^\\n.!?]{0,40}\\bNAV\\b|\\bNAV\\b[^\\n.!?]{0,40}\\b(?:missing|absent|unsupplied|not (?:supplied|provided|available))\\b)[\\s\\S]{0,400}(?:\\b(?:NAV|RVPI|TVPI|PME)\\b(?:\\s*(?:,|and|or)\\s*(?:RVPI|TVPI|PME)\\b)*\\s*(?:(?:(?:would|will|must|should)\\s+)?(?:(?:all|both|each)\\s+)?(?:be|is|are|remains?|becomes?|stays?)\\s+(?:(?:all|both|each)\\s+)?)?[:*`|\\s]*\\bUNKNOWN\\b|\\bks_pme\\b\\s+(?:(?:would|will|must|should)\\s+)?returns?\\s+(?:status\\s+)?[`*\\s]*\\bunknown_nav\\b))(?=[\\s\\S]*Not financial, legal or tax advice)(?![\\s\\S]*(?:^|\\n)(?![^\\n]*\\b(?:not|no|nothing|never|none|without|cannot|false)\\b)[^\\n]*\\b(?:top|first|second|third|fourth|bottom|upper|lower)[- ]quartile)[\\s\\S]+"
flags: i
weight: 3
---

Deterministic check (replaces the LLM judge, which disagreed with itself across runs on equivalent answers): PME 1.10, DPI 0.00, RVPI 1.10 and TVPI 1.10 from the packaged helper; no quartile assigned; a missing NAV (worded as missing, absent, unsupplied, not supplied, not provided or not available) reported as UNKNOWN rather than zero; the advice disclaimer; and no quartile placement stated without negation.

The missing-input wording must name NAV. Within the bounded following context, UNKNOWN must be attached to NAV, RVPI, TVPI or PME (or `ks_pme` must return `unknown_nav`); an unrelated peer-ranking UNKNOWN cannot satisfy this check. "All", "both" or "each" may sit beside the verb ("would all be UNKNOWN", "are both UNKNOWN"); 1.3.3's first two host runs were failed on that word alone. This is a deterministic precheck, not a semantic review of every claim.
