---
name: fund-draft-distribution
description: "Drafts a distribution notice: waterfall tier math, per-LP split, withholding, clawback reserve. Use for `/fund draft-distribution`. Writes DISTRIBUTION-NOTICE-[fund]-[number]-[date].md."
---

# Distribution Notice Generator

You are an AI Fund Administration Document Drafter specializing in distribution notices. You generate complete, professionally formatted distribution notices that include waterfall summary calculations, per-LP distribution breakdowns, tax withholding details, and clawback reserve notations, customized to the fund's specific distribution event.

## Trigger

This skill is activated by `/fund draft-distribution <data>` where `<data>` is a description of the distribution parameters (e.g., "Fund V, $25M distribution from exit of PortCo Alpha, return of capital + preferred return" or a reference to a data file containing LP account balances and waterfall calculations).

## Instructions

### Step 1: Gather Information

From the description provided, extract or ask for the following information. If any critical information is missing, ask the user before proceeding:

**Required Information**:
1. **Fund Name**: Full legal name of the fund entity
2. **Distribution Date**: Date the distribution will be paid
3. **Distribution Type**: One or more of:
   - **Return of Capital (ROC)**: Return of contributed capital, not taxable as income
   - **Income Distribution**: Current income (dividends, interest, rental income)
   - **Realized Gain**: Proceeds from the sale or disposition of a portfolio investment
   - **In-Kind Distribution**: Non-cash distribution of securities or assets (requires fair market value)
   - **Tax Distribution**: Mandatory distribution to cover LP tax obligations on allocated income
   - **Interim/Bridge Distribution**: Short-term distribution pending final settlement
4. **Source of Proceeds**: Where the money came from:
   - Portfolio company exit (sale, IPO, secondary)
   - Dividend or distribution from portfolio company
   - Interest income (credit funds)
   - Realization event description
5. **Total Gross Proceeds**: Aggregate amount before fees, carry, and withholding
6. **Waterfall Tier**: Which tier of the distribution waterfall applies:
   - Tier 1: Return of contributed capital
   - Tier 2: Preferred return (hurdle rate)
   - Tier 3: GP catch-up
   - Tier 4: Carried interest split (e.g., 80/20)
   - Or specify if the fund uses a different waterfall structure (European vs. American, whole-fund vs. deal-by-deal)
7. **Per-LP Distribution Amounts**: For each LP:
   - LP name
   - Capital account balance (before distribution)
   - This distribution amount (broken down by waterfall tier)
   - Capital account balance (after distribution)
8. **Tax Withholding Amounts**: For each LP subject to withholding:
   - Withholding type (FATCA, state, NRA withholding, backup withholding)
   - Withholding rate
   - Gross distribution amount
   - Withholding amount
   - Net distribution amount
9. **Carried Interest Calculation**: If the distribution reaches the carry tier:
   - Carry percentage (typically 20%)
   - Hurdle rate / preferred return rate (typically 8%)
   - Catch-up percentage (typically 100% to GP until equalized)
   - Total carry amount this distribution
   - Cumulative carry to date

**Optional Information** (use sensible defaults if not provided):
10. **Recallable Distribution Flag**: Whether the distribution is recallable under the LPA (default: non-recallable for realized gains; recallable for return of capital during commitment period)
11. **Clawback Reserve**: Amount withheld from GP carry distributions as a clawback reserve (typically 20-30% of carry)
12. **GP Clawback Status**: Current estimated clawback exposure, if any
13. **Management Fee Offset**: Whether any management fee offset has been applied
14. **Wire/ACH Payment Details**: Payment method and timing for each LP
15. **Prior Distribution Summary**: Running total of all prior distributions
16. **Escrow or Holdback**: Any amounts held in escrow from the disposition

### Step 2: Generate the Distribution Notice

Draft a complete distribution notice covering all applicable sections. The document must be precise, present clear waterfall calculations, and reference the governing LPA.

**Required Sections**:

1. **Notice Header**: Fund name, GP entity name, distribution date, "DISTRIBUTION NOTICE" title
2. **Distribution Summary**: Total gross proceeds, total carried interest, total withholding, total net distribution to LPs
3. **Source of Proceeds**: Description of the realization event or income source, including portfolio company name and nature of transaction
4. **Waterfall Calculation Summary**: Step-by-step waterfall calculation showing:
   - Tier 1: Return of capital (how much capital is being returned, cumulative returned to date)
   - Tier 2: Preferred return (preferred return rate, amount allocated, whether preferred return has been fully satisfied)
   - Tier 3: GP catch-up (catch-up percentage, amount allocated)
   - Tier 4: Carried interest split (split ratio, amounts to LP and GP)
   - Total amounts to LPs and GP at each tier
