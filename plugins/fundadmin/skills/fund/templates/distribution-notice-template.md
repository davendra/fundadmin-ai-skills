# Distribution Notice

<!--
Distribution notice drafting template for qualified human review.
For use with PE, VC, RE, Credit, and other closed-end fund structures.
Populate terms from identified sources; retain [MISSING] or UNCALCULATED wherever
the governing provision, evidence or packaged-helper support is absent.
-->

> DRAFT — Not financial, legal or tax advice. Qualified human review is required.
> This template does not issue a notice, decide any partner's tax treatment or approve payment.

---

## DISTRIBUTION NOTICE NO. [NUMBER]

**[FUND LEGAL NAME]**
([Sourced entity form and jurisdiction; otherwise MISSING])

---

| Field | Value |
|-------|-------|
| **Fund Name** | [Full legal name of the fund] |
| **Distribution Number** | [Sequential number — e.g., Distribution No. 4] |
| **Date of Notice** | [YYYY-MM-DD] |
| **Record Date** | [YYYY-MM-DD — date as of which LP interests are determined] |
| **Payment Date** | [YYYY-MM-DD — date funds will be wired to LPs] |
| **Total Gross Distribution** | $[Total gross distribution amount] |
| **Total Net Distribution** | $[Total net distribution after withholding] |

---

## Distribution Type

<!-- Check all that apply and provide amounts for each category. -->

