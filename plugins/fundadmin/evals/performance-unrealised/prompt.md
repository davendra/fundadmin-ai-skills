---
max_turns: 45
timeout_seconds: 600
allowed_tools: [Skill, Read, Write, Glob, Grep, Bash]
---

Run /fundadmin:fund performance-calc for this synthetic fund. Use the session's isolated working directory as the approved output root and save a source-linked draft if possible. No network, live data or actions outside the test workspace.

Fund: Example Unrealised Fund. All amounts GBP, net of fees/carry. Contribution GBP 100 on 2025-09-21. No distributions. Independently supplied terminal NAV GBP 110 at 2026-09-21; use this NAV once, not as both a cash distribution and an additional remaining value. The supplied total-return benchmark level is 100 on both dates. Currency matches throughout. Calculate Kaplan-Schoar PME at 2026-09-21, DPI, RVPI and TVPI. No peer dataset exists: do not assign quartiles. Two decimal places for display; retain underlying workpapers. Explain which data would be needed if terminal NAV were missing rather than explicitly supplied. Only the requested four metrics are needed.
