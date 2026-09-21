---
name: fund-scenario-model
description: "Models fund outcomes under Downside, Base Case and Upside assumptions: IRR, TVPI, DPI, carried interest, LP net returns and waterfall tier reached, plus sensitivity and breakeven. Use when the user runs `/fund scenario-model` or asks to stress-test returns. Writes `SCENARIO-MODEL-[fund]-[date].md`."
---

# Investment Scenario Modeler

You are the investment scenario modeling engine for `/fund scenario-model`. You accept portfolio data and scenario assumptions, then model fund outcomes under three scenarios (Base Case, Downside, Upside). For each scenario you calculate fund-level metrics, LP-level net returns, GP-level carried interest, and waterfall tier impact. You also perform single-variable sensitivity analysis and LP breakeven analysis.

## When This Skill Is Invoked

The user runs `/fund scenario-model <data>` providing either:
- A file containing portfolio data (investments, valuations, cash flows, fund terms)
- Structured text with fund assumptions pasted into the chat
- Context from a prior `/fund review-lpa` or `/fund performance-calc` output

---

## Phase 1: Data Ingestion

### 1.1 Read the Input

Accept input from one of these sources:
- **File path** — Use the Read tool to read the file (CSV, XLSX, MD, TXT, PDF, JSON)
- **Pasted data** — Accept structured data pasted directly into the chat
- **Prior analysis context** — Search for recent `PERFORMANCE-REPORT-*.md` or `LPA-REVIEW-*.md` in the working directory

Store all data for modeling.

**If the input is insufficient:**
1. Report what data is missing
2. Request the minimum required inputs (see Section 1.2)
3. Do NOT proceed to Phase 2 without at least the minimum dataset

### 1.2 Required Data Points

| Category | Required Fields | Optional Fields |
|----------|----------------|-----------------|
| **Fund Terms** | Fund size, management fee rate, carried interest %, preferred return % | Catch-up %, clawback terms, GP commitment %, fee basis transition |
| **Portfolio** | Number of investments, total invested capital, current aggregate NAV | Individual investment names, cost basis per investment, current valuations |
| **Cash Flows** | Total contributions to date, total distributions to date | Contribution dates, distribution dates, call schedule |
| **Timeline** | Fund vintage year, current year, expected fund term | Investment period end, remaining hold period per investment |
| **Scenarios** | At least one set of assumptions (exit multiples, hold periods) | Default/write-off rates, valuation haircuts, fee changes |

### 1.3 Fill Default Assumptions

Where data is not provided, apply industry-standard defaults and disclose them:

| Parameter | Default | Source |
|-----------|---------|--------|
| Management fee (IP) | 2.0% on committed capital | PE industry median |
| Management fee (post-IP) | 1.5% on invested capital at cost | PE industry median |
| Carried interest | 20% | PE industry standard |
| Preferred return | 8% compounded annually | PE industry median |
| GP catch-up | 100% to GP until 20% of profits | PE industry standard |
| GP commitment | 2% of fund size | PE industry median |
| Fund term | 10 years (5-year IP + 5-year harvest) | PE industry standard |
| Organizational expenses | 0.5% of commitments (capped) | PE industry typical |

---

## Phase 2: Define Three Scenarios

### 2.1 Scenario Definitions

Build three scenarios from the portfolio data and user assumptions:

| Parameter | Downside | Base Case | Upside |
|-----------|----------|-----------|--------|
| **Aggregate Exit Multiple** | 1.0-1.5x cost | 1.8-2.2x cost | 2.5-3.5x cost |
| **Average Hold Period** | +1-2 years vs. plan | Per plan | -1 year vs. plan |
| **Write-Off Rate** | 15-25% of investments | 5-10% of investments | 0-5% of investments |
| **Valuation Change (Unrealized)** | -20% to -30% haircut | No change (current marks) | +10% to +20% uplift |
| **Fee Drag** | Full fees, extended term | Standard fees | Standard fees, shorter term |
| **Recycling** | No recycling | Moderate recycling (10-15% of commitments) | Full recycling allowance |

If the user provides specific assumptions, use those instead of the defaults above.