| Type | Amount | Impact on Unfunded Commitment | Description |
|------|--------|-------------------------------|-------------|
| **Return of Capital** | $[amount] | [Restores (recallable) / No effect / MISSING] | [Return of contributed capital; tax treatment as classified by the fund's tax adviser] |
| **Income** | $[amount] | [No effect / MISSING] | [Interest, dividend or other income, as classified by the fund's tax adviser] |
| **Realized Gain / (Loss)** | $[amount] | [No effect / MISSING] | [Character and holding period as classified by the fund's tax adviser] |
| **Withholding Tax** | ($[amount]) | — | [Only from evidenced withholding determinations; otherwise MISSING] |
| **Carried Interest to GP** | $[amount] | — | [Helper `waterfall` output or supplied, cited figure; otherwise UNCALCULATED] |
| **Other** | $[amount] | [MISSING] | [Description — e.g., "Fee rebate," "Insurance proceeds"] |
| **Total Gross Distribution** | **$[total]** | — | — |

<!-- These types follow ILPA's Capital Call & Distribution Template v2.0 (released 11 Sep 2025; implementation Q1 2027): an ILPA published position, not a compliance test. -->

---

## Source of Proceeds

<!-- Describe the investment event(s) generating this distribution. -->

| Source | Proceeds | Cost Basis | Gain / (Loss) | Holding Period |
|--------|----------|-----------|---------------|---------------|
| [e.g., "Sale of Portfolio Company ABC, Inc."] | $[gross proceeds] | $[cost basis] | $[gain or loss] | [X] months |
| [e.g., "Dividend from Portfolio Company XYZ Corp."] | $[amount] | N/A | $[amount] | N/A |
| [e.g., "Interest on bridge loan to Portfolio Co. DEF"] | $[amount] | N/A | $[amount] | N/A |
| **Total** | **$[total proceeds]** | **$[total basis]** | **$[total gain/loss]** | — |

**Transaction Summary:** [Brief narrative description — e.g., "On [date], the Fund completed the sale of its entire equity interest in ABC, Inc. to [Buyer] for total consideration of $[X], consisting of $[Y] in cash and $[Z] in deferred consideration. The Fund's original investment was made on [date] at a cost of $[X]."] [Gross multiple and IRR only as helper `metrics` / `dated_irr` results with workpapers or supplied, cited figures; otherwise UNCALCULATED.]

---

## Waterfall Summary

<!-- Tier order from the cited LPA provision. Only a whole-fund single-event waterfall with full or no catch-up can be computed with the packaged `waterfall` helper. Cumulative positions, preferred-return accrual, catch-up history, partial catch-up, deal-by-deal and clawback figures are UNCALCULATED unless supplied and cited from the administrator's workpaper. -->

### Cumulative Waterfall Position (As of This Distribution)

| Tier | Description | Required Amount | Distributed to Date | Remaining | Status |
|------|-------------|----------------|--------------------|-----------|---------| 
| **Tier 1** | Return of Capital | $[total capital called] | $[cumulative return of capital] | $[remaining] | [Complete / In Progress] |
| **Tier 2** | Preferred Return ([X]%) | [supplied, cited figure / UNCALCULATED] | [supplied, cited figure] | [supplied, cited figure / UNCALCULATED] | [Complete / In Progress / Not Yet Reached / UNKNOWN] |
| **Tier 3** | GP Catch-Up ([X]%) | [supplied, cited figure / UNCALCULATED] | [supplied, cited figure] | [supplied, cited figure / UNCALCULATED] | [Complete / In Progress / Not Yet Reached / UNKNOWN] |
| **Tier 4** | Carried Interest Split ([X/Y]%) | N/A | $[cumulative Tier 4 distributions] | Ongoing | [Active / Not Yet Reached] |

### This Distribution — Waterfall Allocation

| Tier | LP Share | GP Share (Carry) | Total |
|------|----------|-----------------|-------|
| Tier 1 — Return of Capital | $[amount] | $[amount] | $[amount] |
| Tier 2 — Preferred Return | $[amount] | $[amount] | $[amount] |
| Tier 3 — GP Catch-Up | $[amount] | $[amount] | $[amount] |
| Tier 4 — Carried Interest | $[amount] | $[amount] | $[amount] |
| **Total** | **$[LP total]** | **$[GP total]** | **$[grand total]** |

---

## Per-LP Distribution Schedule

| Investor ID | Total Commitment | Gross Distribution | Tax Withholding | Net Distribution |
|-------------|-----------------|-------------------|-----------------|-----------------|
| [LP-001] | $[commitment] | $[gross amount] | $[withholding] | $[net amount] |
| [LP-002] | $[commitment] | $[gross amount] | $[withholding] | $[net amount] |
| [LP-003] | $[commitment] | $[gross amount] | $[withholding] | $[net amount] |
| [LP-004] | $[commitment] | $[gross amount] | $[withholding] | $[net amount] |
| [LP-005] | $[commitment] | $[gross amount] | $[withholding] | $[net amount] |
| [GP Entity] (Carried Interest) | $[GP commitment] | $[GP share] | $[withholding] | $[net amount] |
| **TOTAL** | **$[total]** | **$[total gross]** | **$[total withholding]** | **$[total net]** |

### Tax Withholding Notes

<!-- Show withholding only from supplied, evidenced withholding determinations (author, date, basis, rate, base). Never apply a default rate or decide a partner's tax status in this template. -->

| Investor ID | Withholding Type and Basis (as determined) | Determination Source | Rate (as determined) | Base Amount | Withholding Amount |
|-------------|--------------------------------------------|----------------------|----------------------|-------------|--------------------|
| [LP-00X] | [type and legal basis stated in the determination] | [author, date, locator] | [rate] | $[amount] | $[amount] |

[If no evidenced determination was supplied: MISSING — evidenced withholding determination.]

---

## Impact on Unfunded Commitment

<!-- Recallability is expressed through each line's impact on unfunded commitment, using only the cited LPA provision. -->

- **Amount restoring unfunded commitment (recallable):** $[amount / None / MISSING]
- **Governing provision:** [Section X.X; otherwise MISSING — governing recallability terms]
- **Recall purposes, conditions and period:** [only as stated in the cited provision; otherwise MISSING]

## Clawback Reserve Notation

<!-- If carried interest is being distributed, note the clawback reserve status. -->

- **Carried Interest Distributed (This Distribution):** $[amount]
- **Cumulative Carried Interest Distributed:** $[cumulative amount]
- **Escrow Balance:** $[amount held in escrow per LPA Section [X.X]]
- **Escrow Percentage:** [X]% of carried interest held back
- **Clawback figures stated gross or net of tax:** [Gross / Net of tax at the rate stated in the LPA / MISSING]
- **Clawback Obligation Status:** [supplied, cited figure from the administrator's workpaper / UNCALCULATED — not supported by the packaged helper]

---

## Payment Method and Timeline

**Payment Method:** Wire transfer to the verified LP bank accounts held in the system of record.

**Payment Date:** [YYYY-MM-DD]

Do not send bank details by email. Any change to bank details is accepted only through [the fund's documented change process — MISSING if not supplied] and is confirmed by an outbound callback to a number already held in the system of record before payment. [Change cut-off date: sourced date / MISSING.]

**K-1 / Tax Reporting:** Tax allocations related to this distribution will be reflected in the Schedule K-1 for the tax year ending [date]. Expected K-1 delivery date: [sourced date / MISSING].

---

## General Partner Signature

On behalf of the General Partner:

**[GP Entity Legal Name]**

By: ____________________________

Name: [Authorized Signatory Name]

Title: [Title — e.g., Managing Director, Authorized Person]

Date: ____________________________

---

## Status, limitations and data handling
- Report status: [DRAFT / PARTIAL / BLOCKED / READY_FOR_REVIEW] — the same value as the evidence sidecar.
- Assumptions: [list]
- Limitations and checks not performed: [list; UNKNOWN / NOT PERFORMED items]
- Data handling: the packaged helpers ran locally and made no network calls; the AI host and its model provider processed the document content; connectors used: [none / list]. Confirm the source documents' confidentiality terms permit this processing.

Not financial, legal or tax advice. Qualified human review is required.

---

<!--
TEMPLATE USAGE NOTES:

1. Replace [bracketed placeholders] only with sourced values; keep MISSING / UNCALCULATED visible. Dollar placeholders are illustrative: use the actual single currency throughout.
2. The Per-LP distribution schedule should include ALL partners, including GP carry, using pseudonymous investor IDs; legal names are merged from the protected register at issue.
3. Use fund_calculations.py allocate for LP amounts with source-supported weights, and reconcile the sum to the Total Distribution.
4. Waterfall figures come from the packaged `waterfall` helper where the model is supported, otherwise from the administrator's cited workpaper, otherwise UNCALCULATED.
5. Withholding comes only from evidenced withholding determinations; this template never decides a partner's tax status or applies a default rate.
6. Impact on unfunded commitment (recallability) should match the specific LPA provisions.
7. Clawback reserve notation is required whenever carried interest is distributed.
8. Distribution types (return of capital, income, gain) have different tax treatments —
   ensure proper categorization in consultation with the fund's tax advisor.
9. For interim distributions during the investment period, note the impact on
   unfunded commitments (if recallable) or the waterfall position.
10. This template should be reviewed by fund counsel and tax advisors before first use.
11. Obtain the DISTRIBUTION-NOTICE basename from fund_report.py filename and save using the shared report contract's isolated run and write-report helper (drafts subfolder).
-->
