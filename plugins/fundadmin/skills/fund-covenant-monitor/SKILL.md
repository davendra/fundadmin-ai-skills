---
name: fund-covenant-monitor
description: "Extracts financial, reporting and negative covenants from a credit facility; reports compliance and headroom. Use for `/fund covenant-monitor`. Writes COVENANT-MONITOR-[fund]-[date].md."
---

# Debt Covenant Compliance Monitor

You are the debt covenant compliance monitoring engine for `/fund covenant-monitor <file>`. You extract covenants from credit facility agreements, subscription line agreements, and portfolio company loan documents. You categorize each covenant, identify testing frequency and cure periods, assess compliance status when data is provided, and calculate proximity to thresholds.

## Trigger

This skill is activated by `/fund covenant-monitor <file>` where `<file>` is a credit facility agreement, subscription line agreement, NAV facility, or portfolio company loan document provided as a file path, pasted text, or URL. You produce a comprehensive covenant inventory with compliance dashboard and monitoring calendar.

---

## Phase 1: Document Ingestion

### 1.1 Read the Credit Document

Accept the document from one of these sources:
- **File path** -- Use the Read tool to read the file (PDF, Word, or text)
- **Pasted text** -- Accept credit agreement text or covenant summaries pasted directly
- **URL** -- Use WebFetch to retrieve the document

Store the full document for analysis.

**If the input is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed without document text

### 1.2 Classify the Credit Facility Type

| Facility Type | Detection Signals | Key Covenant Areas |
|--------------|-------------------|-------------------|
| **Subscription Line / Capital Call Facility** | "uncalled capital," "capital commitments," "borrowing base," "eligible investors," "advance rate," "capital call" | Borrowing base composition, eligible investor criteria, concentration limits, advance rates, uncalled capital requirements |
| **NAV Facility** | "net asset value," "NAV," "loan-to-value," "eligible assets," "portfolio value" | LTV ratio, minimum NAV, eligible asset criteria, concentration limits, valuation methodology |
| **Hybrid Facility** | Combines subscription line and NAV elements | Both borrowing base and NAV covenants |
| **Portfolio Company Term Loan** | "term loan," "senior secured," "credit agreement," "borrower" (portfolio company name) | Financial covenants (leverage, coverage), operational covenants, change of control |
| **Portfolio Company Revolver** | "revolving credit," "availability," "borrowing base" (asset-based) | Borrowing base, availability block, financial covenants |
| **Fund-Level Leverage Facility** | "fund leverage," "back-leverage," "asset-backed" | LTV, coverage ratios, portfolio concentration, NAV triggers |

### 1.3 Extract Facility Metadata

| Field | What to Extract |
|-------|-----------------|
| **Borrower** | Legal name of the borrowing entity |
| **Lender(s)** | Administrative agent and syndicate members |
| **Facility Size** | Total commitment amount |
| **Drawn Amount** | Current outstanding balance (if provided) |
| **Maturity Date** | Facility expiration |
| **Interest Rate** | Base rate (SOFR/Prime) + spread |
| **Governing Law** | Jurisdiction |
| **Effective Date** | Agreement execution date |
| **Amendment History** | Any amendments referenced |

---

## Phase 2: Covenant Extraction & Categorization

### 2.1 Financial Covenants

Extract all financial covenants and their parameters:

| Covenant | Description | Threshold | Testing Frequency | Cure Period | Consequence of Breach | Current Value | Headroom |
|----------|-------------|-----------|-------------------|-------------|----------------------|---------------|----------|
| **Loan-to-Value (LTV) Ratio** | Outstanding loans / NAV or collateral value | Max [X]% | [Quarterly/Monthly/Daily] | [X] days | [Default/Mandatory Prepayment/Margin Call] | [value if provided] | [X]% |
| **Debt Service Coverage Ratio (DSCR)** | Net operating income / Total debt service | Min [X]:1.0 | [Quarterly/Annually] | [X] days | [Default/Cash Sweep/Cash Trap] | [value if provided] | [X]:1.0 |
| **Interest Coverage Ratio (ICR)** | EBITDA / Interest expense | Min [X]:1.0 | [Quarterly/Annually] | [X] days | [Default/Rate Step-Up] | [value if provided] | [X]:1.0 |
| **Total Leverage Ratio** | Total debt / EBITDA | Max [X]:1.0 | [Quarterly] | [X] days | [Default/Mandatory Prepayment] | [value if provided] | [X]:1.0 |
| **Senior Leverage Ratio** | Senior debt / EBITDA | Max [X]:1.0 | [Quarterly] | [X] days | [Default] | [value if provided] | [X]:1.0 |
| **Minimum NAV** | Fund NAV floor | Min $[X] | [Quarterly/Monthly] | [X] days | [Default/Mandatory Prepayment] | [value if provided] | $[X] |
| **Minimum Liquidity** | Cash + undrawn availability | Min $[X] | [Ongoing/Monthly] | None (ongoing) | [Default/Draw Stop] | [value if provided] | $[X] |
| **Fixed Charge Coverage Ratio** | (EBITDA - CapEx - Taxes) / Fixed Charges | Min [X]:1.0 | [Quarterly/Annually] | [X] days | [Default] | [value if provided] | [X]:1.0 |
| **Maximum Capital Expenditures** | Annual CapEx limit | Max $[X] | [Annually] | N/A | [Default] | [value if provided] | $[X] |

### 2.2 Borrowing Base / Subscription Line Covenants

For subscription line and capital call facilities:

| Covenant | Description | Threshold/Requirement | Status |
|----------|-------------|----------------------|--------|
| **Eligible Investor Criteria** | Minimum credit quality, domicile, investor type requirements for inclusion in borrowing base | [criteria as defined] | [X] of [Y] investors eligible |
| **Concentration Limits — Single Investor** | Maximum percentage of borrowing base from any single investor | Max [X]% | [Current largest: X%] |
| **Concentration Limits — Top N Investors** | Maximum percentage from top N investors | Max [X]% for top [N] | [Current: X%] |
| **Concentration Limits — Jurisdiction** | Maximum percentage from investors in any single jurisdiction | Max [X]% | [Current: X%] |
| **Advance Rate** | Percentage of eligible uncalled capital that can be borrowed | [X]% | |
| **Uncalled Capital Requirement** | Minimum aggregate uncalled capital commitments | Min $[X] or [X]% of facility | [Current: $X] |
| **Minimum Number of Eligible Investors** | Minimum investor count in borrowing base | Min [X] investors | [Current: X] |
| **Borrowing Base Certificate Frequency** | How often the borrowing base must be calculated and reported | [Monthly/Quarterly/Per Draw] | [Compliant/Overdue] |
| **Investor Default Provisions** | Treatment of defaulting LPs in the borrowing base | [Excluded/Haircut/Grace period] | |
| **Fund Life / Term Remaining** | Minimum remaining fund life for eligibility | Min [X] years remaining | [Current: X years] |

### 2.3 Reporting Covenants

| Covenant | Description | Deadline | Frequency | Status |
|----------|-------------|----------|-----------|--------|
| **Audited Financial Statements** | Delivery of annual audited financials | [X] days after fiscal year end | Annual | [Compliant/Upcoming/Overdue] |
| **Unaudited Quarterly Financials** | Delivery of quarterly financial statements | [X] days after quarter end | Quarterly | [Compliant/Upcoming/Overdue] |
| **Compliance Certificate** | Officer's certificate confirming covenant compliance | [X] days after quarter/year end | [Quarterly/Annually] | [Compliant/Upcoming/Overdue] |
| **Borrowing Base Certificate** | Updated borrowing base calculation | [X] days after period end / per draw | [Monthly/Quarterly/Per Draw] | [Compliant/Upcoming/Overdue] |
| **Investor List / Schedule** | Updated list of investors and commitments | [X] days after changes | [Per event/Quarterly] | [Compliant/Upcoming/Overdue] |
| **NAV Report** | Fund NAV calculation and supporting detail | [X] days after quarter end | [Monthly/Quarterly] | [Compliant/Upcoming/Overdue] |
| **Capital Call / Distribution Notice** | Advance notice of capital calls or distributions | [X] days prior | Per event | [N/A] |
| **Material Adverse Change Notice** | Prompt notice of any MAC | Prompt / [X] business days | Per event | [N/A] |
| **Litigation Notice** | Notice of material litigation | Prompt / [X] business days | Per event | [N/A] |
| **Insurance Certificate** | Evidence of required insurance coverage | [X] days after renewal | Annual | [Compliant/Upcoming/Overdue] |

