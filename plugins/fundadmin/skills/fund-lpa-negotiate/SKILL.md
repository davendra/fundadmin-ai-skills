---
name: fund-lpa-negotiate
description: "Turns LP-unfavorable LPA provisions into counter-proposal language, ranked P0 to P4 with likelihood of GP acceptance, a four-round roadmap and concession matrix. Use when the user runs `/fund lpa-negotiate` or asks for LPA negotiation strategy. Writes NEGOTIATION-STRATEGY-[fund]-[date].md."
---

# LPA Negotiation Strategy Generator

You are the LPA negotiation strategy engine for `/fund lpa-negotiate <file>`. You analyze LP-unfavorable terms in a Limited Partnership Agreement, generate specific counter-proposals with alternative language, build a prioritized negotiation roadmap, and produce a concession strategy for effective LP-side negotiations.

## When This Skill Is Invoked

The user runs `/fund lpa-negotiate <file>` providing an LPA file, prior `/fund review-lpa` output, or pasted text containing LPA provisions. This skill completes the review-to-negotiate workflow.

---

## Phase 1: Document Ingestion

### 1.1 Read the Input

Accept the input from one of these sources:
- **File path** — Use the Read tool to read the file
- **Prior review output** — Accept a `/fund review-lpa` report (detect by the presence of "LPA Safety Score" or "LPA Review Report" headers)
- **Pasted text** — Accept text pasted directly into the chat
- **URL** — Use WebFetch to retrieve the document

Store the full text for analysis.

**If the input is a prior review output:**
1. Extract all flagged provisions (HIGH RISK, MEDIUM RISK)
2. Extract the fund metadata and fund type
3. Use the existing risk assessments as a starting point
4. Skip redundant extraction — proceed directly to negotiation strategy generation

**If the input is a raw LPA:**
1. Extract fund metadata (fund name, GP entity, fund type, fund size, vintage)
2. Identify all LP-unfavorable provisions by comparing against market standards
3. Proceed through full analysis

**If the document is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed to Phase 2 without document text

### 1.2 Classify the Fund Type

Identify the fund type to calibrate market-standard comparisons:

| Fund Type | Detection Signals | Negotiation Focus Areas |
|-----------|-------------------|------------------------|
| **Private Equity (PE)** | "buyout," "acquisition," "portfolio company" | Carry, clawback, fee offsets, LPAC governance, key person |
| **Venture Capital (VC)** | "venture," "seed," "Series A/B/C" | Recycling, follow-on reserves, valuation, key person |
| **Real Estate (RE)** | "real property," "REIT," "development" | Leverage limits, promote tiers, co-invest, development risk |
| **Credit / Debt** | "credit facility," "loan origination," "mezzanine" | Concentration limits, leverage ratios, income distributions |
| **Hedge Fund** | "trading," "NAV," "redemption," "high water mark" | Gates, side pockets, redemption terms, crystallization |
| **Fund of Funds (FoF)** | "underlying fund," "multi-manager" | Double fees, look-through rights, underlying fund selection |

---

## Phase 2: Identify Negotiable Provisions

### 2.1 Provision Extraction and Assessment

For each LP-unfavorable provision identified, extract:

| Field | Description |
|-------|-------------|
| **Provision Name** | Category label (e.g., "Carried Interest," "Key Person Provision") |
| **LPA Section** | Section and clause reference |
| **Current Language** | Exact quoted text from the LPA |
| **Plain English Summary** | What this provision actually means for LPs |
| **GP-Favorability Score** | 1 (slightly GP-favorable) to 4 (extreme) |
| **Financial Impact** | Quantified impact where possible (bps, dollars, percentage of returns) |

### 2.2 Priority Classification

Assign each provision a priority ranking:

| Priority | Label | Criteria | Negotiation Approach |
|----------|-------|----------|---------------------|
| **P0** | Dealbreaker | Provision creates unacceptable risk; commitment should not proceed without change | Lead with this; firm position; willing to walk away |
| **P1** | Critical | Materially affects LP economics or protections; strong push for change | Raise early; use market data to justify; limited flexibility |
| **P2** | Important | Meaningful but not critical; improvement would significantly enhance terms | Raise in second round; willing to accept partial improvement |
| **P3** | Desirable | Below-market but livable; improvement would be beneficial | Use as negotiating leverage; trade for P0/P1 wins |
| **P4** | Nice-to-have | Minor improvement; low financial impact | Concession candidate; trade freely for higher-priority wins |

### 2.3 Likelihood of Acceptance Assessment

For each counter-proposal, estimate likelihood of GP acceptance:

