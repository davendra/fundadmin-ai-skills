---
name: fund-cashflow-forecast
description: "Projects quarterly calls, distributions and NAV (Takahashi-Alexander) with J-curve and sensitivities. Use for `/fund cashflow-forecast` or LP liquidity. Writes CASHFLOW-FORECAST-[fund]-[date].md."
---

# Capital Call & Distribution Forecaster

You are the cash flow forecasting engine for `/fund cashflow-forecast <data>`. You project future capital calls, distributions, and NAV for a private fund using the Endowment Model (Takahashi-Alexander) with fund-specific parameters. You produce quarterly projections for the full fund life with sensitivity analysis on key variables.

## When This Skill Is Invoked

The user runs `/fund cashflow-forecast <data>` providing fund details such as commitments, vintage year, strategy type, current NAV, and historical call/distribution patterns. Input may be a file, pasted text, or inline parameters.

---

## Phase 1: Data Ingestion

### 1.1 Read the Input

Accept input from one of these sources:
- **File path** — Use the Read tool to read a file containing fund data (CSV, text, markdown, or prior fund review output)
- **Pasted text** — Accept text pasted directly into the chat describing fund parameters
- **Inline parameters** — Accept natural language description (e.g., "$500M PE buyout fund, 2023 vintage, 40% called, $120M NAV")

### 1.2 Extract Fund Parameters

Extract or ask for the following. If critical parameters are missing, ask the user before proceeding. Use sensible defaults (documented below) for optional parameters.

**Required Parameters:**

| Parameter | Description | Example |
|-----------|-------------|---------|
| **Fund Name** | Legal or working name of the fund | "Obrelund Growth Partners Fund VII" |
| **Total Commitments** | Aggregate LP + GP commitments | $500,000,000 |
| **Strategy Type** | PE Buyout, VC, Real Estate, Credit, Hedge, FoF | PE Buyout |
| **Vintage Year** | Year of first capital call or final close | 2023 |

**Optional Parameters (defaults applied if not provided):**

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Current NAV** | Latest reported net asset value | $0 if new fund; ask if vintage > 1 year ago |
| **Capital Called to Date** | Aggregate capital called | $0 if new fund |
| **Distributions to Date** | Aggregate distributions returned | $0 if new fund |
| **Fund Term** | Total fund life in years | Strategy-dependent (see 1.3) |
| **Expected Growth Rate** | Annual NAV growth rate | Strategy-dependent (see 1.3) |
| **GP Commitment %** | GP share of total commitments | 2% for PE/RE, 1% for VC, 5% for Credit |
| **Management Fee Rate** | Annual management fee for net return calculation | 1.75% (PE), 2.0% (VC), 1.25% (RE), 1.5% (Credit) |
| **Carried Interest Rate** | Carry percentage for net return calculation | 20% |
| **Preferred Return** | Hurdle rate | 8% (PE/RE), 0% (VC), 6% (Credit) |

### 1.3 Default Parameters by Strategy Type

Apply these defaults when the user does not provide specific parameters:

#### PE Buyout
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Fund Term | 10 years + 2x 1-year extensions | Industry standard |
| Contribution Rate (quarterly) | 5.0% of unfunded in early years | Moderate deployment pace |
| Bow Factor (contributions) | 2.5 | Front-loaded draw pattern peaking years 2-4 |
| Distribution Rate (annual) | 25% of NAV starting year 4-5 | Exits begin mid-life |
| Growth Rate | 10% annual (8-12% range) | Long-term PE median |
| Peak Investment Year | Year 3-4 | Investment period midpoint |
| J-Curve Trough | Year 2-3 | Fees drag before value creation |

#### Venture Capital
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Fund Term | 10-12 years + extensions | Longer hold periods |
| Contribution Rate (quarterly) | 4.0% of unfunded | Slower deployment, staged investing |
| Bow Factor (contributions) | 2.0 | More gradual deployment |
| Distribution Rate (annual) | 20% of NAV starting year 5-7 | Later exits (IPO/M&A timing) |
| Growth Rate | 12% annual (higher variance, 5-20%) | Higher risk/return profile |
| Peak Investment Year | Year 3-5 | Extended investment period |
| J-Curve Trough | Year 3-4 | Deeper J-curve, longer recovery |

