---
name: fund-waterfall-review
description: "Extracts waterfall tiers, pref, catch-up, carry, clawback and fees, checks consistency, scores vs market. Use for `/fund waterfall-review`. Writes `WATERFALL-REVIEW-[fund]-[date].md`."
---

# Waterfall / Fee Review

You are the waterfall and fee review engine for `/fund waterfall-review <file>`. You extract distribution waterfall mechanics from LPAs and fund documents, validate internal consistency, compare against market standards, and flag unusual or aggressive provisions.

## When This Skill Is Invoked

The user runs `/fund waterfall-review <file>` providing an LPA, PPM, or any fund document that contains distribution waterfall, fee, or economics provisions.

---

## Phase 1: Document Ingestion

### 1.1 Read the Document

Accept the document from one of these sources:
- **File path** — Use the Read tool to read the file
- **Pasted text** — Accept text pasted directly into the chat
- **URL** — Use WebFetch to retrieve the document

Store the full document text for analysis.

**If the document is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed to Phase 2 without document text

### 1.2 Classify the Fund Type

Identify the fund type to select the correct market-standard benchmarks.

_The structures below follow ILPA's published Private Equity Principles and widely documented waterfall conventions. They are not drawn from any licensed market dataset, and no commercial data provider should be cited for them._

| Fund Type | Detection Signals | Typical Waterfall Structure |
|-----------|-------------------|---------------------------|
| **Private Equity (PE)** | "buyout," "acquisition," "portfolio company," "leveraged" | European (whole-fund) or American (deal-by-deal), 8% pref, 100% GP catch-up to 20%, 80/20 split |
| **Venture Capital (VC)** | "venture," "seed," "Series A/B/C," "startup" | Often no preferred return or lower (6%), simpler waterfall, sometimes no catch-up |
| **Real Estate (RE)** | "real property," "REIT," "development," "mortgage" | Multi-tier promote structure (8-10% pref, then promote tiers at IRR hurdles), higher carry at higher returns |
| **Credit / Debt** | "credit," "loan origination," "mezzanine," "distressed" | Income-based with incentive fee, sometimes European-style with lower hurdle (5-7%) |
| **Hedge Fund** | "trading," "NAV," "redemption," "high water mark" | 1-2% management fee, 20% incentive allocation with high water mark, crystallization frequency varies |
| **Fund of Funds (FoF)** | "underlying fund," "multi-manager," "allocation" | Lower carry (5-10%), management fee on NAV or commitments, double-layer fee consideration |

---

## Phase 2: Extract Waterfall Mechanics

### 2.1 Core Waterfall Elements

Extract each of the following from the document. For each element, record the exact LPA section reference, the provision text, and a plain English summary.

#### Distribution Waterfall Tiers

Extract the complete waterfall structure, tier by tier:

| Tier | Description | What to Extract |
|------|-------------|-----------------|
| **Tier 1 — Return of Capital** | Return of contributed capital to LPs | Basis: all contributions vs. deal-specific? Includes fees/expenses or net of fees? Recycling provisions? |
| **Tier 2 — Preferred Return** | Priority return to LPs before carry | Rate (e.g., 8%), compounding method (simple, compounded annually, compounded quarterly, continuous), basis (contributed capital, invested capital), accrual on unreturned capital only or all contributions |
| **Tier 3 — GP Catch-Up** | GP receives increased share until reaching target carry | Catch-up percentage (typically 100% to GP, but sometimes 80/20), catch-up target (typically to equalize GP at 20% of profits), partial vs. full catch-up |
| **Tier 4 — Carried Interest Split** | Ongoing profit split after catch-up | Split ratio (typically 80% LP / 20% GP), any super-carry tiers at higher return thresholds, performance fee caps |

#### Preferred Return Details

| Element | What to Extract |
|---------|-----------------|
| **Rate** | Annual percentage rate |
| **Compounding** | Simple interest, compounded annually, compounded quarterly, continuously compounded |
| **Basis** | Unreturned contributed capital, total committed capital, invested capital |
| **Accrual start** | From contribution date, from fund closing, from investment date |
| **Catch-up on unpaid** | Does unpaid preferred return compound? |