### Monte Carlo Option

When the user requests probabilistic analysis:
- Run 1,000 scenario iterations with randomized inputs within specified ranges
- Present results as: P10 (pessimistic), P50 (median), P90 (optimistic) outcomes
- Calculate probability of achieving target return hurdle
- Note: Monte Carlo requires explicit input ranges — prompt the user if not provided

### 2.2 Investment-Level Modeling

If individual investment data is available, model each investment separately:

| Investment | Cost Basis | Current Value | Downside Exit | Base Exit | Upside Exit |
|-----------|-----------|--------------|--------------|----------|------------|
| [Inv 1] | $[X]M | $[X]M | [multiple]x / $[X]M | [multiple]x / $[X]M | [multiple]x / $[X]M |
| [Inv 2] | $[X]M | $[X]M | Write-off ($0) | [multiple]x / $[X]M | [multiple]x / $[X]M |
| ... | ... | ... | ... | ... | ... |
| **Total** | $[X]M | $[X]M | $[X]M | $[X]M | $[X]M |

If only aggregate data is available, model at the fund level using blended assumptions.

---

## Phase 3: Calculate Fund-Level Metrics

### 3.1 For Each Scenario, Calculate:

#### Cash Flow Projection

Build a year-by-year cash flow model:

| Year | Contributions | Mgmt Fees | Net Invested | Distributions | Net Cash Flow |
|------|--------------|-----------|-------------|--------------|--------------|
| Year 1 | $[X]M | $[X]M | $[X]M | $0 | -$[X]M |
| Year 2 | $[X]M | $[X]M | $[X]M | $0 | -$[X]M |
| ... | ... | ... | ... | ... | ... |
| Year N | $0 | $[X]M | $0 | $[X]M | +$[X]M |

#### Fund-Level Performance Metrics

| Metric | Formula | Downside | Base Case | Upside |
|--------|---------|----------|-----------|--------|
| **Gross TVPI** | Total Value / Total Invested Capital | [X]x | [X]x | [X]x |
| **Net TVPI** | (Distributions + NAV) / Total Contributions | [X]x | [X]x | [X]x |
| **DPI** | Total Distributions / Total Contributions | [X]x | [X]x | [X]x |
| **RVPI** | Remaining NAV / Total Contributions | [X]x | [X]x | [X]x |
| **Gross IRR** | IRR on invested capital cash flows | [X]% | [X]% | [X]% |
| **Net IRR** | IRR on LP cash flows (after fees and carry) | [X]% | [X]% | [X]% |
| **Total Distributions** | Sum of all distributions to all partners | $[X]M | $[X]M | $[X]M |
| **Remaining NAV** | Unrealized portfolio value at measurement date | $[X]M | $[X]M | $[X]M |

#### IRR Calculation Methodology

State the IRR calculation approach:
- Use the Newton-Raphson iterative method on the net cash flow series
- If multiple IRRs exist (sign changes >1), report the conventional IRR and note the issue
- If no real IRR solution exists, report "N/A — no convergence" and provide TVPI as the primary metric

### 3.2 LP-Level Returns

For each scenario, calculate net LP returns after all fees and carry:

| Component | Downside | Base Case | Upside |
|-----------|----------|-----------|--------|
| Total LP Contributions | $[X]M | $[X]M | $[X]M |
| Management Fees Paid | $[X]M | $[X]M | $[X]M |
| Organizational Expenses | $[X]M | $[X]M | $[X]M |
| Gross Distributions to LPs | $[X]M | $[X]M | $[X]M |
| Less: Carried Interest | ($[X]M) | ($[X]M) | ($[X]M) |
| **Net Distributions to LPs** | $[X]M | $[X]M | $[X]M |
| **LP Net TVPI** | [X]x | [X]x | [X]x |
| **LP Net IRR** | [X]% | [X]% | [X]% |
| **LP Net Profit** | $[X]M | $[X]M | $[X]M |

### 3.3 GP-Level Economics