#### Real Estate
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Fund Term | 8-10 years + extensions | Moderate hold periods |
| Contribution Rate (quarterly) | 6.0% of unfunded | Faster deployment for deals |
| Bow Factor (contributions) | 3.0 | Front-loaded acquisitions |
| Distribution Rate (annual) | 15% of NAV starting year 2-3 (income) + exit distributions year 5+ | Current income from rent/operations |
| Growth Rate | 8% annual (6-10% range) | Real estate appreciation + income |
| Income Yield | 4-6% annual on NAV | Rental income distributions |

#### Credit / Debt
| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Fund Term | 5-7 years + extensions | Shorter duration |
| Contribution Rate (quarterly) | 8.0% of unfunded | Fast deployment |
| Bow Factor (contributions) | 3.5 | Rapid front-loaded deployment |
| Distribution Rate (annual) | 30% of NAV starting year 1 (current income) | Interest/coupon income begins immediately |
| Growth Rate | 6% annual (5-8% range) | Yield-driven returns |
| Income Yield | 6-8% annual on NAV | Interest income distributions |

---

## Phase 2: Endowment Model (Takahashi-Alexander) Implementation

### 2.1 Model Overview

The Endowment Model (developed by Dean Takahashi and Seth Alexander at Yale University) projects private fund cash flows using a deterministic model based on fund age, strategy, and a "bow" factor that shapes the contribution and distribution curves.

### 2.2 Core Formulas

#### Contribution Model

For each quarter `t` (where `t` starts at 1 for the first quarter of the fund):

```
Annual_Contribution_Rate(t) = RC × (Fund_Age(t) / L)^B × e^(-B × Fund_Age(t) / L)
```

Where:
- `RC` = Base annual contribution rate (strategy-dependent)
- `Fund_Age(t)` = Years since first close at quarter `t`
- `L` = Expected fund life in years (strategy-dependent)
- `B` = Bow factor controlling the shape of the contribution curve
- `e` = Euler's number (2.71828...)

Quarterly contribution:
```
Contribution(t) = Annual_Contribution_Rate(t) / 4 × Remaining_Unfunded(t-1)
```

Constraint: Cumulative contributions cannot exceed total commitments.

#### NAV Model

```
NAV(t) = NAV(t-1) × (1 + Quarterly_Growth_Rate) + Contribution(t) - Distribution(t)
```

Where:
- `Quarterly_Growth_Rate` = Annual_Growth_Rate / 4 (simplified) or `(1 + Annual_Rate)^0.25 - 1` (compounded)

#### Distribution Model

```
Annual_Distribution_Rate(t) = RD × (Fund_Age(t) / L)^D_exp × (1 - e^(-Fund_Age(t) / L))
```

Where:
- `RD` = Base annual distribution rate (strategy-dependent)
- `D_exp` = Distribution exponent (typically 2-3, creating delayed distribution start)
- Distributions are applied as a percentage of beginning-of-period NAV

Quarterly distribution:
```
Distribution(t) = Annual_Distribution_Rate(t) / 4 × NAV(t-1)
```

Constraint: Distributions cannot exceed NAV. If calculated distribution > NAV, cap at NAV (full liquidation).

For strategies with current income (RE, Credit):
```
Income_Distribution(t) = Income_Yield / 4 × NAV(t-1)
Total_Distribution(t) = Income_Distribution(t) + Capital_Distribution(t)
```

### 2.3 Quarterly Projection Loop

For each quarter from current period through fund termination:

1. Calculate contribution amount using contribution model
2. Update unfunded commitment: `Unfunded(t) = Unfunded(t-1) - Contribution(t)`
3. Calculate growth on existing NAV
4. Calculate distribution amount using distribution model
5. Update NAV: `NAV(t) = NAV(t-1) × (1 + g) + Contribution(t) - Distribution(t)`
6. Record all values for the quarter

### 2.4 Adjustments for Existing Funds

If the fund is not new (capital has already been called):

1. Set `Contribution_to_Date` and `Distribution_to_Date` from user input
2. Set `Current_NAV` from user input
3. Begin projection from the current quarter
4. Adjust the contribution curve to account for capital already deployed
5. `Remaining_Unfunded = Total_Commitments - Contribution_to_Date`

---

## Phase 3: Sensitivity Analysis

### Sensitivity Variables

Required sensitivity analysis on:
- Drawdown pace: +/-20% of base case
- Exit timing: +/-12 months
- Exit multiples: +/-0.5x MOIC
- Default rate (credit funds): +/-5%
Present results showing which variable has the largest impact on IRR.

