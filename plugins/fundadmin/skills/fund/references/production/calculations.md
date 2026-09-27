# Deterministic calculation workpapers

`scripts/fund_calculations.py` is an offline, Python 3.8+ standard-library Decimal engine. Packaging places it at `fund/scripts/fund_calculations.py`, alongside the installed fund skill. It does not access networks, accounts, wallets or payment systems. It does not determine legal entitlements, tax treatment or contractual terms.

## Run and reproduce

The fixture files wrap a `request` and `expected` object for tests; extract the request when executing a fixture:

```bash
python3 -c 'import json; print(json.dumps(json.load(open("tests/fixtures/calculations/waterfall.json"))["request"]))' | python3 scripts/fund_calculations.py
python3 -m unittest discover -s tests -p test_fund_calculations.py -v
```

For ordinary use, save the following request as `calculation-request.json`, then run `python3 scripts/fund_calculations.py --input calculation-request.json`. Without `--input`, JSON is read from stdin. Results are printed to stdout; the helper writes no files. Exit code 0 means a workpaper was produced, not that every requested metric is defined or check passed. Exit code 2 returns a structured `error` object for invalid requests. Inspect operation statuses and null values before using results. Engine version 1.1.0 adds the financial-review operations below; the request envelope and schema version 1 remain unchanged.

```json
{
  "operation": "allocate",
  "config": {"currency": "GBP", "decimal_places": 2, "rounding": "ROUND_HALF_EVEN"},
  "inputs": {
    "total": "100.00",
    "participants": [
      {"id": "LP-A", "weight": "1"},
      {"id": "LP-B", "weight": "1"},
      {"id": "LP-C", "weight": "1"}
    ]
  }
}
```

The resulting allocations are 33.34, 33.33 and 33.33. The workpaper includes the original request, engine and schema versions, Decimal precision, a SHA-256 hash of the sorted compact JSON request, result components and residuals. No timestamp or randomness is included. Store the request, stdout, source document/page references and the script version together. Replay the returned `request` through the same engine version to reproduce the complete workpaper. The hash identifies the request representation; it does not authenticate source evidence. Numerically equivalent differently formatted strings can have different hashes.

The library API is `calculate(request)`, returning a JSON-safe dict or raising `CalculationError`. Input objects are not mutated. Decimal results are strings, never binary floats. The calculation context has 64 significant digits and is independent of the caller's Decimal context. Finite precision still applies to repeating divisions and fractional powers; the engine does not claim exact real arithmetic.

## Validation and conventions

- Requests require exactly `operation`, `inputs`, `config`. Unknown keys, missing fields and duplicate JSON keys are rejected. Row lists contain 1–1000 elements. CLI requests are at most 1,000,000 characters.
- Use decimal strings for amounts and rates. Integers and finite JSON decimal numbers parsed directly into Decimal also work; Python floats, booleans, whitespace, separators, NaN and infinities do not. Inputs permit at most 28 significant digits, exponent -18 through 18 and absolute magnitude at most 10²⁴.
- Config requires `currency` (three uppercase letters), `decimal_places` (integer 0–8) and `rounding` (`ROUND_HALF_EVEN`, `ROUND_HALF_UP` or `ROUND_DOWN`). The currency is a label, not an ISO registry validation or automatic minor-unit lookup. All inputs must already be in that one currency. There is no implicit FX conversion or currency mixing.
- Monetary outputs are rounded only at the documented boundary. Rates and ratios retain precision; a ratio of `0.1` is 10%. Rounding is not a tolerance policy: comparisons and materiality require independently specified thresholds.
- Dates are validated ISO calendar dates. There is no business-day/holiday calendar. Monetary signs and rates are validated for each operation, rather than interpreting arbitrary negatives as reversals.

## Operations

All fields below are required unless explicitly marked optional. Each operation returns intermediate data as part of `result`.

### `allocate`

