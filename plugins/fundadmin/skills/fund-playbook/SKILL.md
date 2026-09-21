---
name: fund-playbook
description: "Tracks how a firm's LPA terms drift across fund vintages and builds a negotiation playbook of standard positions and red lines. Use when the user runs `/fund playbook`, asks how terms changed between Fund II and Fund III, or shares LPAs from several vintages. Writes TERMS-PLAYBOOK-[date].md."
---

# Fund Terms Playbook Generator

You are the fund terms playbook engine for `/fund playbook <files>`. You accept multiple LPAs across fund vintages from the same firm or GP, analyze how terms have evolved over time, identify the firm's standard positions and negotiation patterns, flag directional drift (GP-favorable vs LP-favorable), and generate a comprehensive negotiation playbook for future fund commitments.

## When This Skill Is Invoked

The user runs `/fund playbook <files>` providing two or more LPA files, prior `/fund review-lpa` outputs, or `/fund extract-terms` outputs across different fund vintages from the same GP or firm.

---

## Phase 1: Document Ingestion

### 1.1 Read the Inputs

Accept multiple inputs from any combination of these sources:
- **File paths** — Use the Read tool to read each file (space-separated or glob pattern)
- **Prior review outputs** — Accept `/fund review-lpa` or `/fund extract-terms` reports
- **Pasted text** — Accept text pasted directly into the chat (prompt user to separate vintages)
- **URLs** — Use WebFetch to retrieve documents

Store all document texts indexed by fund vintage.

**Minimum requirement:** At least 2 fund documents from different vintages. If only 1 is provided:
1. Report that playbook generation requires at least 2 vintages for trend analysis
2. Suggest: "Provide LPAs from at least two fund vintages (e.g., Fund II and Fund III) for meaningful trend analysis."
3. Offer to run `/fund benchmark` instead for single-fund analysis

**If any document is unreadable:**
1. Report the specific file that failed
2. Continue with remaining readable documents
3. Note the gap in the output

### 1.2 Identify Vintages and Ordering

For each document, extract:

| Field | What to Extract |
|-------|-----------------|
| **Fund Name** | Legal name (e.g., "Obrelund Capital Partners Fund III, L.P.") |
| **Fund Number** | Roman numeral or sequence (I, II, III, IV...) |
| **GP Entity** | General Partner name |
| **Management Company** | Manager entity name (if different from GP) |
| **Vintage Year** | Year of final close or first investment |
| **Fund Size** | Total commitments at final close |
| **Strategy** | Sub-strategy (buyout, growth, venture, etc.) |

Order the funds chronologically by vintage year. If vintage years are unclear, order by fund number.

### 1.3 Validate Same-Firm Lineage

Confirm that the documents represent the same firm's fund series:
- GP entity names should be related (same management company or sequential GP entities)
- Fund names should share a common base name (e.g., "Obrelund Capital Partners Fund II" and "Obrelund Capital Partners Fund III")
- If documents appear to be from different firms, warn the user and ask for confirmation before proceeding

---

## Phase 2: Extract Terms Across Vintages

### 2.1 Term Extraction Matrix

For each fund vintage, extract the following terms. If using prior `/fund review-lpa` or `/fund extract-terms` output, reuse the extracted data directly.

#### Economic Terms

| Term | What to Extract Per Vintage |
|------|---------------------------|
| **Management Fee — Investment Period** | Rate, basis (committed/invested/NAV), payment frequency |
| **Management Fee — Post-Investment Period** | Rate, basis, step-down mechanics |
| **Carried Interest** | Rate, basis (whole-fund vs deal-by-deal), super-carry tiers |
| **Preferred Return** | Rate, compounding method, basis |
| **GP Catch-Up** | Percentage, target allocation, full vs partial |
| **GP Commitment** | Amount, percentage of fund size |
| **Fee Offsets** | Percentage by fee type (transaction, monitoring, director, break-up) |
| **Organizational Expense Cap** | Dollar amount or percentage of commitments |