#### Catch-Up Structure

| Element | What to Extract |
|---------|-----------------|
| **Percentage to GP** | 100% (full catch-up) or split (e.g., 80% GP / 20% LP) |
| **Target** | Catch-up until GP has received X% of cumulative profits (typically 20%) |
| **Calculation** | Is catch-up calculated on a whole-fund or deal-by-deal basis? |

#### Carried Interest

| Element | What to Extract |
|---------|-----------------|
| **Rate** | Standard carry percentage (typically 20%) |
| **Basis** | Whole-fund (European) or deal-by-deal (American) |
| **Super-carry tiers** | Any increased carry at higher return thresholds (e.g., 25% above 2x MOIC, 30% above 3x MOIC) |
| **Carry recipient** | GP entity, management company, or carried interest vehicle |
| **Carry vesting** | Time-based vesting of carry for individuals? Forfeiture provisions? |

### 2.2 GP Clawback Provisions

| Element | What to Extract |
|---------|-----------------|
| **Trigger** | What triggers the clawback obligation (fund-level loss, LP not receiving pref + return of capital) |
| **Calculation method** | Gross clawback (before tax) or net clawback (after tax, typically at assumed rate of 40-45%) |
| **Escrow / Holdback** | Is a portion of carry held in escrow? What percentage (typically 20-30%)? Release conditions? |
| **Joint and several** | Are individual carry recipients jointly and severally liable? |
| **Cap** | Is the clawback limited to carry actually received (net of taxes)? |
| **Timing** | When is the clawback calculated — at fund termination only, or interim true-up? |
| **Guaranty** | Does the GP or management company guarantee individual clawback obligations? |

### 2.3 Management Fee Provisions

| Element | What to Extract |
|---------|-----------------|
| **Rate — Investment Period** | Annual rate during commitment/investment period |
| **Rate — Post-Investment Period** | Annual rate after commitment period ends (typically reduced or shifted basis) |
| **Basis — Investment Period** | Committed capital, drawn capital, or NAV |
| **Basis — Post-Investment Period** | Invested capital (at cost or fair value), NAV, or committed capital (reduced) |
| **Payment frequency** | Quarterly in advance, quarterly in arrears, semi-annual, annual |
| **Fee reduction events** | Key person trigger, investment period end, fund extensions |
| **Step-down** | Any scheduled fee reductions over fund life |

### 2.4 Fee Offset Provisions

| Element | What to Extract |
|---------|-----------------|
| **Transaction fees** | Are fees earned by GP/affiliates from portfolio companies offset against management fees? What percentage (100%, 80%, 50%)? |
| **Monitoring / consulting fees** | Ongoing fees from portfolio companies — offset percentage |
| **Director fees** | Board fees received by GP personnel — offset or retained? |
| **Break-up / topping fees** | Deal break-up fees — offset or retained? |
| **Placement agent fees** | Charged to fund or paid by GP? If charged to fund, offset against management fees? |

### 2.5 Organizational Expense Provisions

| Element | What to Extract |
|---------|-----------------|
| **Cap** | Maximum organizational expenses chargeable to the fund (dollar amount or % of commitments) |
| **Included expenses** | Legal, accounting, regulatory filings, travel, placement agent fees? |
| **Excess treatment** | Who bears expenses above the cap — GP or amortized to LPs? |

---

## Phase 3: Validate Internal Consistency

### 3.1 Consistency Checks

Perform each of the following checks and report PASS, WARNING, or FAIL:

