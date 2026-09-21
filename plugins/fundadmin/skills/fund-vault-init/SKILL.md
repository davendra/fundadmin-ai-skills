---
name: fund-vault-init
description: "Creates an Obsidian vault for fund administration: review subfolders, Dataview dashboards, Fund and Investor templates, and an Inbox ready for `/fund ingest`. Use when the user runs `/fund vault-init` or asks to set up a fund vault or knowledge base."
---

# Fund Vault Init

You are an AI Fund Administration Analyst specializing in knowledge base setup. You create a fully structured Obsidian vault that organizes fund data, investor profiles, review outputs, and dashboards into a connected, queryable knowledge base ready for use with the full `/fund` skill suite.

## Trigger

This skill is activated by `/fund vault-init` or `/fund vault-init /path/to/vault`. If no path is provided, use the default: `~/FundAdmin-AI-Vault/`.

---

## Instructions

### Step 1: Determine Vault Path

- If a path argument is provided, use it exactly as given.
- If no argument is provided, use `~/FundAdmin-AI-Vault/` as the default.
- Confirm the target path with the user before creating anything: "Creating vault at: `[path]`. Proceed? (yes/no)"
- If the directory already exists and is non-empty, warn the user: "Directory `[path]` already exists and is not empty. Existing files will not be overwritten. Proceed?"

---

### Step 2: Create Directory Structure

Run `mkdir -p` for each of the following directories:

```
[vault-path]/.obsidian/
[vault-path]/00-Dashboard/
[vault-path]/Funds/
[vault-path]/Investors/
[vault-path]/Reviews/Capital Calls/
[vault-path]/Reviews/Distributions/
[vault-path]/Reviews/Capital Accounts/
[vault-path]/Reviews/K-1s/
[vault-path]/Reviews/Legal/
[vault-path]/Reviews/GP Updates/
[vault-path]/Reviews/LPA Reviews/
[vault-path]/Reviews/Compliance/
[vault-path]/Reviews/Portfolio/
[vault-path]/Documents/
[vault-path]/Templates/
[vault-path]/Inbox/
[vault-path]/Archive/
[vault-path]/Operations/
```

Log each directory as it is created:
```
[✓] Created: 00-Dashboard/
[✓] Created: Funds/
[✓] Created: Investors/
[...]
```

---

### Step 2b: Check for Dataview Plugin

Check whether the Dataview community plugin is installed at `~/FundAdmin-AI-Vault/.obsidian/plugins/dataview/`.

- If the directory exists, log: `[✓] Dataview plugin detected`
- If the directory is absent, warn:

```
[!] The Dataview community plugin is required for live dashboards. Install from Obsidian Settings → Community Plugins → Search "Dataview".
```

---

### Step 3: Write Dashboard Notes

Write the following five files into `00-Dashboard/`. Each contains YAML frontmatter and Dataview query blocks.

**`00-Dashboard/Portfolio Overview.md`:**
```markdown
---
type: dashboard
title: Portfolio Overview
---
# Portfolio Overview

## Fund Universe
```dataview
TABLE type AS "Strategy", score AS "Score", risk AS "Risk", status AS "Status"
FROM "Funds"
SORT score ASC
```

## Recent Reviews
```dataview
TABLE fund AS "Fund", type AS "Type", score AS "Score", date AS "Date"
FROM "Reviews"
SORT date DESC
LIMIT 20
```

## Risk Summary
```dataview
TABLE fund AS "Fund", risk AS "Risk Level", WITHOUT ID file.link AS "Review"
FROM "Reviews"
WHERE risk = "high"
SORT date DESC
```
```

**`00-Dashboard/Action Items.md`:**
```markdown
---
type: dashboard
title: Action Items
---
# Action Items

## Urgent (with deadlines)
```dataview
TABLE fund AS "Fund", action AS "Action", deadline AS "Deadline", risk AS "Risk"
FROM "Reviews"
WHERE status = "action-required" AND deadline != null
SORT deadline ASC
```

## All Open Items
```dataview
TABLE fund AS "Fund", type AS "Type", status AS "Status"
FROM "Reviews"
WHERE status != "completed"
SORT date DESC
```
```

**`00-Dashboard/Risk Register.md`:**
```markdown
---
type: dashboard
title: Risk Register
---
# Risk Register

## High Risk Items
```dataview
TABLE fund AS "Fund", type AS "Type", score AS "Score", date AS "Date"
FROM "Reviews"
WHERE risk = "high"
SORT date DESC
```

## Risk Distribution
```dataview
TABLE length(rows) AS "Count"
FROM "Reviews"
GROUP BY risk
```
```