#### Governance Terms

| Term | What to Extract Per Vintage |
|------|---------------------------|
| **Fund Term** | Total years, extension count and duration, extension approval |
| **Investment Period** | Duration, extension provisions, early termination triggers |
| **Key Person Provision** | Named individuals, trigger mechanism, cure period |
| **GP Clawback** | Trigger, scope (gross/net), escrow percentage, timing |
| **LPAC** | Composition, powers, consent requirements |
| **No-Fault Removal** | Availability, vote threshold, consequences |
| **No-Fault Dissolution** | Availability, vote threshold |
| **Excuse / Exclusion** | Scope, triggers, process |
| **LP Transfer Rights** | Restrictions, GP consent, transfer fee |
| **Recycling** | Permitted percentage, conditions, time limits |

#### Side Letter Standard Positions

If side letters are available for any vintage:

| Position | What to Extract |
|----------|-----------------|
| **Fee Discounts** | Standard discount offered, eligibility threshold |
| **Co-Investment Rights** | Priority allocation, pro-rata vs discretionary |
| **Reporting Enhancements** | Additional reporting commitments |
| **MFN Rights** | Breadth of MFN election |
| **LPAC Seat** | Commitment threshold for LPAC seat |
| **Excuse Rights** | Standard excuse provisions |
| **Transparency** | Portfolio company information access |

---

### Vintage Year Filtering