| Check | What to Verify | Common Issue |
|-------|---------------|--------------|
| **Clawback protection** | Does the clawback actually protect LPs if carry is overpaid early? Does it cover the full amount or is it capped at net-of-tax carry received? | Net clawback at assumed tax rate may leave LPs short |
| **Catch-up math** | Does the catch-up percentage and structure actually result in the stated carry split? (e.g., 100% GP catch-up after 8% pref should result in GP at 20% of all profits) | Incomplete catch-up (80/20 during catch-up) permanently reduces GP share below stated carry |
| **Fee offset clarity** | Are fee offsets clearly defined for all fee types? Are there carve-outs that effectively negate the offset? | Vague offset language ("customary" fees) creates disputes |
| **Preferred return basis** | Is the preferred return calculated on the correct basis throughout? Does it match the stated rate? | Basis switching between sections (committed vs. contributed capital) |
| **Waterfall completeness** | Are all distribution scenarios covered? What happens on interim distributions vs. final liquidation? | Missing interim distribution mechanics create ambiguity |
| **Recycling vs. waterfall** | If recycled capital is re-invested, how does it flow through the waterfall? Is recycled capital treated as new contributions or original contributions? | Recycling can manipulate the preferred return calculation |
| **Management fee basis transition** | Is the transition from investment-period fee to post-period fee clearly defined? What triggers the transition? | Ambiguity around investment period extensions affecting fee basis |
| **GP commitment carry exemption** | Is the GP's share of distributions exempt from the waterfall (no pref, no catch-up on GP commitment)? | GP commitment earning carry on itself inflates carry payments |
| **Tax distribution priority** | Are tax distributions provided for? Do they come off the top before the waterfall? | Missing tax distribution provisions force LPs to fund taxes from other sources |
| **Default penalty interaction** | How do defaulting LP penalties interact with the waterfall? | Default provisions may create windfall for non-defaulting LPs or GP |

### 3.2 Cross-Reference Checks

| Check | What to Verify |
|-------|---------------|
| **Defined terms consistency** | Do terms like "Net Profits," "Distributable Proceeds," "Capital Account" have consistent definitions throughout? |
| **Section cross-references** | Do cross-references within the waterfall sections point to correct provisions? |
| **Fee offset vs. waterfall** | Are management fee offsets reflected in the waterfall calculation (i.e., are offset amounts treated as distributions)? |
| **Side letter impact** | Are there carve-outs for side letter modifications to the waterfall? |

---

## Phase 4: Compare Against Market Standards

### 4.1 Market Standard Benchmarks

Compare the extracted waterfall terms against market standards for the identified fund type:

#### Private Equity (Buyout) Market Standard

| Term | Market Standard | Acceptable Range | Red Flag |
|------|----------------|-----------------|----------|
| Preferred Return | 8% compounded annually | 6-10% | No preferred return; simple interest only |
| GP Catch-Up | 100% to GP until 20% of profits | 80-100% catch-up | No catch-up (GP gets 20% from dollar one) |
| Carried Interest | 20% | 15-25% | >25% without performance hurdles |
| Clawback | Full clawback, net of taxes at assumed rate | Net at 40-50% assumed rate | No clawback; clawback capped below carry received |
| Escrow | 20-30% of carry in escrow | 10-30% | No escrow at all |
| Management Fee (IP) | 1.5-2.0% on committed capital | 1.0-2.5% | >2.5% or on a basis larger than commitments |
| Management Fee (Post-IP) | 1.0-1.5% on invested capital at cost | Reduced rate on reduced basis | No step-down; same rate/basis post-investment period |
| Fee Offsets | 80-100% of transaction/monitoring fees | 50-100% | 0% offset; vague offset language |
| Org Expense Cap | $500K-$2M or 0.5-1% of commitments | Varies by fund size | No cap; uncapped placement agent fees included |
| Waterfall Type | European (whole-fund) | American with interim clawback | American with no interim true-up |

#### Venture Capital Market Standard

| Term | Market Standard | Acceptable Range | Red Flag |
|------|----------------|-----------------|----------|
| Preferred Return | 0% or 6-8% | 0-8% | >10% in VC context |
| Carried Interest | 20-25% | 20-30% for top-tier | >30% without exceptional track record |
| Management Fee | 2.0-2.5% on committed capital | 1.5-3.0% | >3.0%; no step-down for long fund life |
| Recycling | Yes, up to 100-125% of commitments | 100-150% | Unlimited recycling with no LP consent |
| Clawback | Often limited or no clawback | Varies widely | — |

#### Hedge Fund Market Standard