| Likelihood | Label | Basis |
|------------|-------|-------|
| **High** | Likely to accept | Market-standard request; most GPs concede this; low cost to GP |
| **Medium** | Possible | Common negotiation point; outcome depends on LP leverage and fund demand |
| **Low** | Unlikely | GP-favorable provision is intentional; GP has strong incentive to resist; requires significant LP leverage |

---

## Phase 3: Generate Counter-Proposals

### 3.1 Per-Provision Negotiation Strategy

For EACH LP-unfavorable provision, generate the following structured analysis:

#### Counter-Proposal Template

```
### [Provision Name] — Section [X.X]
**Priority:** [P0/P1/P2/P3/P4] — [Label]
**Likelihood of Acceptance:** [High/Medium/Low]

#### Current Provision
> [Exact quoted text from the LPA]

#### Market Standard Comparison
[Description of what comparable funds (same type, same size, same vintage) typically provide. Include specific data points: percentages, thresholds, common structures.]

#### Recommended Counter-Proposal
> [Specific alternative language to propose — drafted as replacement clause text that could be inserted into the LPA or a side letter]

#### Negotiation Talking Points
- [Point 1: Frame collaboratively — "We've seen in recent comparable funds..." or "ILPA best practices suggest..."]
- [Point 2: Ground the ask in something you can actually point to — the ILPA Principles text, a clause in the GP's own prior fund, or this skill's reference ranges. Do not invent a survey statistic or attribute a figure to a data provider this project holds no license to.]
- [Point 3: Explain LP benefit without implying GP bad faith — "This modification would provide greater alignment..."]
- [Point 4: If applicable, note regulatory trend — "Increasing SEC scrutiny on this area suggests..."]

#### Trade-Off Suggestions
- **Will concede**: [What the LP could offer in exchange — e.g., "Accept current management fee rate"]
- **In exchange for**: [What the LP wants — e.g., "Full clawback with 30% escrow"]

#### Financial Impact
[Quantified difference between current provision and proposed counter, where calculable]
```

### 3.2 Market Standard Reference Data

Use these benchmarks when generating counter-proposals:

**PE/Buyout Benchmarks:**
- Management fee: 1.50-2.00% on committed capital (IP), 1.00-1.50% on invested capital (post-IP)
- Carried interest: 20% with 8% preferred return, compounded annually
- GP catch-up: 100% to GP until 20% of profits
- Clawback: Full, net of taxes at 40-45% assumed rate, with 25-30% escrow
- Fee offsets: 80-100% of transaction, monitoring, and consulting fees
- Key person: Suspension of investment period upon departure of named individuals; LP vote to resume or terminate
- LPAC: Independent LP representatives with consent rights over conflicts of interest
- GP removal: Supermajority (66-75%) LP vote for cause; some funds allow no-fault removal at 75-80%

**VC Benchmarks:**
- Management fee: 2.00-2.50% on committed capital
- Carried interest: 20-25% (top-tier may command 25-30%)
- Preferred return: 0-8% (many VC funds have no hurdle)
- Recycling: 100-125% of commitments

**Real Estate Benchmarks:**
- Preferred return: 8-10%, multi-tier promote structure
- Management fee: 1.00-1.50% on committed capital
- Leverage: 50-65% LTV cap with LPAC consent above threshold

---

## Phase 4: Build Negotiation Roadmap

### 4.1 Sequencing Strategy

Organize provisions into negotiation rounds:

**Round 1 — Lead Items (P0 Dealbreakers + highest-impact P1)**
- Items that must be resolved or the LP walks away
- Raise these first to establish the LP's serious concerns
- Maximum 2-3 items to avoid overwhelming the GP

**Round 2 — Core Package (remaining P1 + high-value P2)**
- Items that materially improve LP economics and protections
- Present as a package — makes it harder for GP to reject individually
- 3-5 items in this round

**Round 3 — Value Add (remaining P2 + P3)**
- Items that enhance terms but are not critical
- Position as reasonable requests that demonstrate LP sophistication
- Be prepared to trade some of these for Round 1/2 wins

**Round 4 — Concession Trades (P4 + remaining P3)**
- Items the LP is willing to concede
- Explicitly offer to withdraw these in exchange for GP movement on priority items

### 4.2 Concession Strategy

Build a concession matrix:

| LP Concedes (Low Value to LP) | LP Gains (High Value to LP) |
|-------------------------------|----------------------------|
| [P4 item: e.g., accept current org expense cap] | [P0/P1 item: e.g., full clawback with escrow] |
| [P3 item: e.g., accept quarterly-in-advance fee payment] | [P1 item: e.g., 100% fee offset on transaction fees] |
| [P4 item: e.g., accept current confidentiality scope] | [P2 item: e.g., key person trigger with named individuals] |

### 4.3 Walk-Away List

Identify absolute dealbreakers — provisions that, if not modified, should prevent LP commitment:

