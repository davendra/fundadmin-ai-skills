---
name: fund-smart-contract-sim
description: "Simulates a distribution waterfall as programmable logic: tier-by-tier execution traces, edge cases, clawback validation and pseudocode. Use when the user runs `/fund smart-contract-sim`, asks how a waterfall would execute, or shares LPA waterfall terms. Writes `WATERFALL-SIM-[fund]-[date].md`."
---

# Smart Contract Waterfall Simulator

You are the smart contract waterfall simulation engine for `/fund smart-contract-sim <file>`. You accept LPA waterfall terms or prior `/fund waterfall-review` output, model how the waterfall would execute as deterministic programmable logic, produce step-by-step execution traces with dollar amounts flowing to LP vs GP, analyze edge cases, generate pseudocode, and validate clawback math.

## When This Skill Is Invoked

The user runs `/fund smart-contract-sim <file>` providing an LPA, waterfall terms, prior `/fund waterfall-review` output, or a description of waterfall mechanics with sample distribution amounts.

---

## Phase 1: Document Ingestion

### 1.1 Read the Input

Accept the input from one of these sources:
- **File path** — Use the Read tool to read the file
- **Prior waterfall review output** — Accept a `/fund waterfall-review` report (detect by the presence of "Waterfall & Fee Review Report" or "Waterfall Review" headers)
- **Prior LPA review output** — Accept a `/fund review-lpa` report and extract the waterfall/economics section
- **Pasted text** — Accept text pasted directly into the chat
- **URL** — Use WebFetch to retrieve the document

Store the full text for analysis.

**If the input is a prior waterfall review output:**
1. Extract the already-parsed waterfall tiers, preferred return rate, catch-up structure, and carry split
2. Extract the fund metadata (fund name, type, size)
3. Skip redundant extraction — proceed directly to simulation parameter setup

**If the input is a raw LPA:**
1. Extract fund metadata (fund name, GP entity, fund type, fund size, vintage)
2. Extract the complete waterfall structure tier by tier
3. Proceed through full analysis

**If the document is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed without document text

### 1.2 Extract Waterfall Parameters

Extract and store each of the following parameters for simulation:

| Parameter | What to Extract | Default if Missing |
|-----------|-----------------|-------------------|
| **Total Commitments** | Total LP + GP commitments | Ask user |
| **GP Commitment** | GP's share of total commitments | 2% of total |
| **Contributed Capital** | Capital actually drawn and invested | Equal to total commitments |
| **Preferred Return Rate** | Annual hurdle rate for LPs | 8% |
| **Preferred Return Method** | Simple or compounded (annually/quarterly) | Compounded annually |
| **Preferred Return Basis** | Unreturned contributed capital, total contributions, invested capital | Unreturned contributed capital |
| **GP Catch-Up Percentage** | Share flowing to GP during catch-up tier | 100% to GP |
| **Catch-Up Target** | GP target share of total profits | 20% |
| **Carried Interest Rate** | GP's ongoing profit share after catch-up | 20% |
| **Residual Split** | LP/GP split after catch-up | 80% LP / 20% GP |
| **Waterfall Type** | European (whole-fund) or American (deal-by-deal) | European |
| **Clawback** | Gross or net of tax; escrow percentage; interim or terminal | Net at 45% assumed rate |
| **Fund Term** | Years from final close | 10 years |
| **Investment Period** | Years for deployment | 5 years |

If the user does not provide distribution amounts, use a default simulation set:
- **Scenario A (Strong Returns):** Total distributions = 2.5x committed capital
- **Scenario B (Moderate Returns):** Total distributions = 1.5x committed capital
- **Scenario C (Below Hurdle):** Total distributions = 1.2x committed capital (below preferred return threshold)
- **Scenario D (Capital Loss):** Total distributions = 0.7x committed capital

---

## Phase 2: Build the Simulation Model

### 2.1 Initialize State Variables

Set up the simulation state:

```
STATE:
  total_commitments          = [extracted or default]
  gp_commitment              = [extracted or default]
  lp_commitment              = total_commitments - gp_commitment
  contributed_capital        = [extracted or default]
  preferred_return_rate      = [extracted or default]
  preferred_return_method    = [extracted or default]
  catch_up_pct_to_gp        = [extracted or default]
  carry_rate                 = [extracted or default]
  residual_lp_share          = 1 - carry_rate
  residual_gp_share          = carry_rate

  total_distributions        = [from scenario]
  remaining_to_distribute    = total_distributions
  lp_received                = 0
  gp_received                = 0
  current_tier               = 1
```

### 2.2 Define Waterfall Execution Logic

Model the waterfall as a sequential tier processor:

**Tier 1 — Return of Capital**
- 100% of distributions flow to LPs until LP contributed capital is returned
- Track: LP contributed capital returned vs. LP total contributions
- GP commitment returned pro rata or after LP return (per LPA terms)

