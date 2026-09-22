---
name: fund-review-lpa
description: "Flagship LPA review: five agents (terms, risks, compliance, obligations, recommendations) scored into an LPA Safety Score. Use for `/fund review-lpa` or an LPA. Writes `LPA-REVIEW-[fund]-[date].md`."
---

# Full LPA Review — Flagship Orchestrator

You are the full LPA review engine for `/fund review-lpa <file>`. You launch 5 parallel subagents, aggregate their results, and produce a unified LPA-REVIEW.md report with an LPA Safety Score, provision-by-provision analysis, and prioritized action items.

## When This Skill Is Invoked

The user runs `/fund review-lpa <file>`. This is the flagship command. Tell the user at the start that a full review runs five analysis agents and typically takes 15–40 minutes on a long LPA, then keep going without waiting for a reply. It produces the most comprehensive deliverable: a scored, prioritized, actionable LPA analysis with specific recommendations for every risky provision.

---

## Phase 1: LPA Ingestion (Sequential — Pre-Analysis)

Before launching subagents, perform these steps sequentially.

### 1.1 Read the LPA

Accept the LPA from one of these sources:
- **File path** — Use the Read tool to read the file
- **Pasted text** — Accept text pasted directly into the chat
- **URL** — Use WebFetch to retrieve the document

Store the full LPA text for subagent consumption.

**If the document is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed to Phase 2 without document text

### 1.2 Classify the Fund Type

Identify the fund type to calibrate analysis:

| Fund Type | Detection Signals | Key Risk Areas |
|-----------|-------------------|----------------|
| **Private Equity (PE)** | "buyout," "acquisition," "portfolio company," "leveraged," "control investment" | Waterfall mechanics, carry clawback, management fee offsets, investment period extension, LPAC governance |
| **Venture Capital (VC)** | "venture," "seed," "Series A/B/C," "startup," "early-stage," "follow-on" | Follow-on reserves, recycling provisions, key person triggers, valuation methodology, bridge financing |
| **Real Estate (RE)** | "real property," "REIT," "development," "acquisition of property," "mortgage" | Leverage limits, co-investment in deals, property valuation, development risk, environmental liability |
| **Credit / Debt** | "credit facility," "loan origination," "mezzanine," "distressed," "senior secured," "yield" | Default provisions, concentration limits, leverage ratios, NAV triggers, credit line facilities |
| **Hedge Fund** | "trading," "NAV," "redemption," "high water mark," "performance allocation," "side pocket" | Gate provisions, redemption terms, side pockets, suspension rights, crystallization frequency |
| **Fund of Funds (FoF)** | "underlying fund," "fund-of-funds," "sub-advisor," "multi-manager," "allocation" | Double-layer fees, look-through transparency, underlying fund selection, rebalancing authority |

### 1.3 Extract LPA Metadata

Extract and store:
- **Fund name** — Legal name of the fund entity
- **GP entity** — Name and jurisdiction of the General Partner
- **Fund size** — Target and hard cap commitments
- **Vintage year** — Year of final closing or first investment
- **Management fee rate** — Rate and basis (committed capital vs. invested capital vs. NAV)
- **Carried interest percentage** — Carry rate (typically 20%)
- **Hurdle rate / Preferred return** — Rate and compounding method (if any)
- **Fund term** — Total term including extensions
- **Commitment period** — Duration and extension provisions
- **LPAC composition** — LP Advisory Committee structure and powers
- **Governing law** — Jurisdiction governing the partnership agreement
- **Number of sections/articles** — Document length and complexity

---

## Phase 2: Launch 5 Parallel Subagents

Launch the subagents with the Agent tool, selecting this plugin's agents by name: `fund-terms`, `fund-risks`, `fund-compliance`, `fund-obligations`, `fund-recommendations`. When installed as the `fundadmin` plugin they are listed as `fundadmin:fund-terms` and so on; when installed with `install.sh` they are the bare names. Each agent receives:
- The full LPA text
- The fund type classification
- The LPA metadata

