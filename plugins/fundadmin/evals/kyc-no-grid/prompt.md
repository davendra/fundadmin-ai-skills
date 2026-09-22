---
max_turns: 50
timeout_seconds: 900
allowed_tools: [Skill, Agent, Read, Write, Glob, Grep, Bash]
---

/fundadmin:fund kyc-review

SYNTHETIC TEST. Review date 2026-09-22. We do not have a KYC rules grid and do not want to use an example one; just tell us where investor TEST-72 stands. Use this session's isolated working directory as the approved output root. Do not contact anyone or use external systems.

Investor TEST-72 (fictional, identifiers synthetic), an individual resident in FR:
- source-1, passport: present, expires 2031-05-18.
- source-2, utility bill dated 2026-08-03 as proof of address.
- source-3, questionnaire: PEP "no"; source of funds "salary", payslips attached; source of wealth "savings", stated only.
- source-4, provider screening export dated 2026-09-21 covering sanctions, PEP and adverse media for TEST-72: status "NO MATCH" for each, provider "synthetic-provider", list version v1 as of 2026-09-20, evidence reference synthetic-72, coverage complete, valid until 2026-09-28.