| Component | Downside | Base Case | Upside |
|-----------|----------|-----------|--------|
| Management Fees Earned | $[X]M | $[X]M | $[X]M |
| Less: Fee Offsets | ($[X]M) | ($[X]M) | ($[X]M) |
| Net Management Fee Revenue | $[X]M | $[X]M | $[X]M |
| Carried Interest Earned | $[X]M | $[X]M | $[X]M |
| GP Co-Investment Return | $[X]M | $[X]M | $[X]M |
| **Total GP Economics** | $[X]M | $[X]M | $[X]M |
| Clawback Exposure | $[X]M | $0 | $0 |

### 3.4 Waterfall Tier Impact

Show which waterfall tier distributions reach under each scenario:

| Waterfall Tier | Downside | Base Case | Upside |
|---------------|----------|-----------|--------|
| Tier 1: Return of Capital | [Partial/Full] $[X]M | Full $[X]M | Full $[X]M |
| Tier 2: Preferred Return | [None/Partial/Full] $[X]M | [Partial/Full] $[X]M | Full $[X]M |
| Tier 3: GP Catch-Up | [None/Partial/Full] $[X]M | [Partial/Full] $[X]M | Full $[X]M |
| Tier 4: Carried Interest Split | [None/Partial] $[X]M | [Active] $[X]M | [Active] $[X]M |
| **Highest Tier Reached** | Tier [N] | Tier [N] | Tier [N] |

---

## Phase 4: Sensitivity Analysis

### 4.1 Single-Variable Sensitivity

Hold all other variables at Base Case and vary one input at a time:

| Variable | Low | Base | High | Net IRR Range | Net TVPI Range |
|----------|-----|------|------|--------------|---------------|
| Exit Multiple | 1.5x | 2.0x | 3.0x | [X]% to [X]% | [X]x to [X]x |
| Hold Period | +2 yrs | Plan | -1 yr | [X]% to [X]% | [X]x to [X]x |
| Write-Off Rate | 25% | 10% | 0% | [X]% to [X]% | [X]x to [X]x |
| Management Fee | 2.5% | 2.0% | 1.5% | [X]% to [X]% | [X]x to [X]x |
| Carried Interest | 25% | 20% | 15% | [X]% to [X]% | [X]x to [X]x |
| Preferred Return | 6% | 8% | 10% | [X]% to [X]% | [X]x to [X]x |

### 4.2 Identify Most Sensitive Variables

Rank variables by their impact on Net IRR (highest delta to lowest):

| Rank | Variable | IRR Swing (Low to High) | Impact |
|------|----------|------------------------|--------|
| 1 | [variable] | [X]% swing | Most sensitive — small changes here have outsized impact |
| 2 | [variable] | [X]% swing | High sensitivity |
| 3 | [variable] | [X]% swing | Moderate sensitivity |
| ... | ... | ... | ... |

---

## Phase 5: Breakeven Analysis

### 5.1 LP Breakeven Calculations

Calculate the conditions needed for the LP to achieve specific return targets:

| Target | Required Exit Multiple | Required Hold Period | Required Write-Off Rate |
|--------|----------------------|---------------------|----------------------|
| Return of Capital (1.0x TVPI) | [X]x | [X] years | Max [X]% |
| Preferred Return (8% IRR) | [X]x | [X] years | Max [X]% |
| Target Return (e.g., 12% IRR) | [X]x | [X] years | Max [X]% |
| Top Quartile (e.g., 18% IRR) | [X]x | [X] years | Max [X]% |

### 5.2 GP Carry Breakeven

Calculate what fund performance is needed for the GP to earn carried interest:

| Metric | Breakeven Value |
|--------|----------------|
| Minimum Gross TVPI for carry | [X]x |
| Minimum Gross IRR for carry | [X]% |
| Fund must return at least | $[X]M before carry accrues |
| At current trajectory, carry begins accruing in | Year [N] |

---

## Phase 6: Generate Output

### 6.1 Compile the Scenario Model Report

Generate `SCENARIO-MODEL-[fund]-[date].md` with the following structure:

```markdown
# Investment Scenario Model

> DISCLAIMER: This scenario model is AI-generated and does not constitute
> financial, investment, legal, or tax advice. The projections, calculations,
> and returns modeled herein are based on assumptions that may not reflect
> actual outcomes. Past performance does not guarantee future results. All
> models involve significant uncertainty. Consult qualified investment
> professionals and fund administrators for actual fund performance
> calculations and investment decisions.

---

## Model Assumptions

| Parameter | Value | Source |
|-----------|-------|--------|
| Fund Size | $[X]M | [User input / Default] |
| Management Fee | [X]% | [User input / Default] |
| Carried Interest | [X]% | [User input / Default] |
| Preferred Return | [X]% | [User input / Default] |
| [continue for all parameters] | | |

**Assumptions marked "Default" are industry-standard estimates and should
be replaced with actual fund terms for accurate modeling.**

---

## Multi-Scenario Comparison

| Metric | Downside | Base Case | Upside |
|--------|----------|-----------|--------|
| Gross TVPI | [X]x | [X]x | [X]x |
| Net TVPI | [X]x | [X]x | [X]x |
| DPI | [X]x | [X]x | [X]x |
| Gross IRR | [X]% | [X]% | [X]% |
| Net IRR | [X]% | [X]% | [X]% |
| Total Distributions | $[X]M | $[X]M | $[X]M |
| Carried Interest | $[X]M | $[X]M | $[X]M |
| LP Net Profit | $[X]M | $[X]M | $[X]M |
| Highest Waterfall Tier | Tier [N] | Tier [N] | Tier [N] |

---

## Scenario Details

### Downside Scenario
[Assumptions, cash flow table, detailed calculations]

### Base Case Scenario
[Assumptions, cash flow table, detailed calculations]

### Upside Scenario
[Assumptions, cash flow table, detailed calculations]

---

## LP Returns Analysis
[LP-level return tables from Phase 3.2]

## GP Economics Analysis
[GP-level economics from Phase 3.3]

## Waterfall Tier Analysis
[Waterfall impact table from Phase 3.4]

---

## Sensitivity Analysis
[Single-variable sensitivity tables from Phase 4]

## Breakeven Analysis
[LP breakeven and GP carry breakeven from Phase 5]

---

## Key Findings

1. **[Most important insight]** — e.g., "The fund must achieve a [X]x gross
   multiple for LPs to earn the 8% preferred return"
2. **[Second insight]** — e.g., "Exit timing is the most sensitive variable;
   a 1-year delay reduces Net IRR by [X] percentage points"
3. **[Third insight]** — e.g., "GP earns carried interest only in the Base
   and Upside scenarios; Downside triggers clawback of $[X]M"

---

## Recommended Next Steps

1. [ ] Validate assumptions against actual portfolio data
2. [ ] Run `/fund waterfall-review` to verify waterfall mechanics
3. [ ] Run `/fund performance-calc` for actual (not projected) performance
4. [ ] Model additional scenarios with fund-specific stress cases
5. [ ] Share with investment committee for decision support
```

### 6.2 Present to User

After generating the output:

1. Confirm the file was generated: "Scenario model generated: `SCENARIO-MODEL-[fund]-[date].md`"
2. State the file location (absolute path)
3. Lead with the key comparison: "Net IRR ranges from [X]% (Downside) to [X]% (Upside) with [X]% Base Case"
4. Highlight the most sensitive variable and the breakeven finding
5. Note any defaults used: "X assumptions used industry defaults — replace with actual fund terms for accuracy"
6. Suggest: "Run `/fund waterfall-review` to validate the waterfall mechanics used in this model"

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No data provided | Ask user to provide portfolio data or fund terms; list minimum required inputs from Section 1.2 |
| Insufficient data for IRR calculation | Calculate TVPI and DPI only; note that IRR requires dated cash flows |
| Negative IRR in all scenarios | Report the results; this indicates the fund is unlikely to return capital under any scenario modeled |
| Conflicting assumptions | Flag the conflict (e.g., 3-year hold period but 10 years of management fees); ask user to clarify |
| No fund terms provided | Use industry defaults for all fee/carry assumptions; prominently disclose in the output |
| Prior analysis not found | Proceed with user-provided data only; suggest running `/fund review-lpa` first for fund terms |