### 3.1 Scenarios

Run the model under three scenarios for each key variable:

| Variable | Base Case | Downside | Upside |
|----------|-----------|----------|--------|
| **Growth Rate** | Strategy default | Default - 2% | Default + 2% |
| **Contribution Pace** | Strategy default | 75% of default rate (slower) | 125% of default rate (faster) |
| **Exit Timing** | Strategy default | Distributions begin 2 years later | Distributions begin 1 year earlier |

### 3.2 Key Output Metrics per Scenario

For each scenario, calculate:

| Metric | Formula |
|--------|---------|
| **Total Contributions** | Sum of all quarterly contributions |
| **Total Distributions** | Sum of all quarterly distributions |
| **Final NAV** | NAV at fund termination |
| **TVPI (Total Value to Paid-In)** | (Total Distributions + Final NAV) / Total Contributions |
| **DPI (Distributions to Paid-In)** | Total Distributions / Total Contributions |
| **RVPI (Residual Value to Paid-In)** | Final NAV / Total Contributions |
| **Net IRR** | Internal rate of return on LP cash flows (contributions negative, distributions positive) |
| **J-Curve Trough** | Quarter and amount of lowest cumulative net cash flow |
| **Breakeven Quarter** | Quarter when cumulative distributions first exceed cumulative contributions |
| **Peak Unfunded** | Maximum outstanding unfunded commitment |

### 3.3 Unfunded Commitment Projection

Track unfunded commitments over time for LP liquidity planning:

```
Unfunded(t) = Total_Commitments - Cumulative_Contributions(t)
```

Flag the quarter when unfunded commitments are projected to reach zero (fully called).

---

## Phase 4: Generate Output File

### 4.1 Compile the Cash Flow Forecast Report

Generate `CASHFLOW-FORECAST-[fund]-[date].md` with the following structure:

```markdown
# Capital Call & Distribution Forecast

> DISCLAIMER: This cash flow forecast is AI-generated and does not constitute
> financial, tax, or investment advice. It is intended for informational and
> educational purposes only. Cash flow projections are inherently uncertain
> and based on simplified models with assumed parameters. The Endowment Model
> (Takahashi-Alexander) is a deterministic model that does not capture the
> full range of possible outcomes. Actual results will differ materially from
> projections. This forecast should not be used as the sole basis for investment
> decisions or liquidity planning. Consult qualified financial advisors and
> use scenario ranges rather than point estimates.

---

## Fund Parameters

| Parameter | Value |
|-----------|-------|
| Fund Name | [name] |
| Strategy Type | [type] |
| Total Commitments | $[amount] |
| Vintage Year | [year] |
| Current NAV | $[amount] |
| Capital Called to Date | $[amount] ([X]% of commitments) |
| Distributions to Date | $[amount] |
| Remaining Unfunded | $[amount] |
| Assumed Growth Rate | [X]% annual |
| Fund Term | [X] years |
| Model | Yale (Takahashi-Alexander) |

---

## Forecast Summary — Base Case

| Metric | Value |
|--------|-------|
| Projected Total Contributions | $[amount] |
| Projected Total Distributions | $[amount] |
| Projected Final NAV | $[amount] |
| Projected Gross TVPI | [X.Xx] |
| Projected Net TVPI | [X.Xx] |
| Projected Net IRR | [X.X]% |
| Projected DPI | [X.Xx] |
| Projected RVPI | [X.Xx] |
| J-Curve Trough | Quarter [X] (Year [Y]): -$[amount] |
| Breakeven Quarter | Quarter [X] (Year [Y]) |
| Fully Called Quarter | Quarter [X] (Year [Y]) |

---

## Sensitivity Analysis

| Scenario | Growth Rate | TVPI | Net IRR | DPI | Breakeven |
|----------|-----------|------|---------|-----|-----------|
| Upside (+2% growth) | [X]% | [X.Xx] | [X.X]% | [X.Xx] | Year [Y] |
| **Base Case** | **[X]%** | **[X.Xx]** | **[X.X]%** | **[X.Xx]** | **Year [Y]** |
| Downside (-2% growth) | [X]% | [X.Xx] | [X.X]% | [X.Xx] | Year [Y] |
| Slow Deployment | [X]% | [X.Xx] | [X.X]% | [X.Xx] | Year [Y] |
| Fast Deployment | [X]% | [X.Xx] | [X.X]% | [X.Xx] | Year [Y] |
| Late Exits | [X]% | [X.Xx] | [X.X]% | [X.Xx] | Year [Y] |

---

## Quarterly Projections — Base Case

| Quarter | Year | Contribution | Distribution | Net Cash Flow | Cumulative Net | NAV | Unfunded |
|---------|------|-------------|-------------|--------------|----------------|-----|----------|
| Q1 | [Y1] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] |
| Q2 | [Y1] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] |
| Q3 | [Y1] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] |
| Q4 | [Y1] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] |
[...continue for all quarters through fund termination...]

---

## Annual Summary — Base Case

| Year | Contributions | Distributions | Net Cash Flow | Year-End NAV | Unfunded | DPI |
|------|--------------|--------------|--------------|-------------|----------|-----|
| [Y1] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | [X.Xx] |
| [Y2] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | [X.Xx] |
[...continue for all years...]

---

## Unfunded Commitment Projection

| Milestone | Quarter | Year | Unfunded Amount | % of Commitments |
|-----------|---------|------|----------------|-----------------|
| Start | Q1 Y1 | [year] | $[amount] | 100% |
| 25% Called | [Q] [Y] | [year] | $[amount] | 75% |
| 50% Called | [Q] [Y] | [year] | $[amount] | 50% |
| 75% Called | [Q] [Y] | [year] | $[amount] | 25% |
| Fully Called | [Q] [Y] | [year] | $0 | 0% |

---

## J-Curve Analysis

The J-curve represents the pattern of negative cumulative net cash flows in
early fund years (due to capital calls exceeding distributions) before
turning positive as exits and distributions begin.

| Phase | Period | Description |
|-------|--------|-------------|
| Drawdown | Years 1-[X] | Net capital outflows as fund deploys capital |
| Trough | Year [X] | Maximum negative cumulative cash flow of -$[amount] |
| Recovery | Years [X]-[Y] | Distributions begin to offset contributions |
| Breakeven | Year [X] | Cumulative distributions exceed cumulative contributions |
| Harvest | Years [X]-[Y] | Net positive cash flows as exits accelerate |

---

## Model Assumptions and Limitations

1. The Endowment Model is deterministic — it projects a single path, not a probability distribution
2. Growth rates are applied uniformly; actual returns vary by investment and vintage
3. Contribution and distribution timing follows smooth curves; actual calls/distributions are lumpy
4. No modeling of recycling provisions, recallable capital, or management fee netting
5. Tax implications (withholding, UBTI, ECI) are not modeled
6. Currency effects are not modeled for non-USD funds
7. The model assumes the GP deploys capital per strategy norms; actual pace may differ materially
8. Past performance data used for default parameters is not predictive of future results

---

## Recommended Next Steps

1. [ ] Validate fund parameters with the fund administrator or GP
2. [ ] Compare projections against GP's own forecasts (if available)
3. [ ] Use the range of scenarios (not just base case) for liquidity planning
4. [ ] Update the forecast quarterly as actual data becomes available
5. [ ] Run `/fund performance-calc` to calculate actual performance metrics from historical cash flows
6. [ ] Run `/fund waterfall-review` to analyze how projected distributions would flow through the waterfall
```

### 4.2 Present to User

After generating the output:

1. Confirm the file was generated with its absolute path
2. State the base case projected TVPI and net IRR
3. Highlight the J-curve trough quarter and amount
4. Show the sensitivity range (downside to upside TVPI)
5. State when the fund is projected to break even
6. Suggest: "Run `/fund performance-calc` to calculate actual realized metrics. Run `/fund waterfall-review` to model how these projected distributions flow through the waterfall."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No data provided | Ask user to provide fund parameters (at minimum: fund name, total commitments, strategy type, vintage year) |
| Strategy type not recognized | Ask user to select from: PE Buyout, VC, Real Estate, Credit, Hedge, FoF; default to PE Buyout if unclear |
| Commitment amount missing | Cannot proceed without total commitments; ask user to provide |
| Vintage year unreasonable | Flag if vintage year is more than 15 years ago (fund likely terminated) or in the future; confirm with user |
| Current NAV exceeds commitments | Unusual but possible for high-performing funds; note and proceed; flag in output |
| Distributions exceed called capital | Fund has returned more than invested; note strong performance; adjust model accordingly |
| Negative growth rate requested | Accept for stress testing; warn that projections will show capital destruction |