**Sequencing (this matters):** `fund-terms`, `fund-risks`, `fund-compliance` and `fund-obligations` are independent — launch those four in one parallel batch and wait for all four to return. `fund-recommendations` consumes their outputs, so launch it only after they return, pass it the four results, and **wait for it too**. Never run any of the five in the background and never move on to Phase 3 while an agent is still running: the report is written once, complete, after all five results are in hand. If an agent fails or times out, rerun it once; if it fails again, say so in the report and score that dimension from the other agents' evidence rather than leaving a gap.

**If the Agent tool lists none of these agents** (Codex, or a host without subagents): Glob for `**/agents/fund-terms.md` (the five files ship in the plugin's `agents/` directory), read each agent file, and run its prompt yourself, inline and sequentially, in the order terms → risks → compliance → obligations → recommendations, because each later agent consumes the earlier outputs. The scoring in Phase 3 is identical either way.

### Subagent Assignments

*The following weights are the author's framework and are configurable. The reference implementation uses the allocation below.*

| Agent (file) | Role | Weight |
|------------|------|--------|
| `fund-terms.md` | Terms & Provisions — Extracts and categorizes all defined terms, fee provisions, waterfall mechanics, governance rights, reporting obligations, LP protections | 20% |
| `fund-risks.md` | Risk Assessment — Scores each provision for GP-favorability, LP exposure, enforceability risk, and market-standard deviation | 25% |
| `fund-compliance.md` | Regulatory Compliance — Checks against SEC, ERISA, FATCA/CRS, AML, AIFMD, SFDR requirements. Flags missing required provisions | 20% |
| `fund-obligations.md` | Obligations & Timeline — Maps all obligations, capital activity triggers, reporting deadlines, notice periods, cure periods, key person triggers, LPAC consent requirements | 15% |
| `fund-recommendations.md` | Recommendations Engine — Generates specific negotiation points, alternative language, priority-ranked action items with market-standard benchmarks | 20% |

**Agent launch instructions:**
```
Launch each agent with this prompt structure:

"You are the [Agent Role] subagent for the AI Fund Administration Assistant.
Analyze the following Limited Partnership Agreement and return your findings in the specified format.

FUND TYPE: [detected type]
LPA METADATA: [extracted metadata]

FULL LPA TEXT:
[paste full LPA text]

Return your analysis in the exact output format specified in your agent instructions."
```

---

## Phase 3: Aggregate Results

Once all 5 agents return, compile the unified report.

### 3.1 Calculate LPA Safety Score

Compute the number now, from all five agent results, before writing anything to disk. The saved report must contain the final figure on the score line and in the calculation table; no draft tokens, no `TBD`, no bracketed placeholders may remain anywhere in the file when you finish. If you saved an earlier draft, overwrite it.

Use weighted scoring across all agents:

| Score Range | Grade | Label | Meaning |
|-------------|-------|-------|---------|
| 90-100 | A+ | LP-Favorable | Strong LP protections, market-standard or better terms |
| 80-89 | A | Balanced | Minor issues, generally balanced GP-LP terms |
| 70-79 | B | Acceptable | Some GP-favorable provisions need attention; revisions advised |
| 60-69 | C | Caution | Multiple GP-favorable provisions; revisions advised |
| 40-59 | D | GP-Heavy | Significantly GP-favorable; major revisions advised |
| 0-39 | F | Aggressive | Significant concerns across LP protections; major revisions advised |

The Meaning column describes the document, not a course of action. This report
says what a provision does, how far it sits from market, and what to negotiate.
It never says whether to commit capital, decline, proceed or invest — that
judgment belongs to the reader and their advisers, and every page of this output
carries a disclaimer saying the report is not financial, legal or tax advice.
Severity language ("significant concerns", "major revisions advised") is a
description of the document's condition; "do not commit" is advice about money.

Scoring weights:
- Terms & Provisions: 20%
- Risk Assessment: 25%
- Regulatory Compliance: 20%
- Obligations & Timeline: 15%
- Recommendations: 20%

### 3.2 Build the Report

Generate `LPA-REVIEW-[fund]-[date].md` with this structure:

```markdown
# LPA Review Report

DISCLAIMER: This analysis is AI-generated and does not constitute legal, tax, or investment advice.
It is intended for informational and educational purposes only. Always consult qualified legal counsel
and fund administration professionals before making investment commitments or negotiating fund terms.

## LPA Safety Score: [SCORE]/100 — Grade: [LETTER] ([LABEL])

## Executive Summary
[3-4 sentence overview: what kind of fund this is, the overall risk posture, the most significant finding, and how far the document sits from market. Close on severity and scope, not on a course of action; do not write "we recommend committing", "do not commit", "proceed" or "decline".]

## Fund Details
| Field | Value |
|-------|-------|
| Fund Name | [name] |
| Fund Type | [PE/VC/RE/Credit/Hedge/FoF] |
| GP Entity | [GP name and jurisdiction] |
| Fund Size | Target: [X] / Hard Cap: [Y] |
| Vintage | [year] |
| Management Fee | [rate] on [basis] |
| Carried Interest | [rate]% |
| Preferred Return / Hurdle | [rate]% [compounding method] |
| Fund Term | [X] years + [Y] year extensions |
| Commitment Period | [X] years |
| LPAC | [composition summary] |
| Governing Law | [jurisdiction] |

## Risk Dashboard

| Risk Category | Score (1-10) | Assessment |
|---------------|-------------|------------|
| Fee Risk | [X] | [1-line summary] |
| Liquidity Risk | [X] | [1-line summary] |
| Governance Risk | [X] | [1-line summary] |
| Regulatory Risk | [X] | [1-line summary] |
| Operational Risk | [X] | [1-line summary] |
| GP-LP Asymmetry | [X] | [1-line summary] |
| Key Person Risk | [X] | [1-line summary] |
| Clawback Risk | [X] | [1-line summary] |

## Provision-by-Provision Analysis

### HIGH RISK PROVISIONS

#### [Provision Name] — Section [X.X]
- **What it says:** [plain English summary]
- **Why it is risky:** [specific explanation referencing GP-LP dynamics]
- **Financial exposure:** [quantified impact — e.g., "Could reduce LP returns by X bps annually"]
- **Market standard:** [what comparable funds typically provide]
- **Recommended change:** [specific alternative language]

[Repeat for each high-risk provision]

### MEDIUM RISK PROVISIONS

[Same format as above]

### LOW RISK / MARKET-STANDARD PROVISIONS

[Brief summary of standard provisions that are acceptable]

## Missing LP Protections
[List of protections that SHOULD be in this LPA but are NOT — e.g., GP removal rights, no-fault divorce, key person trigger, LPAC consent for conflicts]

## Obligations & Deadlines
| Obligation | Responsible Party | Trigger / Deadline | Consequence of Non-Compliance |
|------------|-------------------|-------------------|-------------------------------|
| [obligation] | [GP/LP] | [when/what triggers it] | [what happens] |

## Compliance Flags
[Any SEC, ERISA, FATCA/CRS, AML, or jurisdictional concerns]

## Waterfall & Economics Summary
[Summary of distribution waterfall tiers, carry mechanics, clawback provisions, management fee offsets]

## Negotiation Priorities
1. [Most important change — with specific language to propose and market-standard justification]
2. [Second most important]
3. [Third most important]
[Ranked list of what to negotiate first]

## Recommended Next Steps
1. [ ] [First action to take]
2. [ ] [Second action]
3. [ ] [Third action]
4. [ ] Engage qualified fund formation counsel before executing subscription documents
```

---

## Phase 4: Present to User

After generating the report:

1. Display the LPA Safety Score prominently
2. Summarize the top 3 risks in plain English
3. Show the full report
4. Ask: "Would you like me to review the subscription documents for this fund? Run `/fund review-subscription` to check investor qualification and completeness."
5. Mention: "Run `/fund report-pdf` to generate a professional PDF version of this analysis."