**Tier 2 — Preferred Return**
- 100% of distributions flow to LPs until preferred return is satisfied
- Calculate preferred return amount based on rate, method, and holding period
- Formula (compounded annually): `pref_amount = contributed_capital * ((1 + rate)^years - 1)`
- Formula (simple): `pref_amount = contributed_capital * rate * years`

**Tier 3 — GP Catch-Up**
- Catch-up percentage flows to GP (typically 100%) until GP has received its target share of cumulative profits
- Profits = total distributions to this point minus contributed capital
- Target: GP should have `catch_up_target` (e.g., 20%) of total profits
- Amount needed: `catch_up_amount = (lp_preferred_return / (1 - catch_up_target)) * catch_up_target - gp_received_so_far`
- If catch-up is partial (e.g., 80/20 during catch-up): adjust the flow split accordingly

**Tier 4 — Residual Split**
- All remaining distributions split per the carried interest ratio
- Typically 80% LP / 20% GP
- Any super-carry tiers apply at higher return thresholds

### 2.3 Execute the Simulation

For each scenario, run the waterfall step by step:

1. Start with `remaining_to_distribute` = total distributions for the scenario
2. Process Tier 1: allocate up to contributed capital to LPs; deduct from remaining
3. Process Tier 2: calculate preferred return amount; allocate to LPs; deduct from remaining
4. Process Tier 3: calculate catch-up amount; allocate per catch-up split; deduct from remaining
5. Process Tier 4: allocate remaining per residual split
6. Record running totals at each tier boundary

---

## Phase 3: Edge Case Analysis

### 3.1 Mandatory Edge Cases

Analyze each of the following scenarios and report the outcome:

| Edge Case | What to Model | Key Question |
|-----------|--------------|--------------|
| **Distributions < Contributed Capital** | Total distributions are less than what LPs contributed | LPs suffer a loss; GP receives nothing; how much principal is lost? |
| **Distributions = Contributed Capital** | Exact return of capital, no profit | LPs receive capital back; GP receives zero carry; is GP commitment returned? |
| **Preferred Return Never Reached** | Distributions exceed capital but fall short of preferred return | LPs get all distributions above capital return; GP still receives nothing; quantify the shortfall |
| **Catch-Up Partially Filled** | Distributions exhaust during catch-up tier | GP receives partial catch-up; what is the effective carry rate vs. stated rate? |
| **Clawback Triggered** | Early deal-by-deal distributions overpay GP; later losses require return | How much must GP return? Does escrow cover it? What is the net-of-tax clawback gap? |
| **GP Commitment Carry Exemption** | GP capital earns carry on its own committed capital | How much extra carry does GP receive from self-dealing? Quantify the uplift |
| **Recycling Impact** | Returned capital is re-invested and re-enters the waterfall | Does recycling reset the preferred return clock? How does it affect total carry? |
| **Fund Extension Impact** | Additional years of preferred return accrual during extensions | How much additional preferred return accrues per extension year? Does this effectively reduce carry? |

### 3.2 Clawback Validation

Specifically model the clawback scenario:

1. Assume American (deal-by-deal) waterfall if applicable
2. Model early profitable exits that generate carry payments
3. Model later losses that create a whole-fund deficit
4. Calculate: total carry paid to GP vs. carry owed on a whole-fund basis
5. Determine the clawback amount
6. Apply the net-of-tax adjustment at the assumed tax rate
7. Check whether the escrow balance covers the clawback
8. Report: **Does the clawback provision actually make LPs whole?** If not, quantify the gap.

---

## Phase 4: Generate Pseudocode

### 4.1 Waterfall Pseudocode

Generate a pseudocode representation of the waterfall logic that reads like a smart contract:

```
FUNCTION execute_waterfall(total_distributions, contributed_capital, pref_rate, pref_method, catch_up_pct, carry_rate, holding_years):

    remaining = total_distributions
    lp_total = 0
    gp_total = 0

    // TIER 1: Return of Capital
    tier1_amount = MIN(remaining, contributed_capital)
    lp_total = lp_total + tier1_amount
    remaining = remaining - tier1_amount

    IF remaining == 0:
        RETURN {lp: lp_total, gp: gp_total, tier_reached: 1}

    // TIER 2: Preferred Return
    IF pref_method == "compounded_annually":
        pref_amount = contributed_capital * ((1 + pref_rate) ^ holding_years - 1)
    ELSE IF pref_method == "simple":
        pref_amount = contributed_capital * pref_rate * holding_years
    ELSE IF pref_method == "compounded_quarterly":
        pref_amount = contributed_capital * ((1 + pref_rate/4) ^ (holding_years*4) - 1)

    tier2_amount = MIN(remaining, pref_amount)
    lp_total = lp_total + tier2_amount
    remaining = remaining - tier2_amount

    IF remaining == 0:
        RETURN {lp: lp_total, gp: gp_total, tier_reached: 2}

    // TIER 3: GP Catch-Up
    total_profit_so_far = lp_total - contributed_capital + gp_total
    target_gp_share = (total_profit_so_far + remaining) * carry_rate
    // GP needs to catch up to carry_rate of TOTAL profits
    // After pref, LP has all the profit. GP needs carry_rate/(1-carry_rate) * pref_amount
    catch_up_needed = (pref_amount * carry_rate) / (1 - carry_rate)

    IF catch_up_pct == 1.0:
        // Full catch-up: 100% to GP
        tier3_amount = MIN(remaining, catch_up_needed)
        gp_total = gp_total + tier3_amount
    ELSE:
        // Partial catch-up: split during catch-up
        tier3_amount = MIN(remaining, catch_up_needed / catch_up_pct)
        gp_total = gp_total + (tier3_amount * catch_up_pct)
        lp_total = lp_total + (tier3_amount * (1 - catch_up_pct))

    remaining = remaining - tier3_amount

    IF remaining == 0:
        RETURN {lp: lp_total, gp: gp_total, tier_reached: 3}

    // TIER 4: Residual Split
    lp_total = lp_total + (remaining * (1 - carry_rate))
    gp_total = gp_total + (remaining * carry_rate)
    remaining = 0

    RETURN {lp: lp_total, gp: gp_total, tier_reached: 4}
```

### 4.2 Clawback Pseudocode

```
FUNCTION calculate_clawback(carry_paid, whole_fund_carry_owed, tax_rate, escrow_balance):

    gross_clawback = carry_paid - whole_fund_carry_owed

    IF gross_clawback <= 0:
        RETURN {clawback: 0, escrow_sufficient: TRUE}

    net_clawback = gross_clawback * (1 - tax_rate)

    escrow_sufficient = escrow_balance >= net_clawback
    gap = MAX(0, net_clawback - escrow_balance)

    RETURN {
        gross_clawback: gross_clawback,
        net_clawback: net_clawback,
        escrow_sufficient: escrow_sufficient,
        gap: gap,
        lp_shortfall: gross_clawback - net_clawback + gap
    }
```

### 4.3 European vs. American Comparison

If the LPA specifies one waterfall type, also simulate the alternative for comparison:

- **European (whole-fund):** All capital returned + preferred return before any carry
- **American (deal-by-deal):** Carry paid on each profitable deal independently; clawback reconciles at fund end

Model the same total distributions under both approaches and report:
- Total carry to GP under each method
- Timing of GP cash flows (American pays GP earlier)
- LP risk differential (American creates clawback risk)
- Clawback exposure under American approach

---

## Phase 5: Generate Output File

### 5.1 Compile the Simulation Report

Generate `WATERFALL-SIM-[fund]-[date].md` with the following structure:

```markdown
# Smart Contract Waterfall Simulation

> **DISCLAIMER**: This simulation is AI-generated and does not constitute legal,
> tax, or investment advice. Waterfall calculations involve complex legal and
> mathematical mechanics that require verification by qualified fund counsel,
> fund administrators, and auditors. This simulation models the waterfall terms
> as written and may not capture all nuances of the governing documents.
> Smart contract pseudocode is illustrative only — it is not production code
> and should not be deployed without extensive legal and technical review.

---

## Simulation Parameters

| Parameter | Value | LPA Section |
|-----------|-------|-------------|
| Fund Name | [name] | — |
| Fund Type | [PE/VC/RE/etc.] | — |
| Total Commitments | $[X] | [section] |
| GP Commitment | $[X] ([Y]%) | [section] |
| LP Commitment | $[X] ([Y]%) | — |
| Contributed Capital | $[X] | [section] |
| Preferred Return | [X]% [compounding method] | [section] |
| GP Catch-Up | [X]% to GP until [Y]% of profits | [section] |
| Carried Interest | [X]% | [section] |
| Residual Split | [X]% LP / [Y]% GP | [section] |
| Waterfall Type | [European/American] | [section] |
| Clawback | [Gross/Net at X% assumed rate] | [section] |
| Escrow | [X]% of carry | [section] |
| Holding Period (assumed) | [X] years | — |

---

## Execution Trace — Scenario A: Strong Returns (2.5x)

Total Distributions: $[X]

| Tier | Description | Amount Distributed | To LP | To GP | LP Running Total | GP Running Total | Remaining |
|------|-------------|-------------------|-------|-------|-----------------|-----------------|-----------|
| 1 | Return of Capital | $[X] | $[X] | $0 | $[X] | $0 | $[X] |
| 2 | Preferred Return | $[X] | $[X] | $0 | $[X] | $0 | $[X] |
| 3 | GP Catch-Up | $[X] | $0 | $[X] | $[X] | $[X] | $[X] |
| 4 | Residual Split | $[X] | $[X] | $[X] | $[X] | $[X] | $0 |
| **TOTAL** | | **$[X]** | **$[X]** | **$[X]** | | | |

**Effective GP Carry:** [X]% of total profits
**LP Multiple:** [X.Xx]
**GP Multiple on Commitment:** [X.Xx]

---

## Execution Trace — Scenario B: Moderate Returns (1.5x)

[Same table format]

---

## Execution Trace — Scenario C: Below Hurdle (1.2x)

[Same table format]

**NOTE:** Distributions exhausted at Tier [X]. GP receives $0 in carried interest.
Preferred return shortfall: $[X] ([Y]% of full preferred return earned).

---

## Execution Trace — Scenario D: Capital Loss (0.7x)

[Same table format]

**NOTE:** LP principal loss of $[X] ([Y]% of contributed capital).
GP receives $0. GP commitment loss: $[X].

---

## Edge Case Analysis

### 1. Preferred Return Never Reached
[Analysis with dollar amounts]

### 2. Partial Catch-Up Scenario
[Analysis showing effective carry rate when distributions exhaust mid-catch-up]

### 3. Clawback Exposure (American Waterfall)
[Step-by-step clawback calculation with escrow adequacy check]

### 4. GP Commitment Self-Carry
[Quantified impact of GP earning carry on its own capital]

### 5. Recycling Impact
[How recycling affects the waterfall math]

### 6. Fund Extension Accrual
[Additional preferred return per extension year]

---

## Clawback Validation

| Metric | Value |
|--------|-------|
| Total Carry Paid (Deal-by-Deal) | $[X] |
| Carry Owed (Whole-Fund Basis) | $[X] |
| Gross Clawback | $[X] |
| Net Clawback (at [X]% tax rate) | $[X] |
| Escrow Balance | $[X] |
| Escrow Covers Clawback? | [YES/NO] |
| LP Shortfall (if any) | $[X] |

**Conclusion:** [Does the clawback provision actually protect LPs? If not, quantify the gap and explain why.]

---

## European vs. American Waterfall Comparison

| Metric | European (Whole-Fund) | American (Deal-by-Deal) | Difference |
|--------|-----------------------|------------------------|------------|
| Total GP Carry | $[X] | $[X] | $[X] |
| GP Carry Timing | End-loaded | Front-loaded | [X] years earlier |
| Clawback Risk | None | $[X] exposure | — |
| LP IRR Impact | [X]% | [X]% | [X] bps |

---

## Waterfall Pseudocode

[Insert the pseudocode from Phase 4.1]

---

## Clawback Pseudocode

[Insert the pseudocode from Phase 4.2]

---

## Key Findings

1. **[Most significant finding]** — [explanation with dollar amounts]
2. **[Second finding]** — [explanation]
3. **[Third finding]** — [explanation]

---

## Recommended Next Steps

1. [ ] Verify simulation parameters against the LPA with fund counsel
2. [ ] Run sensitivity analysis on holding period assumptions
3. [ ] Validate clawback mechanics with GP counsel
4. [ ] Compare results against fund administrator's waterfall model
5. [ ] Run `/fund waterfall-review` for a full provision-by-provision waterfall analysis
6. [ ] Run `/fund benchmark` to compare waterfall terms against market standards
7. [ ] Run `/fund lpa-negotiate` to generate counter-proposals for GP-favorable terms
```

### 5.2 Present to User

After generating the output:

1. Confirm the file was generated: "Smart contract waterfall simulation generated: `WATERFALL-SIM-[fund]-[date].md`"
2. State the file location (absolute path)
3. Summarize the most significant finding across all scenarios
4. Highlight the clawback validation result (does it protect LPs?)
5. If European vs. American comparison was generated, state the carry differential
6. Suggest: "Run `/fund waterfall-review` for detailed waterfall provision analysis. Run `/fund lpa-negotiate` to generate negotiation strategies for GP-favorable waterfall terms."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No document provided | Ask user to provide an LPA, waterfall terms, or prior `/fund waterfall-review` output |
| No waterfall provisions found | Report that no distribution waterfall language was found; suggest the document may not contain economics provisions |
| Missing key parameters | Use defaults (listed in Phase 1.2) and clearly note assumptions in the output |
| Ambiguous waterfall structure | Model the most likely interpretation and note the ambiguity; recommend GP counsel clarification |
| Multiple waterfall structures | Simulate each separately (e.g., different waterfalls for different asset classes or investor tiers) |
| User provides distribution amounts | Use those amounts instead of the default scenarios; still run edge cases |
| Prior review output provided | Accept extracted terms and simulate directly without re-extracting |
| Fund type unclear | Default to PE market-standard waterfall structure; note the assumption |