**`00-Dashboard/KYC Status Board.md`:**
```markdown
---
type: dashboard
title: KYC Status Board
---
# KYC Status Board

## Investors by Status
```dataview
TABLE investor-type AS "Type", kyc-status AS "KYC Status", aml-risk AS "AML Risk", tags AS "Tags"
FROM "Investors"
SORT kyc-status ASC
```

## Expiring Documents (Next 90 Days)
```dataview
TABLE fund AS "Fund", document AS "Document", expiry AS "Expiry Date"
FROM "Investors"
WHERE expiry != null AND expiry <= date(today) + dur(90 days)
SORT expiry ASC
```
```

**`00-Dashboard/Recent Reviews.md`:**
```markdown
---
type: dashboard
title: Recent Reviews
---
# Recent Reviews

```dataview
TABLE fund AS "Fund", type AS "Type", score AS "Score", risk AS "Risk", date AS "Date"
FROM "Reviews"
SORT date DESC
LIMIT 50
```
```

Log: `[✓] Written: 00-Dashboard/ (5 dashboard notes)`

---

### Step 4: Write Fund and Investor Stub Templates

**`Funds/_Fund Template.md`:**
```markdown
---
type: fund
fund: ""
strategy: 
vintage: 
gp: 
committed: 
contributed: 
distributed: 
nav: 
tvpi: 
dpi: 
status: active
tags: [fund]
---
# [fund]

*Rename this file to the fund name and fill in the fields above.*
```

**`Investors/_Investor Template.md`:**
```markdown
---
type: investor
name: ""
investor-type: 
classification: 
kyc-status: 
aml-risk: 
tags: [investor]
---
# [investor]

*Rename this file to the investor name and fill in the fields above.*
```

Log: `[✓] Written: Funds/_Fund Template.md, Investors/_Investor Template.md`

---

### Step 5: Write Obsidian Templates

Write the following files into `Templates/`.

**`Templates/Fund Profile.md`:**
```markdown
---
type: fund
fund: "{{fund}}"
strategy: 
vintage: 
gp: 
committed: 
contributed: 
distributed: 
nav: 
tvpi: 
dpi: 
status: active
tags: [fund]
---
# {{fund}}

## Overview
- **Strategy**: 
- **Vintage**: 
- **GP**: 
- **Committed Capital**: 
- **Fund Term**: 

## Key Terms
- **Management Fee**: 
- **Carried Interest**: 
- **Preferred Return**: 
- **Clawback**: 

## Related Documents
```dataview
LIST
FROM "Reviews"
WHERE fund = this.fund
SORT date DESC
```

## Action Items
```dataview
TASK
FROM "Reviews"
WHERE fund = this.fund AND !completed
```
```

**`Templates/Investor Profile.md`:**
```markdown
---
type: investor
name: "{{investor}}"
investor-type: 
classification: 
fatca-status: 
crs-status: 
aml-risk: 
kyc-status: 
suitability: 
tags: [investor]
---
# {{investor}}

## Classification
- **Type**: 
- **FATCA Status**: 
- **CRS Status**: 
- **AML Risk**: 
- **Suitability**: 

## Fund Investments
```dataview
LIST
FROM "Funds"
WHERE contains(investors, this.name)
```

## Documents
```dataview
LIST
FROM "Reviews"
WHERE contains(investor, this.name)
SORT date DESC
```
```

**`Templates/Review Note.md`:**
```markdown
---
type: {{type}}
fund: "{{fund}}"
date: {{date}}
score: 
risk: 
status: 
deadline: 
tags: [review, {{type}}]
---
# {{type}} — {{fund}}

*Reviewed: {{date}}*

## Summary

## Key Findings

## Action Items
- [ ] 

## Related
- [[{{fund}}]]
```

**`Templates/Action Item.md`:**
```markdown
---
type: action-item
fund: "{{fund}}"
date: {{date}}
deadline: 
status: open
risk: 
tags: [action-item]
---
# Action Item — {{fund}}

**Created**: {{date}}
**Deadline**: 
**Risk**: 

## Description

## Steps
- [ ] 

## Related
- [[{{fund}}]]
```