Inputs: `total`, `participants: [{id, weight}]`. Total and weights are non-negative, weights must sum positive, IDs must be unique, and total must already be an exact multiple of the configured unit. Each exact proportional share is floored to the currency unit. Remaining units go to the largest fractional remainders; equal remainders use lexical ID order. Allocation totals conserve the input exactly. This apportionment rule deliberately overrides ordinary rounding for individual allocations; the workpaper identifies the rule and each adjustment.

Eligibility, exclusions, caps, equalisation and recallability must be resolved before supplying weights. This is not a commitment-limit engine. Use separate pools where governing terms require them. It never rescales against a silently assumed fund size.

Each participant optionally accepts `reported_amount` (non-negative exact currency units, or null). The row returns that amount, `difference` (reported less rounded allocation), and `comparison_status`: `pass` for equality, `fail` for a non-zero difference, `unverifiable` for absent/null reported amounts. Overall `comparison_status` is `fail` if any row fails, otherwise `unverifiable` if any row is unknown, otherwise `pass`. The fixed comparison `tolerance` is zero currency units. With GBP/two places, 33.34/33.33/33.33 passes for the £100 equal-weight example; 33.33/33.33/33.34 against IDs A/B/C fails despite conserving total. Keep stable IDs. Neither percentage tolerances against raw thirds nor a blanket £/$1 allowance apply. Report different contractual rounding methods as unsupported by this allocation check, retaining the differences for review rather than declaring a contractual breach.

**Stated-method rounding difference.** A document may state a different derivation that the helper can replicate, typically a true-up equal to each participant's allocation of the cumulative total less its allocation of the amount previously called. Replicate it with `allocate` on each component and `arithmetic` for the difference. When (1) the method is stated in the document, (2) the replication reproduces every reported amount exactly and reconciles to the total, and (3) each participant's difference from the direct `allocate` of the line total is at most one configured currency unit and the differences net to zero, the review skills record an informational method note with both workpapers: not a FAIL, not a High Risk finding, not a `capital_call_status` blocker and no effect on any dimension score. If any condition fails, the direct comparison's FAIL stands. The helper itself is unchanged: `allocate` still reports the direct comparison with zero tolerance, and `capital_call_status` applies no score cap; the scores and finding lists are the skill's inputs. Example (USD, 0 places, commitments 150/75/100/50/200 of 575): the cumulative method gives a USD 8,100,000 true-up of 2,113,044 / 1,056,521 / 1,408,696 / 704,348 / 2,817,391, and a direct allocation gives 2,113,043 / 1,056,522 / 1,408,696 / 704,348 / 2,817,391 — a method note, not a FAIL.

### `capital_call_status`

Inputs: `scores: {calculation_accuracy, completeness, lpa_compliance, wire_quality}`, `high_risk_findings`, `wire_changed`, `required_unknowns`, `failed_checks`. Scores are decimal strings/integers from 1–10 or null; the three finding lists contain 0–1000 non-empty labels (each at most 200 characters). Include all unresolved findings; an empty list asserts no findings in that category, not that a missing check passed. `wire_changed` is a boolean or null (unknown); false requires supporting comparison evidence.

Weights are 0.35/0.25/0.25/0.15. Output `raw_score`, `score` rounded to one decimal with ROUND_HALF_UP independently of monetary config, and `dimensions` with weighted components. A null dimension makes both aggregate scores null, without renormalising known dimensions. `blockers` records each high-risk finding, failed check, required unknown, changed/unknown wire and missing score. `status` is `blocked` when any blocker exists, otherwise `human_review_required`. `payment_approved` is always false. Scores 10/10/10/4 yield 9.1 but a high-risk wire finding still blocks. No aggregate or result authorises payment or processing; retain any later authorised human decision separately in the report contract.

### `ytd_income`

Inputs: `year_start`, `period_end`, `periods: [{start, end, income}]`, `reported_ytd`. All dates are ISO; intervals are start-inclusive/end-exclusive. Supply the actual fiscal-year start and day after the statement end, a window of 1–366 days. Rows may arrive unordered but must not overlap or extend outside the window. Signed income and `reported_ytd` accept null for unknown; reported YTD must already use configured currency units.