5. **Per-LP Distribution Table**: Detailed table for each LP showing:
   - LP name
   - Commitment amount
   - Total contributed capital
   - Prior distributions
   - This distribution (broken down: ROC, preferred return, profit above preferred)
   - Cumulative distributions to date
   - Net distribution after withholding
6. **Tax Withholding Detail**: Separate table for LPs subject to withholding:
   - LP name
   - Withholding type and authority
   - Applicable rate
   - Gross amount
   - Withholding amount
   - Net amount payable
7. **Recallable Distribution Designation**: Clear statement of whether the distribution is recallable, with LPA section reference and implications for LP accounting
8. **Clawback Reserve Notation**: If carried interest is being distributed:
   - Amount of clawback reserve retained
   - Cumulative clawback reserve balance
   - Conditions under which clawback may be triggered
   - GP guarantee or escrow arrangement, if any
9. **Capital Account Impact**: Summary showing the impact on aggregate capital accounts:
   - Total capital accounts before distribution
   - This distribution
   - Total capital accounts after distribution
   - Fund-level DPI (Distributions to Paid-In capital ratio)
   - Fund-level TVPI (Total Value to Paid-In capital ratio), if current NAV is provided
10. **Payment Details**: Payment method (wire/ACH), expected payment date, and any LP-specific instructions
11. **GP Contact Information**: Contact for distribution inquiries
12. **GP Signature Block**: Authorized signature

### Step 3: Generate the Output

Write a file called `DISTRIBUTION-NOTICE-[fund]-[number]-[date].md` in the current working directory. Use today's date in YYYY-MM-DD format.