When analyzing term evolution across fund vintages:
- Group terms by vintage year (Fund I, Fund II, Fund III, etc.)
- Show trend direction: tightening (LP-favorable) vs loosening (GP-favorable)
- Highlight "red lines" — terms that never changed (firm's non-negotiable positions)
- Include market context: were changes driven by market shifts or LP pressure?

## Phase 3: Analyze Term Evolution

### 3.1 Trend Analysis Per Term

For each term, analyze the evolution across vintages:

| Analysis | How to Assess |
|----------|--------------|
| **Direction** | Increasing, decreasing, stable, or volatile |
| **Magnitude** | Size of change between vintages (bps, percentage points, dollar amounts) |
| **Acceleration** | Is the change accelerating, decelerating, or linear? |
| **Market Context** | Is the change consistent with broader market trends, or firm-specific? |

Classification of trends:

| Trend | Definition | Example |
|-------|-----------|---------|
| **Consistently GP-Favorable Drift** | Each vintage moves terms in GP's favor | Mgmt fee: 1.5% -> 1.75% -> 2.0% |
| **Consistently LP-Favorable Drift** | Each vintage moves terms in LP's favor | Clawback: no escrow -> 20% escrow -> 30% escrow |
| **Stable** | Terms remain unchanged across vintages | Carry at 20% across all funds |
| **Volatile** | Terms move in different directions across vintages | Pref return: 8% -> 6% -> 8% |
| **Step Change** | One vintage has a material change that persists | Key person clause added in Fund III, maintained in Fund IV |
| **New Addition** | Term first appears in a later vintage | LPAC added starting in Fund II |
| **Removed** | Term present in earlier vintage but dropped | No-fault removal present in Fund I, absent from Fund II onward |

### 3.2 Key Person Evolution

Specific analysis for key person provisions:
- Track named individuals across vintages
- Note additions and departures
- Flag if key persons have changed significantly (succession risk)
- Assess whether trigger mechanisms have strengthened or weakened

### 3.3 LPAC Evolution

Track LPAC composition and powers:
- Number of seats and composition rules across vintages
- Consent rights: added, removed, or modified
- Conflict resolution role: expanding or contracting
- Valuation oversight: present or absent

### 3.4 Fund Size vs. Term Relationship

Analyze whether term changes correlate with fund size growth:
- Did fees increase as fund size grew? (common pattern)
- Did governance protections weaken as fund size grew? (concerning pattern)
- Did GP commitment percentage decrease as fund size grew? (economically equivalent but optically different)

---

## Phase 4: Generate Negotiation Playbook

### 4.1 Standard Position Identification

For each term, determine the firm's standard position:

| Element | How to Determine |
|---------|-----------------|
| **Floor (LP's best case from this firm)** | The most LP-favorable position this firm has accepted in any vintage |
| **Ceiling (GP's most aggressive)** | The most GP-favorable position this firm has set in any vintage |
| **Current Position** | The most recent vintage's term |
| **Trend Direction** | Where the firm is heading based on trajectory |
| **Market Comparison** | How the current position compares to market median |

### 4.2 Recommended Positions

For each term, generate a negotiation recommendation for the next fund:

| Recommendation Element | Content |
|-----------------------|---------|
| **Target Position** | What the LP should request |
| **Historical Justification** | "In Fund [X] you accepted [term]; we are requesting a return to that standard" |
| **Market Justification** | "Market median for this term is [X]; current position at [Y] exceeds market" |
| **Trend-Based Argument** | "This term has drifted [X] bps GP-favorable across [N] vintages; we request a correction" |
| **Red Line** | The worst position the LP should accept |
| **Concession Value** | Can this term be traded for a higher-priority win? |

### 4.3 Drift Alerts

Flag significant directional drift with severity ratings:

| Severity | Criteria |
|----------|---------|
| **HIGH — Systematic GP Drift** | 3+ terms moving GP-favorable across 2+ vintages; pattern suggests deliberate ratcheting |
| **MEDIUM — Selective GP Drift** | 1-2 terms moving GP-favorable while others stable; may reflect market dynamics or specific negotiation outcome |
| **LOW — Stable or LP-Favorable** | Terms stable or improving for LPs; firm maintaining balanced posture |

---

## Phase 5: Generate Output File

### 5.1 Compile the Playbook

Generate `TERMS-PLAYBOOK-[date].md` with the following structure:

```markdown
# Fund Terms Negotiation Playbook

> **DISCLAIMER**: This playbook is AI-generated and does not constitute legal,
> tax, or investment advice. Historical term analysis is based on the provided
> documents and may not capture all negotiation context, side letter modifications,
> or market conditions at the time of each fund closing. Recommended positions
> are directional and must be reviewed by qualified fund formation counsel.
> Market benchmarks cited are from aggregated industry data and may not reflect
> current conditions.

---

## Firm Overview

| Field | Value |
|-------|-------|
| Firm / GP | [management company or GP name] |
| Fund Series Analyzed | [Fund I, Fund II, Fund III, ...] |
| Vintages Covered | [year range] |
| Fund Sizes | [Fund I: $X, Fund II: $Y, Fund III: $Z] |
| Strategy | [strategy description] |
| Playbook Generated | [date] |
| Number of Vintages | [N] |

---

## Executive Summary

**Overall Drift Assessment:** [HIGH / MEDIUM / LOW] — [1-2 sentence summary]

**Key Findings:**
1. [Most significant trend — e.g., "Management fees have increased 25 bps per vintage"]
2. [Second finding — e.g., "Clawback protections have weakened: escrow reduced from 30% to 20%"]
3. [Third finding — e.g., "Key person provisions strengthened with addition of named CIO in Fund III"]

**Recommended Posture for Next Fund:** [Aggressive / Balanced / Selective]
[1-2 sentences explaining why]

---

## Term Evolution Tables

### Economic Terms Evolution

| Term | Fund I ([year]) | Fund II ([year]) | Fund III ([year]) | Trend | Drift |
|------|----------------|-----------------|------------------|-------|-------|
| Mgmt Fee (IP) | [X]% on [basis] | [X]% on [basis] | [X]% on [basis] | [direction] | [GP/LP/Stable] |
| Mgmt Fee (Post-IP) | [X]% on [basis] | [X]% on [basis] | [X]% on [basis] | [direction] | [GP/LP/Stable] |
| Carried Interest | [X]% | [X]% | [X]% | [direction] | [GP/LP/Stable] |
| Preferred Return | [X]% [method] | [X]% [method] | [X]% [method] | [direction] | [GP/LP/Stable] |
| GP Catch-Up | [X]% | [X]% | [X]% | [direction] | [GP/LP/Stable] |
| GP Commitment | [X]% ($[Y]) | [X]% ($[Y]) | [X]% ($[Y]) | [direction] | [GP/LP/Stable] |
| Fee Offsets | [X]% | [X]% | [X]% | [direction] | [GP/LP/Stable] |
| Org Expense Cap | $[X] | $[X] | $[X] | [direction] | [GP/LP/Stable] |

### Governance Terms Evolution

| Term | Fund I ([year]) | Fund II ([year]) | Fund III ([year]) | Trend | Drift |
|------|----------------|-----------------|------------------|-------|-------|
| Fund Term | [X] yrs + [ext] | [X] yrs + [ext] | [X] yrs + [ext] | [direction] | [GP/LP/Stable] |
| Investment Period | [X] yrs | [X] yrs | [X] yrs | [direction] | [GP/LP/Stable] |
| Key Person | [summary] | [summary] | [summary] | [direction] | [GP/LP/Stable] |
| GP Clawback | [summary] | [summary] | [summary] | [direction] | [GP/LP/Stable] |
| LPAC | [summary] | [summary] | [summary] | [direction] | [GP/LP/Stable] |
| No-Fault Removal | [present/absent] | [present/absent] | [present/absent] | [direction] | [GP/LP/Stable] |
| No-Fault Dissolution | [present/absent] | [present/absent] | [present/absent] | [direction] | [GP/LP/Stable] |
| Excuse/Exclusion | [summary] | [summary] | [summary] | [direction] | [GP/LP/Stable] |
| Recycling | [X]% | [X]% | [X]% | [direction] | [GP/LP/Stable] |

### Key Person Tracking

| Individual | Fund I | Fund II | Fund III | Status |
|-----------|--------|---------|----------|--------|
| [Name 1] | Named | Named | Named | Continuing |
| [Name 2] | Named | Named | Not Named | Departed |
| [Name 3] | — | Named | Named | Added Fund II |
| [Name 4] | — | — | Named | Added Fund III |

### Side Letter Standard Positions (if available)

| Position | Fund I | Fund II | Fund III | Trend |
|----------|--------|---------|----------|-------|
| Standard Fee Discount | [X] bps | [X] bps | [X] bps | [direction] |
| Co-Invest Threshold | $[X]M | $[X]M | $[X]M | [direction] |
| MFN Breadth | [scope] | [scope] | [scope] | [direction] |
| LPAC Seat Threshold | $[X]M | $[X]M | $[X]M | [direction] |

---

## Drift Analysis

### GP-Favorable Drift (Terms Moving Against LPs)

#### [Term Name] — [Severity: HIGH/MEDIUM]
- **Fund I ([year]):** [position]
- **Fund II ([year]):** [position]
- **Fund III ([year]):** [position]
- **Cumulative Drift:** [quantified change — bps, percentage points, or qualitative]
- **Economic Impact:** [estimated annual or fund-life cost to LPs from the drift]
- **Market Context:** [is this consistent with broader market trends or firm-specific?]

[Repeat for each term with GP-favorable drift]

### LP-Favorable Drift (Terms Improving for LPs)

[Same format for terms moving in LP's favor]

### Stable Terms

[Brief list of terms that have remained unchanged — these represent the firm's settled positions]

---

## Negotiation Playbook for Next Fund

### Term-by-Term Recommended Positions

#### [Term Name]
| Element | Detail |
|---------|--------|
| **Firm's Standard Position** | [Most common position across vintages] |
| **Most LP-Favorable (Historical)** | [Best position the firm has accepted] — Fund [X] |
| **Most GP-Favorable (Historical)** | [Worst position from LP perspective] — Fund [X] |
| **Current Position (Latest Fund)** | [Most recent vintage term] |
| **Market Median** | [Current market standard for this fund type] |
| **Recommended Ask** | [What to request, with justification] |
| **Red Line** | [Worst acceptable position] |
| **Historical Precedent Argument** | "In Fund [X] you accepted [term]; we request [similar or improved]" |
| **Concession Priority** | [HIGH — do not concede / MEDIUM — concede partially / LOW — trade freely] |

[Repeat for each major term]

### Priority Ranking

| Priority | Term | Recommended Ask | Likelihood of Acceptance |
|----------|------|----------------|-------------------------|
| 1 (Highest) | [term] | [ask] | [High/Medium/Low] |
| 2 | [term] | [ask] | [High/Medium/Low] |
| 3 | [term] | [ask] | [High/Medium/Low] |
| ... | ... | ... | ... |

### Concession Strategy

| LP Concedes | In Exchange For |
|-------------|-----------------|
| [Low-priority term: accept current position] | [High-priority term: request improvement] |
| [Stable term: acknowledge firm's consistent position] | [Drifting term: request correction] |

---

## Fund Size Correlation Analysis

| Metric | Fund I | Fund II | Fund III | Trend |
|--------|--------|---------|----------|-------|
| Fund Size | $[X] | $[X] | $[X] | [X]% growth |
| Mgmt Fee Revenue (est.) | $[X]M/yr | $[X]M/yr | $[X]M/yr | [X]% growth |
| GP Commitment ($) | $[X]M | $[X]M | $[X]M | [X]% growth |
| GP Commitment (%) | [X]% | [X]% | [X]% | [direction] |

**Observation:** [Analysis of whether terms have moved with fund size growth — e.g.,
"Fee revenue has grown faster than fund size due to rate increases, not just AUM growth"]

---

## Recommended Next Steps

1. [ ] Review playbook with fund formation counsel
2. [ ] Confirm current market benchmarks with placement agent or advisor
3. [ ] Prioritize negotiation points by economic impact
4. [ ] Prepare historical precedent arguments for each priority item
5. [ ] Run `/fund benchmark` on the latest fund for current market comparison
6. [ ] Run `/fund lpa-negotiate` on the latest LPA for detailed counter-proposals
7. [ ] Run `/fund smart-contract-sim` to model waterfall outcomes under proposed changes
```

### 5.2 Present to User

After generating the output:

1. Confirm the file was generated: "Fund terms playbook generated: `TERMS-PLAYBOOK-[date].md`"
2. State the file location (absolute path)
3. State the number of vintages analyzed and fund size trajectory
4. Highlight the overall drift assessment (HIGH/MEDIUM/LOW) with the most significant trend
5. Summarize the top 3 recommended negotiation positions for the next fund
6. Suggest: "Run `/fund benchmark` on the latest vintage for current market positioning. Run `/fund lpa-negotiate` for detailed counter-proposal language."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| Only 1 document provided | Cannot generate trend analysis; suggest `/fund benchmark` for single-fund analysis |
| Documents from different firms | Warn the user; ask for confirmation; proceed with comparison if confirmed (reframe as cross-firm comparison rather than vintage evolution) |
| Documents from same vintage | Cannot generate trend analysis; suggest `/fund compare` for same-vintage comparison |
| Missing terms in some vintages | Mark as "Not Found" in evolution tables; note that absence may itself be a finding |
| Fund type changed across vintages | Note the strategy shift; benchmark each vintage against its applicable fund type |
| Side letters not available | Generate playbook without side letter analysis; note the gap |
| Prior review outputs provided | Accept extracted terms directly; skip re-extraction |
| Vintage order unclear | Ask the user to confirm chronological ordering; default to fund number sequence |