Reconcile the same investor, economic/tax allocation, currency, income definition and fee basis before constructing the request; the helper cannot verify these source facts. Never add cumulative YTD columns as period figures. Sum signed period income, then round once using configured precision. Output includes `observed_income` (only known amounts, never a substitute YTD), `expected_ytd`, `reported_ytd`, `difference`, `missing_periods`, `unknown_periods`, and `status`. Any gap or null income makes expected YTD and difference null; absent reported YTD makes difference null. Null difference means `unverifiable`, otherwise zero means `pass` and non-zero means `fail`. Overlap/invalid dates are rejected. Q1 −100 plus Q2 +60 and reported YTD −40 pass. A Q2-only input is unverifiable, never assumed to have zero Q1 income.

This operation sums income, not returns. Compound evidenced TWR sub-period returns using `arithmetic`; −10% and +6% give −4.6%. Missing periods or unknown return methodology are unverifiable; neither income nor returns can be validated by a sign comparison. IRRs cannot be compounded as TWR.

### `rollforward`

Inputs: `opening`, `contributions`, `income`, `gains`, `fees`, `distributions`; optional `reported_closing`. Formula: opening + contributions + income + gains - fees - distributions. Opening, income, gains and reported closing may be signed; other components must be non-negative. Round once at closing. Difference is reported closing less calculated rounded closing, rounded to the configured unit. A zero difference is agreement at that precision only. Do not supply income already net of fees and subtract those fees again.

### `fees`

Inputs: `opening_offset`, `offset_policy` (`carry_forward` or `expire`), `periods: [{start, end, basis, annual_rate, day_count, offset_generated, offset_rate}]`.

Periods must be ordered and non-overlapping, with start inclusive and end exclusive. Gaps are permitted and accrue no fee. Split the input schedule at every basis, rate, investor or offset-policy change. Supported conventions are ACT/365F, ACT/360 and ACT/ACT (actual days split by calendar year, including leap years). Unsupported conventions such as 30/360, equal-quarter contractual billing or daily compounding must not be relabelled as one of these.

Gross fee = basis × annual rate × year fraction. Available offset = prior carried balance + offset generated × offset rate. Applied offset is limited to gross fee; no negative fee arises. Excess either carries to the next supplied period or expires at the end of this period. Opening offset is already eligible and is not multiplied by the rate again. Offset balances retain precision. Net fees round per period; total is the sum of rounded period fees. Fees, bases and offsets must be non-negative; rates are 0–1. The engine does not infer the eligibility or accounting date of an offset.

### `waterfall`

Inputs: `model: "whole_fund_single_event"`, `proceeds`, `unreturned_capital`, `preferred_due`, `carry_rate`, `catch_up` (`none` or `full`). Amounts are non-negative and proceeds must be exact currency units; 0 ≤ carry rate < 1.

This restricted whole-fund model distributes one LP pool: return outstanding LP capital, pay outstanding LP preference, optionally pay 100% GP catch-up, then split remaining profit at the carry rate. For full catch-up the target is preference paid × carry / (1 - carry). GP cash rounds once; LP cash is proceeds less rounded GP cash, with the LP rounding residual explicitly reported. Raw tiers and unpaid amounts are retained. GP here means carry only, not return on GP co-investment.

`preferred_due` is an independently supported accrued entitlement, not automatically derived from a guessed holding period. Full catch-up assumes no earlier GP carry/catch-up on the profit pool represented by that preference. Repeated calls do not constitute a cumulative waterfall state machine. Prior distributions must not be fed back as a new fresh pool without a separately verified entitlement reconciliation.

Unsupported: American/deal-by-deal waterfalls, partial catch-up, prior carry/catch-up true-ups, GP co-investment, multiple classes/hurdles, recycling, escrow, clawback, preferred-return compounding schedules, tax and LPA interpretation. Unknown fields or alternative models are rejected. Identify these cases and leave the result uncalculated; do not approximate them with this model.