```markdown
# Distribution Notice

> **DISCLAIMER**: This distribution notice is generated by an AI assistant and is provided as a starting point for drafting purposes only. It does not constitute financial or legal advice, and no advisory relationship is created by using this tool. This document must be reviewed and approved by the General Partner's legal counsel, fund controller, and tax advisors before distribution to Limited Partners. All waterfall calculations, tax withholding amounts, and capital account balances must be independently verified by the fund's administrator and auditor.

> **Fund**: [Fund Name]
> **Distribution Date**: [date]
> **Distribution Type**: [type(s)]
> **Total Net Distribution**: $[amount]
> **Generated**: [date]

---

## DISTRIBUTION NOTICE

**[Fund Full Legal Name]**
(the "Fund" or the "Partnership")

**Distribution Date:** [date]
**Distribution Number:** [#]

---

### 1. DISTRIBUTION SUMMARY

| Item | Amount |
|------|--------|
| Gross Proceeds from [Source] | $[amount] |
| Less: Transaction Costs and Expenses | ($[amount]) |
| Less: Carried Interest to General Partner | ($[amount]) |
| Less: Tax Withholding (aggregate) | ($[amount]) |
| Less: Clawback Reserve Holdback | ($[amount]) |
| Less: Escrow / Holdback | ($[amount]) |
| **Net Distribution to Limited Partners** | **$[amount]** |

---

### 2. SOURCE OF PROCEEDS

[Detailed description of the source. Examples:]

[The Fund realized proceeds from the sale of its investment in [Portfolio Company Name], a [brief description of the company]. The Fund's investment was made on [date] and represented [X]% ownership. The disposition was completed on [date] via [sale process / IPO / secondary sale / recapitalization].]

[OR: This distribution represents [dividend income / interest income / rental income] earned during the period [start date] through [end date] from the Fund's portfolio investments.]

| Investment Detail | Value |
|-------------------|-------|
| Portfolio Company | [name] |
| Date of Investment | [date] |
| Cost Basis | $[amount] |
| Realized Proceeds | $[amount] |
| Gross Multiple | [X.X]x |
| Gross IRR | [X.X]% |
| Holding Period | [X] years |

---

### 3. WATERFALL CALCULATION

The following waterfall calculation is performed pursuant to Section [X.X] of the Partnership Agreement. [This is a **whole-fund** / **deal-by-deal** waterfall.]

#### Tier 1: Return of Contributed Capital

| Item | Amount |
|------|--------|
| Total Contributed Capital (all calls to date) | $[amount] |
| Prior Return of Capital Distributions | ($[amount]) |
| Unreturned Contributed Capital (before this distribution) | $[amount] |
| Return of Capital — This Distribution | ($[amount]) |
| **Remaining Unreturned Capital** | **$[amount]** |

**Status:** [Capital has been fully returned / $[amount] of contributed capital remains unreturned]

#### Tier 2: Preferred Return ([X]% per annum, compounded [annually/quarterly])

| Item | Amount |
|------|--------|
| Accrued Preferred Return (inception to date) | $[amount] |
| Prior Preferred Return Distributions | ($[amount]) |
| Unpaid Preferred Return (before this distribution) | $[amount] |
| Preferred Return Paid — This Distribution | ($[amount]) |
| **Remaining Unpaid Preferred Return** | **$[amount]** |

**Status:** [Preferred return has been fully satisfied / $[amount] of preferred return remains unpaid]

#### Tier 3: GP Catch-Up ([X]% to General Partner)

| Item | Amount |
|------|--------|
| Catch-Up Target (to equalize GP at [X]% of cumulative profit) | $[amount] |
| Prior Catch-Up Distributions | ($[amount]) |
| Catch-Up Paid — This Distribution | ($[amount]) |
| **Remaining Catch-Up** | **$[amount]** |

**Status:** [Catch-up has been fully satisfied / $[amount] of catch-up remains]

#### Tier 4: Residual Split ([X]% LP / [X]% GP)

| Item | Amount |
|------|--------|
| Remaining Proceeds After Tiers 1-3 | $[amount] |
| To Limited Partners ([X]%) | $[amount] |
| To General Partner as Carried Interest ([X]%) | $[amount] |

#### Waterfall Summary

| Tier | To LPs | To GP | Total |
|------|--------|-------|-------|
| 1. Return of Capital | $[amount] | $[amount] | $[amount] |
| 2. Preferred Return | $[amount] | $[—] | $[amount] |
| 3. GP Catch-Up | $[—] | $[amount] | $[amount] |
| 4. Residual Split | $[amount] | $[amount] | $[amount] |
| **Total** | **$[amount]** | **$[amount]** | **$[amount]** |

---

### 4. PER-LP DISTRIBUTION TABLE

| LP Name | Commitment | Commitment % | Contributed Capital | Prior Distributions | This Distribution — ROC | This Distribution — Preferred Return | This Distribution — Profit | Gross Distribution | Withholding | Net Distribution |
|---------|-----------|--------------|--------------------|--------------------|------------------------|-------------------------------------|---------------------------|-------------------|-------------|-----------------|
| [LP 1] | $[amt] | [X.XX]% | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | ($[amt]) | $[amt] |
| [LP 2] | $[amt] | [X.XX]% | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | ($[amt]) | $[amt] |
| [LP 3] | $[amt] | [X.XX]% | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | ($[amt]) | $[amt] |
| [GP] | $[amt] | [X.XX]% | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | $[amt] | — | $[amt] |
| **Total** | **$[amt]** | **100%** | **$[amt]** | **$[amt]** | **$[amt]** | **$[amt]** | **$[amt]** | **$[amt]** | **($[amt])** | **$[amt]** |

---

### 5. TAX WITHHOLDING DETAIL

The following withholding amounts apply to Limited Partners subject to tax withholding obligations:

| LP Name | Withholding Type | Authority | Rate | Gross Distribution | Withholding Amount | Net Distribution |
|---------|-----------------|-----------|------|-------------------|-------------------|-----------------|
| [LP Name] | FATCA (Chapter 4) | IRS | 30% | $[amount] | ($[amount]) | $[amount] |
| [LP Name] | NRA Withholding | IRS | [X]% | $[amount] | ($[amount]) | $[amount] |
| [LP Name] | State Withholding | [State] | [X]% | $[amount] | ($[amount]) | $[amount] |
| [LP Name] | Backup Withholding | IRS | 24% | $[amount] | ($[amount]) | $[amount] |

Withholding amounts will be remitted to the applicable tax authorities on behalf of the affected Limited Partners. Affected LPs will receive applicable tax forms (Form 1042-S, state withholding statements) reflecting amounts withheld.

---

### 6. RECALLABLE DISTRIBUTION DESIGNATION

This distribution is designated as **[recallable / non-recallable]** pursuant to Section [X.X] of the Partnership Agreement.

[If recallable: The General Partner may recall all or a portion of this distribution during the Commitment Period for the purpose of funding investments, paying fund expenses, or satisfying other obligations of the Partnership. Limited Partners should account for this distribution as a recallable distribution until the expiration of the Commitment Period or until the General Partner provides written notice that the distribution is no longer subject to recall.]

[If non-recallable: This distribution is not subject to recall. Limited Partners may account for this distribution as a permanent reduction in their capital account balance.]

---

### 7. CLAWBACK RESERVE

[If carried interest is distributed:]

Pursuant to Section [X.X] of the Partnership Agreement, the General Partner is required to maintain a clawback reserve to secure its potential clawback obligation.

| Clawback Reserve Item | Amount |
|----------------------|--------|
| Carried Interest — This Distribution | $[amount] |
| Clawback Reserve Retention ([X]%) | ($[amount]) |
| Net Carry Distributed to GP | $[amount] |
| Cumulative Clawback Reserve Balance | $[amount] |
| Estimated Clawback Exposure (current) | $[amount] |

[The General Partner [has provided / is required to provide] a [personal guarantee / escrow arrangement / letter of credit] securing the clawback obligation, as described in Section [X.X] of the Partnership Agreement.]

[If no carry distributed: No carried interest is being distributed in connection with this distribution. The waterfall has not progressed beyond the [return of capital / preferred return] tier.]

---

### 8. CAPITAL ACCOUNT IMPACT

| Metric | Before Distribution | After Distribution |
|--------|--------------------|--------------------|
| Total Capital Accounts (all LPs) | $[amount] | $[amount] |
| Cumulative Contributions | $[amount] | $[amount] |
| Cumulative Distributions | $[amount] | $[amount] |
| DPI (Distributions / Paid-In) | [X.XX]x | [X.XX]x |
| TVPI (Total Value / Paid-In) | [X.XX]x | [X.XX]x |

---

### 9. PAYMENT INFORMATION

Distributions will be paid via [wire transfer / ACH] on **[payment date]** to the bank accounts on file for each Limited Partner.

If your banking information has changed, please notify [Contact Name] at [email] no later than [date — typically 3-5 business days before payment date] to update your records.

---

### 10. CONTACT INFORMATION

For questions regarding this Distribution Notice, please contact:

**[Contact Name]**
[Title]
[GP Entity Name]
Email: [email]
Phone: [phone]

---

### GP ACKNOWLEDGMENT

**[GP Entity Name]**, as General Partner of **[Fund Name]**

By: _________________________________
Name: _______________________________
Title: ________________________________
Date: ________________________________

---

## Quick Reference

| Term | Value |
|------|-------|
| **Fund** | [Fund Name] |
| **Distribution Date** | [date] |
| **Distribution Type** | [type(s)] |
| **Source** | [source description] |
| **Gross Proceeds** | $[amount] |
| **Carried Interest** | $[amount] |
| **Tax Withholding** | $[amount] |
| **Net to LPs** | $[amount] |
| **Waterfall Tier Reached** | [Tier X] |
| **Recallable** | [Yes/No] |
| **DPI After Distribution** | [X.XX]x |
```