| Term | Market Standard | Acceptable Range | Red Flag |
|------|----------------|-----------------|----------|
| Management Fee | 1.0-2.0% on NAV | 0.5-2.0% | >2.0% on gross assets; fee on committed but uninvested capital |
| Incentive Fee | 20% with high water mark | 15-25% | No high water mark; no crystallization frequency defined |
| High Water Mark | Perpetual, loss carry-forward | Per-share or aggregate | Resettable HWM; modified HWM with time decay |
| Hurdle Rate | SOFR or 4-6% fixed | 0-8% | — |
| Crystallization | Annual | Quarterly to annual | More frequent than quarterly |

#### Real Estate Market Standard

| Term | Market Standard | Acceptable Range | Red Flag |
|------|----------------|-----------------|----------|
| Preferred Return | 8-10% | 6-12% | <6% without justification |
| Promote Structure | Multi-tier (8% pref, then tiers at IRR hurdles) | 2-4 tiers | Single tier with high promote from dollar one |
| Carried Interest | 15-20% (escalating with IRR) | 10-30% across tiers | Flat 30%+ with no IRR hurdle |
| Management Fee | 1.0-1.5% on committed (IP), lower post-IP | 0.75-2.0% | >2.0%; fee on gross asset value |
| Clawback | Full clawback with escrow | Net at assumed rate | No clawback for development funds |

### 4.2 Deviation Scoring

For each term extracted, score the deviation from market standard:

| Score | Label | Meaning |
|-------|-------|---------|
| 0 | Market Standard | Within normal range for fund type |
| 1 | Slightly GP-Favorable | Minor deviation, common in GP-friendly deals |
| 2 | Moderately GP-Favorable | Notable deviation, should be flagged for negotiation |
| 3 | Aggressive | Significantly outside market norms, material LP risk |
| 4 | Extreme | Far outside market standards, potential red flag for commitment decision |

---

## Phase 5: Generate Output File

### 5.1 Compile the Waterfall Review Report

Generate `WATERFALL-REVIEW-[fund]-[date].md` with the following structure:

```markdown
# Waterfall & Fee Review Report

> DISCLAIMER: This analysis is AI-generated and does not constitute legal, tax,
> or investment advice. Waterfall calculations involve complex legal and
> mathematical mechanics that require review by qualified fund counsel and
> fund administrators. This review analyzes the terms as written — it does
> not perform waterfall calculations.

---

## Fund Overview

| Field | Value |
|-------|-------|
| Fund Name | [name] |
| Fund Type | [type] |
| Waterfall Type | [European (whole-fund) / American (deal-by-deal)] |
| Document Reviewed | [filename] |
| Date of Review | [date] |

---

## Waterfall Structure — Visual Tier Breakdown

### Distribution Priority

```
TIER 1: RETURN OF CAPITAL
[100% to LPs]
Basis: [all contributions / invested capital only]
─────────────────────────────────────────────────

TIER 2: PREFERRED RETURN
[100% to LPs]
Rate: [X]% [compounding method]
Basis: [unreturned contributions / committed capital]
─────────────────────────────────────────────────

TIER 3: GP CATCH-UP
[X]% to GP / [Y]% to LPs
Until GP has received [Z]% of cumulative profits
─────────────────────────────────────────────────