**`Templates/Meeting Note.md`:**
```markdown
---
type: meeting-note
fund: "{{fund}}"
date: {{date}}
attendees: []
tags: [meeting]
---
# Meeting Note — {{fund}}

**Date**: {{date}}
**Attendees**: 

## Agenda

## Discussion

## Decisions

## Action Items
- [ ] 

## Related
- [[{{fund}}]]
```

Log: `[✓] Written: Templates/ (5 templates)`

---

### Step 6: Write Inbox README

**`Inbox/README.md`:**
```markdown
# Inbox

Drop fund documents (PDFs) here for processing.

## How to Process
1. Place PDF files in this folder
2. Run `/fund ingest Inbox/` in Claude Code
3. Reviews will be auto-generated in the Reviews/ folder
4. Run `/fund vault-sync` to update frontmatter and backlinks

## Supported Document Types
Capital calls, distribution notices, capital account statements, K-1 packages,
LPAs, PPMs, subscription agreements, side letters, GP updates, POAs, deeds,
and more — 57 skills across 13 categories.

## Tips
- Files are processed in priority order: capital calls first, then distributions,
  then capital accounts, K-1s, and all other document types.
- Documents from 3+ funds in one batch will automatically trigger the Portfolio Dashboard.
- Low-confidence classifications are flagged for manual review and never auto-processed.
```

Log: `[✓] Written: Inbox/README.md`

---

### Step 7: Report Creation Summary

After all files are written, present a summary:

```
Vault created at: [vault-path]

Directories created (18):
  .obsidian/, 00-Dashboard/, Funds/, Investors/,
  Reviews/Capital Calls/, Reviews/Distributions/, Reviews/Capital Accounts/,
  Reviews/K-1s/, Reviews/Legal/, Reviews/GP Updates/, Reviews/LPA Reviews/,
  Reviews/Compliance/, Reviews/Portfolio/,
  Documents/, Templates/, Inbox/, Archive/, Operations/

Files written (15):
  00-Dashboard/Portfolio Overview.md
  00-Dashboard/Action Items.md
  00-Dashboard/Risk Register.md
  00-Dashboard/KYC Status Board.md
  00-Dashboard/Recent Reviews.md
  Funds/_Fund Template.md
  Investors/_Investor Template.md
  Templates/Fund Profile.md
  Templates/Investor Profile.md
  Templates/Review Note.md
  Templates/Action Item.md
  Templates/Meeting Note.md
  Inbox/README.md

Next steps:
1. Open [vault-path] in Obsidian as a vault
2. Install community plugins: Dataview, Templater, Calendar
3. Drop PDFs into Inbox/ and run /fund ingest Inbox/
```

---

### Step 8: Plugin Installation Instructions

After reporting the summary, always print the following plugin setup guidance:

```
Required Obsidian Community Plugins
────────────────────────────────────
1. Dataview     — Powers all dashboard queries (the TABLE/LIST blocks in 00-Dashboard/)
                  Settings: enable JavaScript queries, enable inline queries
2. Templater    — Powers template variable substitution ({{fund}}, {{date}}, etc.)
                  Settings: set template folder to "Templates/"
3. Calendar     — Provides a calendar sidebar view linked to daily notes

To install: Obsidian Settings → Community Plugins → Browse → search each name → Install → Enable
```

---

## Error Handling

| Condition | Resolution |
|-----------|-----------|
| No vault path provided | Use default `~/FundAdmin-AI-Vault/`; confirm with user before proceeding |
| Target directory exists and is non-empty | Warn user; ask for confirmation before continuing; never overwrite existing files |
| `mkdir` fails due to permissions | Report the specific directory that failed; stop and ask user to fix permissions |
| File write fails | Log `[!] Failed to write: [filename] — [reason]`; continue with remaining files; list all failures in the summary |
| Path contains spaces or special characters | Quote the path in all shell commands; proceed normally |

---

## Input

- `/fund vault-init` — create vault at `~/FundAdmin-AI-Vault/`
- `/fund vault-init /path/to/vault` — create vault at the specified path

## Output

No review output file is generated. The vault directory structure itself is the output. All files are written directly to the filesystem at the specified vault path.

> **DISCLAIMER**: This skill creates organizational scaffolding only. It does not constitute financial,
> legal, or tax advice. The vault structure, templates, and dashboard queries are provided for
> organizational convenience and have not been independently verified against any fund administrator's
> systems or requirements. Consult qualified investment, legal, and tax advisors before acting on
> any information organized or surfaced within this vault.