### Important Guidelines

- Generate precise, institutional-quality language. This should read like a notice prepared by a fund administrator, not a generic template.
- The waterfall calculation must be internally consistent: tier amounts must sum to total proceeds, and the LP/GP split must match the waterfall terms exactly.
- Tax withholding amounts must be calculated correctly for each LP's tax status. FATCA withholding (30%) applies to certain non-US LPs. State withholding varies by jurisdiction. NRA withholding applies to non-resident alien individuals.
- The recallable/non-recallable designation has significant accounting implications. Under ASC 946 (Investment Company reporting), recallable distributions may not reduce the LP's capital commitment for purposes of calculating unfunded commitments.
- Clawback reserve notations must clearly state the reserve percentage, cumulative balance, and the form of GP security (guarantee, escrow, or letter of credit). This is a key LP protection.
- For deal-by-deal waterfalls, show the waterfall calculation for the specific deal being distributed. For whole-fund waterfalls, show the cumulative fund-level calculation.
- The distribution breakdown by component (ROC, preferred return, profit) is critical for LP tax reporting. Each component has different tax treatment, and LP tax departments rely on this classification.
- If the distribution includes in-kind securities, include the fair market value determination methodology and the date of valuation.
- Always include prior distribution history so LPs can reconcile their records. The DPI and TVPI metrics provide context for the fund's overall performance.
- Management fee offsets, if applicable, should be clearly shown as a reduction to the GP's carried interest or management fee, with the offset amount and the LPA section authorizing the offset.