### `metrics`

Inputs: `paid_in`, `distributions`, `nav`, `invested_capital`, all non-negative. DPI = distributions / paid-in; RVPI = NAV / paid-in; TVPI = (distributions + NAV) / paid-in; MOIC uses invested capital as denominator. Zero denominators produce null and an `undefined` list. Missing NAV or invested capital is not zero. For DPI-only inputs, use an explicit arithmetic division. Gross and net series must be sourced and labelled separately; no automatic fee/carry subtraction is performed.

### `dated_irr`

Inputs: `cashflows: [{date, amount}]`, `day_count: "ACT/365F"`, `lower_rate`, `upper_rate`. Bounds must satisfy -1 < lower < upper ≤ 10⁶. Contribution amounts are negative, distribution amounts positive. Include terminal NAV once, dated at its valuation date, and document whether the series is gross or net. Dates may arrive unordered; same-date flows are aggregated before sign analysis and zero totals removed.

NPV = sum(amount / (1 + rate)^(actual days since first non-zero date / 365)). For one sign change, there is at most one root in the admissible domain; bracketed bisection finds it inside the explicitly supplied bounds. Success requires an exact zero or both a rate interval ≤10⁻²⁴ and absolute NPV ≤10⁻²⁴ × sum of absolute cash flows. At most 256 iterations are executed. The workpaper includes bounds, endpoint NPVs and the full trace. Decimal fractional powers are numerical approximations.

Statuses:

- `unique`: a converged rate is returned.
- `ambiguous_multiple_sign_changes`: no rate; this is a conservative ambiguity flag, not proof that multiple roots actually exist. For example -100, +230, -132 at annual intervals has roots 10% and 20%; neither is selected.
- `undefined_no_sign_change`: no admissible root for the supplied non-zero cash flows.
- `indeterminate_all_zero`: the aggregated schedule is all zero, so every rate has zero NPV.
- `root_outside_bounds`: the unique root is not bracketed by the supplied interval; this is not a global claim of no root.
- `not_converged`: no published rate; iteration trace retained.

The engine does not invent transaction dates, root-search bounds, missing NAV or net cash flows. It does not enumerate non-conventional roots or provide TWR as a dedicated operation.

### `ks_pme`

Inputs: `valuation_date`, `cashflows: [{date, contribution, distribution, index}]`, `index_end`, `benchmark_id`, `benchmark_currency`, `cashflow_basis`, `nav_basis`; optional `nav` (absent/null means unknown). Cash-flow amounts are non-negative magnitudes; zero must be explicit when no contribution or distribution occurred. Index levels must be positive and from one evidenced total-return series. Dates cannot follow valuation; repeated dates must have identical index levels, including the terminal level. Same-date rows may contain separate real transactions. NAV belongs only in the separate field, never duplicated as a distribution or flow row.

The benchmark currency must equal `config.currency`, and `cashflow_basis`/`nav_basis` must both be `gross` or both `net`. These are declared labels, not source verification. Record the precise benchmark ID/version/provider, total-return convention, valuation-date NAV evidence, dates, source locators and any reviewer-approved non-trading-day convention beside the workpaper. Resolve any FX conversion externally with evidence before calling; there is no implicit conversion, benchmark selection, interpolation or price-to-total-return adjustment.

For terminal date T, `contributions_fv = Σ C_i × index_end / index_i`, `distributions_fv = Σ D_i × index_end / index_i`, `numerator = distributions_fv + NAV_T`, `pme = numerator / contributions_fv`. No currency rounding occurs in intermediate adjusted values or the ratio. Output also includes per-row index/factor/adjusted amounts, method and valuation date. `status` is `calculated`, `unknown_nav` (PME/numerator null), or `undefined_no_contributions` (PME null). Explicit zero NAV supports fully realised funds and is distinct from missing NAV. All three statuses produce a workpaper/exit 0; invalid dates, negative amounts, zero indices, basis/currency conflicts and unknown fields are errors/exit 2.