| Dealbreaker Provision | Why It Is Non-Negotiable | Minimum Acceptable Modification |
|-----------------------|--------------------------|-------------------------------|
| [Provision] | [Specific risk explanation — quantified if possible] | [The least the LP should accept] |

---

## Phase 5: Generate Output File

### 5.1 Compile the Negotiation Strategy Report

Generate `NEGOTIATION-STRATEGY-[fund]-[date].md` with the following structure:

```markdown
# LPA Negotiation Strategy

> DISCLAIMER: This negotiation strategy is AI-generated and does not constitute
> legal, tax, or investment advice. It is intended for informational and
> educational purposes only. All proposed counter-language and negotiation
> strategies must be reviewed by qualified fund formation counsel before
> use in any negotiation. Market benchmarks cited are directional and may
> not reflect current market conditions or the specific context of this fund.

---

## Fund Overview

| Field | Value |
|-------|-------|
| Fund Name | [name] |
| Fund Type | [PE/VC/RE/Credit/Hedge/FoF] |
| GP Entity | [GP name] |
| Fund Size | [target / hard cap] |
| Source Document | [filename or "Prior LPA Review Output"] |
| Date of Analysis | [date] |

---

## Negotiation Summary

| Metric | Count |
|--------|-------|
| Total Provisions Flagged | [X] |
| P0 — Dealbreakers | [X] |
| P1 — Critical | [X] |
| P2 — Important | [X] |
| P3 — Desirable | [X] |
| P4 — Nice-to-have | [X] |
| Estimated High Acceptance | [X] |
| Estimated Medium Acceptance | [X] |
| Estimated Low Acceptance | [X] |

---

## Walk-Away List (Absolute Dealbreakers)

| # | Provision | Section | Why Non-Negotiable | Minimum Acceptable Change |
|---|-----------|---------|-------------------|--------------------------|
| 1 | [provision] | [X.X] | [explanation] | [minimum change] |

---

## Negotiation Roadmap

### Round 1: Lead Items (Raise First)
[P0 dealbreakers and highest-impact P1 items — 2-3 items maximum]

### Round 2: Core Package (Raise Second)
[Remaining P1 and high-value P2 items — presented as a bundle]

### Round 3: Value Add (Raise Third)
[Remaining P2 and P3 items — prepared to trade some]

### Round 4: Concession Trades (Strategic Gives)
[P4 and low-value P3 items — explicitly offered in exchange]

---

## Concession Strategy

| LP Concedes | In Exchange For |
|-------------|-----------------|
| [low-value item] | [high-value item] |

---

## Detailed Provision-by-Provision Negotiation

### P0 DEALBREAKERS

[Per-provision analysis using the Counter-Proposal Template from Phase 3.1]

### P1 CRITICAL

[Per-provision analysis]

### P2 IMPORTANT

[Per-provision analysis]

### P3 DESIRABLE

[Per-provision analysis]

### P4 NICE-TO-HAVE

[Per-provision analysis]

---

## Side Letter Strategy

If the GP is unwilling to modify the main LPA, the following provisions are
strong candidates for side letter negotiation:

1. [Provision] — [Why a side letter is appropriate]
2. [Provision] — [Why a side letter is appropriate]

---

## Recommended Next Steps

1. [ ] Review this strategy with fund formation counsel
2. [ ] Confirm market data with current placement agent or advisor
3. [ ] Prioritize dealbreakers and confirm walk-away thresholds internally
4. [ ] Prepare side letter requests as a fallback for LPA-level rejections
5. [ ] Schedule negotiation call with GP counsel
6. [ ] Run `/fund draft-side-letter` to generate side letter language for agreed modifications
```

### 5.2 Present to User

After generating the output:

1. Confirm the file was generated with its absolute path
2. State the number of provisions flagged by priority level
3. Highlight the dealbreakers (P0 items) in plain English
4. Summarize the concession strategy in one sentence
5. Suggest: "Run `/fund draft-side-letter` to generate a side letter for any negotiated modifications. Run `/fund review-lpa` first if you haven't already reviewed the full LPA."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No document provided | Ask user to provide an LPA or prior `/fund review-lpa` output |
| Document has no LP-unfavorable terms | Report that the LPA appears balanced or LP-favorable; generate a brief confirmation report noting market-standard compliance |
| Incomplete LPA (missing sections) | Analyze what is present; flag missing sections as potential negotiation items (request full LPA from GP) |
| Input is a term sheet, not an LPA | Analyze available terms; note that term sheet terms are typically negotiable before LPA drafting and flag provisions to lock down early |
| Fund type unclear | Default to PE market standards; note the assumption and recommend user specify fund type |
| Prior review output missing risk flags | Re-analyze the underlying provisions rather than relying solely on the review output |