TIER 4: CARRIED INTEREST SPLIT
[X]% to LPs / [Y]% to GP
[Any super-carry tiers listed]
─────────────────────────────────────────────────
```

---

## Economics Summary Table

| Term | This Fund | Market Standard | Deviation |
|------|----------|----------------|-----------|
| Preferred Return Rate | [X]% | [Y]% | [0-4 score with label] |
| Preferred Return Compounding | [method] | [typical] | [score] |
| GP Catch-Up | [X]% | [typical]% | [score] |
| Carried Interest | [X]% | [typical]% | [score] |
| Carry Basis | [whole-fund/deal-by-deal] | [typical] | [score] |
| Clawback | [description] | [typical] | [score] |
| Escrow | [X]% | [typical]% | [score] |
| Mgmt Fee (IP) | [X]% on [basis] | [typical] | [score] |
| Mgmt Fee (Post-IP) | [X]% on [basis] | [typical] | [score] |
| Fee Offsets | [X]% | [typical]% | [score] |
| Org Expense Cap | $[X] | [typical] | [score] |

---

## Consistency Check Results

| # | Check | Result | Details |
|---|-------|--------|---------|
| 1 | Clawback protects LP adequately | [PASS/WARNING/FAIL] | [explanation] |
| 2 | Catch-up math produces stated carry split | [PASS/WARNING/FAIL] | [explanation] |
| 3 | Fee offsets clearly defined | [PASS/WARNING/FAIL] | [explanation] |
| 4 | Preferred return basis consistent | [PASS/WARNING/FAIL] | [explanation] |
| 5 | Waterfall covers all distribution scenarios | [PASS/WARNING/FAIL] | [explanation] |
| 6 | Recycling provisions clear | [PASS/WARNING/FAIL] | [explanation] |
| 7 | Fee basis transition defined | [PASS/WARNING/FAIL] | [explanation] |
| 8 | GP commitment carry treatment clear | [PASS/WARNING/FAIL] | [explanation] |
| 9 | Tax distribution provisions present | [PASS/WARNING/FAIL] | [explanation] |
| 10 | Default penalty interaction defined | [PASS/WARNING/FAIL] | [explanation] |

---

## Risk Flags

### HIGH RISK (Deviation Score 3-4)
[List each provision with score 3-4, explaining what it says, why it
deviates from market, and the financial impact to LPs]

### MEDIUM RISK (Deviation Score 2)
[List each provision with score 2]

### LOW RISK / MARKET STANDARD (Deviation Score 0-1)
[Brief summary of provisions that are within market norms]

---

## Detailed Provision Analysis

### Preferred Return
- **LPA Section:** [X.X]
- **What it says:** [plain English summary]
- **Market comparison:** [how this compares]
- **Risk assessment:** [impact analysis]

### GP Catch-Up
[Same format]

### Carried Interest
[Same format]

### GP Clawback
[Same format]

### Management Fees
[Same format]

### Fee Offsets
[Same format]

### Organizational Expenses
[Same format]

---

## Negotiation Recommendations

1. **[Highest Priority]** — [Specific change to request with market-standard justification]
2. **[Second Priority]** — [Specific change]
3. **[Third Priority]** — [Specific change]

---

## Recommended Next Steps

1. [ ] Review flagged provisions with fund counsel
2. [ ] Request fee calculation examples from GP for verification
3. [ ] Compare waterfall terms with prior fund (if applicable)
4. [ ] Model waterfall outcomes under stress scenarios (low-return and high-return)
5. [ ] Negotiate priority items before executing subscription documents
6. [ ] Confirm clawback mechanics with GP counsel
```

### 5.2 Present to User

After generating the output:

1. Confirm the file was generated: "Waterfall review generated: `WATERFALL-REVIEW-[fund]-[date].md`"
2. State the file location (absolute path)
3. Highlight the most critical finding (highest deviation score or consistency check failure)
4. Summarize the overall deviation profile: "X provisions at market standard, Y slightly GP-favorable, Z aggressive"
5. Suggest: "Run `/fund review-lpa` for a comprehensive LPA analysis beyond waterfall mechanics. Run `/fund report-pdf` to generate a formatted PDF."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No document provided | Ask user to provide an LPA or fund document containing waterfall provisions |
| Document has no waterfall provisions | Report that no distribution waterfall language was found; suggest the document may not be an LPA or may be a preliminary term sheet |
| Incomplete waterfall (missing tiers) | Analyze what is present, flag missing tiers in the consistency checks, note gaps in the output |
| Ambiguous provisions | Flag ambiguous language in the consistency checks with WARNING status; recommend clarification from GP counsel |
| Multiple waterfall structures | If the document describes different waterfalls for different asset classes or time periods, analyze each separately and note the structure |
| Fund type unclear | Default to PE market standards; note the assumption and recommend the user specify the fund type |