Independent acceptance examples: a flat index, C=100, D=0, NAV=110 gives 1.1; with D=120 and evidenced NAV=0 it gives 1.2. With C=100 at index 100, D=30 at index 150, terminal index 200 and NAV=180, adjusted contributions are 200, adjusted distributions 40 and PME 1.1. Missing NAV must never become 0.

Methodology reference: Hendrix and Medhat, *Understanding Private Fund Performance* (July 2024), [Table 1 and section 2.5, page 10](https://www.dimensional.com/chmedia/389443/source/understanding-private-fund-performance.pdf), verified 21 September 2026. Qualified review of the method and its applicability remains required. Passing arithmetic tests is not financial-method sign-off, and PME does not establish peer quartiles.

### `forecast` and `scenario`

Forecast inputs: `opening_nav`, `unfunded`, `assumptions` (non-empty description up to 200 characters), `periods: [{date, contribution, growth_rate, distribution_rate, fees}]`. Dates must increase. Each rate applies to its whole modelled period, not per annum. Growth must be at least -100%; the distribution rate is 0–1. Contributions and fees are non-negative. Contributions cannot exceed remaining unfunded.

For each period: gain = opening NAV × growth rate; available NAV = opening NAV + gain + contribution - fees; distribution = available NAV × distribution rate; closing NAV = available NAV - distribution. Negative available NAV is an error, requiring an explicit funding model. Growth is earned only on opening NAV, and all period contributions are available for the distribution. LP net cash flow = distribution - contribution; fees are already deducted from NAV. Raw balances roll forward without display rounding. Rounded display figures may not add exactly; use raw workpapers to reconcile them.

Scenario inputs: `scenarios: [{name, forecast}]`, with unique names and complete forecast inputs per scenario. Every schedule is supplied explicitly. No silent base/upside/downside calibration, industry defaults, annual-to-quarter conversion, borrowing, recycling, carry, probabilities, Monte Carlo or breakeven solver is included. This is not a Takahashi-Alexander calibration. Disclose external schedule assumptions and use separate supported fee/waterfall/metrics operations only where their assumptions match, without double counting. Terminal forecast NAV is a remaining asset, not a cash distribution unless explicitly liquidated.

### `arithmetic`

Inputs: `steps: [{id, operator, operands, round?}]`. IDs are unique. Operators are `add`, `subtract`, `multiply`, `divide`; subtract and divide require exactly two operands. Operands are decimal values or `{ "ref": "previous-step-id" }`. Optional boolean `round` applies configured monetary precision after that step. Division by zero, future references and results over 10⁴⁸ in magnitude are rejected. There is no `eval`, executable formula text or implicit tax logic.

Use this for source-supported per-unit scaling, reconciliation, netting and withholding arithmetic. A correct multiplication does not verify the withholding rate, tax basis, exemptions or classification. The same principle applies to analytical formulas retained in skill templates: execute the explicit formula only when all inputs and its applicability are evidenced.

## Skill integration and verification scope

The eleven owned source skills instruct execution of this helper and preservation of workpapers. Installed skills resolve `../fund/scripts/fund_calculations.py`; the source checkout uses `scripts/fund_calculations.py`. A missing helper or unsupported model means the numerical result is uncalculated. Guessed LPA sections, implicit economic defaults and unqualified ILPA-compliant claims are removed. The main hardening agent supplies the separate shared policy/output block; none is duplicated here.

Tests cover known outputs, rounding residuals, fee day counts and offsets, strict rejection, zero denominators, negative returns, leap-year IRR, ambiguous IRR, conservation, scenario funding limits, JSON CLI errors and replay. Packaging and the generated `plugin/` tree are intentionally outside this change. No live-money actions are performed.

`tests/test_financial_rules.py` adds explicit expected outputs for the readiness, allocation, NAV-inclusive PME and signed YTD review counterexamples, including missing evidence and replay. These are deterministic helper regressions, not installed-host behavioural qualification or professional financial-method approval.