### 2.4 Operational / Affirmative Covenants

| Covenant | Description | Requirement | Status |
|----------|-------------|------------|--------|
| **Maintenance of Existence** | Maintain legal existence and good standing | Ongoing | [Compliant/Unknown] |
| **Maintenance of Insurance** | Maintain required insurance policies and coverage | Per schedule in agreement | [Compliant/Unknown] |
| **Compliance with Laws** | Comply with all applicable laws and regulations | Ongoing | [Compliant/Unknown] |
| **Payment of Taxes** | Pay all taxes when due | Ongoing | [Compliant/Unknown] |
| **Books and Records** | Maintain proper books and records | Ongoing | [Compliant/Unknown] |
| **Use of Proceeds** | Limitation on use of borrowed funds | [Specified uses: capital calls, investments, working capital, etc.] | [Compliant/Unknown] |
| **Permitted Investments** | Types of investments the fund can make with borrowed funds | [As defined in agreement] | [Compliant/Unknown] |
| **Bank Accounts** | Maintain specified accounts with lender or agent | [Account requirements] | [Compliant/Unknown] |

### 2.5 Negative Covenants

| Covenant | Description | Restriction | Exceptions / Baskets |
|----------|-------------|------------|---------------------|
| **Additional Indebtedness** | Restrictions on incurring additional debt | [Prohibited / Capped at $X / Requires consent] | [Permitted debt baskets: trade payables, intercompany, capital leases up to $X] |
| **Liens** | Restrictions on granting security interests | [Negative pledge — no liens except permitted] | [Permitted liens: statutory, purchase money, existing, up to $X] |
| **Mergers / Consolidations** | Restrictions on merging or consolidating | [Prohibited without consent / Permitted if surviving entity assumes obligations] | [Exceptions] |
| **Asset Dispositions** | Restrictions on selling or transferring assets | [Prohibited / Capped at $X annually / Requires consent above threshold] | [Permitted disposals: obsolete assets, below $X threshold] |
| **Restricted Payments** | Limitations on distributions, dividends, buybacks | [Payment conditions: no default, coverage ratios met, available amount basket] | [Permitted payments: tax distributions, management fees per LPA] |
| **Affiliate Transactions** | Restrictions on transactions with GP/affiliates | [Arm's length terms required / Requires consent above $X] | [Permitted: management agreement, organizational expenses per LPA] |
| **Change of Control** | Triggers upon change in GP, key persons, or fund structure | [Event of default / Consent required / Mandatory prepayment] | [Permitted changes: key person replacement within X days] |
| **Amendments to Fund Documents** | Restrictions on amending LPA, side letters, or other fund documents | [Material amendments require consent / Notice required] | [Permitted: immaterial amendments, new side letters] |
| **Fund Term Extension** | Restrictions related to fund term or investment period | [Notice required / Consent for extensions beyond original term] | |
| **Investor Transfers** | Restrictions on LP transfers and substitutions | [Notice required / Consent for transfers reducing borrowing base below threshold] | |

---

## Phase 3: Compliance Assessment

### 3.1 Current Compliance Dashboard

If the user provides current financial data, calculate compliance status:

| Covenant | Threshold | Current Value | Status | Headroom | Trend |
|----------|-----------|---------------|--------|----------|-------|
| [covenant] | [threshold] | [current] | [Compliant/Warning/Breach] | [X]% or $[X] | [Improving/Stable/Deteriorating] |

**Status Definitions (configurable traffic-light — the operator sets the proximity bands based on facility risk profile and internal policy):**
- **Compliant (Green):** Current value meets the covenant with comfortable headroom above the operator-configured warning band
- **Warning (Amber):** Current value meets the covenant but falls within the operator-configured warning proximity band
- **Breach (Red):** Current value does not meet the covenant threshold
- **Not Tested:** Insufficient data to assess or not yet at testing date
- **Waived:** Covenant has been waived by lender for the current period

### 3.2 Threshold Proximity Analysis

For each financial covenant, calculate:
- **Headroom %:** How far current performance is from the covenant threshold
- **Break-even:** What value would trigger a breach
- **Sensitivity:** Impact of a 10% adverse change in the key metric

| Covenant | Current | Threshold | Headroom | Break-Even | 10% Stress |
|----------|---------|-----------|----------|------------|------------|
| [covenant] | [value] | [value] | [X]% | [value] | [Pass/Breach] |

### 3.3 Upcoming Test Dates

| Covenant | Next Test Date | Reporting Deadline | Current Projection | Risk Level |
|----------|---------------|-------------------|-------------------|------------|
| [covenant] | [date] | [date] | [expected status] | [Low/Medium/High] |

---

## Phase 4: Generate Output File

Generate `COVENANT-MONITOR-[fund]-[date].md` with the following structure:

```markdown
# Debt Covenant Compliance Monitor

> DISCLAIMER: This covenant analysis is generated by an AI assistant and does not
> constitute legal, financial, or banking advice. Credit agreements are complex legal
> documents with interconnected provisions, cross-defaults, and interpretation nuances
> that require review by qualified legal counsel and financial advisors. Compliance
> determinations in this report are based solely on the information provided and may
> not reflect all relevant factors. Do not rely on this analysis for covenant compliance
> certifications, lender communications, or credit decisions without professional review.

---

## Facility Overview

| Field | Value |
|-------|-------|
| Borrower | [name] |
| Facility Type | [Subscription Line / NAV Facility / Term Loan / Revolver / Hybrid] |
| Lender(s) | [agent and syndicate] |
| Facility Size | $[amount] |
| Outstanding Balance | $[amount] (if provided) |
| Available / Undrawn | $[amount] (if calculable) |
| Maturity Date | [date] |
| Interest Rate | [base] + [spread] bps |
| Governing Law | [jurisdiction] |
| Date of Review | [date] |

---

## Compliance Dashboard

### Overall Status: [ALL COMPLIANT / WARNING / BREACH IDENTIFIED]

| # | Covenant | Type | Threshold | Current | Status | Headroom |
|---|----------|------|-----------|---------|--------|----------|
| 1 | [covenant] | Financial | [threshold] | [current] | [status] | [headroom] |
| 2 | [covenant] | Financial | [threshold] | [current] | [status] | [headroom] |
| 3 | [covenant] | Reporting | [deadline] | [last delivered] | [status] | [days] |
| 4 | [covenant] | Operational | [requirement] | [status] | [status] | N/A |

---

## Financial Covenants — Detail

### [Covenant Name]
- **Section Reference:** [X.X]
- **Description:** [plain English description]
- **Threshold:** [specific requirement]
- **Testing Frequency:** [when tested]
- **Cure Period:** [X days / None]
- **Consequence of Breach:** [specific consequence]
- **Current Status:** [Compliant/Warning/Breach/Not Tested]
- **Headroom:** [X]% ([X] absolute units from threshold)
- **Calculation:** [formula as defined in credit agreement]

[Repeat for each financial covenant]

---

## Borrowing Base Analysis (Subscription Lines)

| Component | Value | Notes |
|-----------|-------|-------|
| Total LP Commitments | $[amount] | |
| Less: Called Capital | ($[amount]) | |
| = Uncalled Capital | $[amount] | |
| Less: Ineligible Investors | ($[amount]) | [reason] |
| = Eligible Uncalled Capital | $[amount] | |
| x Advance Rate | [X]% | |
| = Borrowing Base | $[amount] | |
| Less: Outstanding Loans | ($[amount]) | |
| = Available Borrowing Capacity | $[amount] | |

### Concentration Limit Compliance

| Limit | Threshold | Current | Status |
|-------|-----------|---------|--------|
| Single Investor | Max [X]% | [X]% | [status] |
| Top [N] Investors | Max [X]% | [X]% | [status] |
| Jurisdiction | Max [X]% | [X]% | [status] |
| Investor Count | Min [X] | [X] | [status] |

---

## Reporting Covenants — Calendar

| Deliverable | Deadline | Last Delivered | Next Due | Status |
|-------------|----------|---------------|----------|--------|
| [deliverable] | [frequency/deadline] | [date] | [date] | [status] |

---

## Negative Covenants — Inventory

| # | Covenant | Restriction | Key Exceptions | Compliance Notes |
|---|----------|-------------|---------------|-----------------|
| 1 | [covenant] | [restriction] | [exceptions] | [notes] |

---

## Upcoming Test Dates & Deadlines

| Date | Covenant / Deliverable | Action Required |
|------|----------------------|-----------------|
| [date] | [item] | [action] |

---

## Risk Alerts

### HIGH RISK — Immediate Attention Required
[Covenants in breach or near the threshold (within a proximity band configured by the operator)]

### MEDIUM RISK — Monitor Closely
[Covenants near the threshold (within a proximity band configured by the operator) or with approaching deadlines]

### LOW RISK — Routine Monitoring
[Covenants with comfortable headroom]

---

## Cross-Default and Cascading Risk

[Analysis of cross-default provisions — does a breach under this facility
trigger defaults under other facilities? List any cross-default provisions
and the affected agreements]

| This Facility Breach | Cross-Default Triggered In | Consequence |
|---------------------|---------------------------|-------------|
| [breach type] | [other facility/agreement] | [consequence] |

---

## Recommended Next Steps

1. [ ] Address any HIGH RISK covenant issues immediately with financial and legal advisors
2. [ ] Prepare and deliver any overdue reporting deliverables
3. [ ] Update borrowing base certificate (if subscription line) per required frequency
4. [ ] Model covenant compliance under stress scenarios (revenue decline, valuation decline)
5. [ ] Review cure period mechanics and remediation options for any approaching breaches
6. [ ] Confirm cross-default exposure across all fund-level and portfolio-level facilities
7. [ ] Calendar all upcoming test dates and reporting deadlines
8. [ ] Engage legal counsel for any covenant amendment or waiver negotiations
```

---

## Phase 5: Present to User

After generating the report:

1. Display the **Overall Compliance Status** prominently (ALL COMPLIANT / WARNING / BREACH)
2. List **Covenant Count** by category (X financial, Y reporting, Z operational, W negative)
3. Highlight any covenants at **WARNING** or **BREACH** status
4. Show the **Next 3 Upcoming Deadlines** from the monitoring calendar
5. Show the full report
6. Ask: "Would you like me to review the fund's LPA for related provisions? Run `/fund review-lpa <file>`."
7. Mention: "Run `/fund report-pdf` to generate a professional PDF version of this covenant monitor."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No document provided | Ask user to provide a credit agreement, subscription line agreement, or loan document |
| Document is not a credit agreement | Report that the document does not appear to be a debt/credit facility document; suggest the appropriate `/fund` command |
| No financial data provided for compliance testing | Extract and catalog all covenants from the agreement, mark compliance status as "Not Tested — Provide Current Financial Data," and generate a data request template |
| Multiple facilities in one document | Analyze each facility separately within the same report; note interconnections and cross-default provisions |
| Amended agreement | Track the amendment history; analyze covenants as amended (current effective terms); note original vs. amended thresholds |
| Incomplete document (missing schedules/exhibits) | Analyze what is available; flag references to missing schedules/exhibits; note which covenants cannot be fully assessed |
