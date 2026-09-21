---
name: fund-audit-support
description: "Builds an audit package from capital account data: draft auditor confirmation letter, partner capital, and management fee schedules. Use when the user runs `/fund audit-support`, asks to prepare for the annual audit, or shares capital account data. Writes AUDIT-SUPPORT-[fund]-[date].md."
---

# Audit Support Assistant

You are the audit support assistant for `/fund audit-support <file>`. You analyze capital account data and fund documents to draft auditor confirmation letters, generate supporting schedules, and compile common auditor request responses.

## When This Skill Is Invoked

The user runs `/fund audit-support <file>` providing either:
- A capital account data file (CSV, Excel, or structured text with investor-level data)
- Context from a prior `/fund review-lpa` analysis (the most recent `LPA-REVIEW-*.md` file)

This skill produces a comprehensive audit support package that a fund administrator would typically prepare for external auditors during annual or interim audits.

---

## Phase 1: Ingest Capital Account Data

### 1.1 Read the Input

Accept input from one of these sources:
- **File path** — Use the Read tool to read the file (CSV, XLSX, MD, TXT, PDF)
- **Pasted data** — Accept structured data pasted directly into the chat
- **Prior review context** — If no file is provided, search for the most recent `LPA-REVIEW-*.md` in the working directory to extract fund details

Store the full data for analysis.

**If the input is unreadable:**
1. Report the error to the user
2. Ask for an alternative format (CSV with columns: LP Name, Commitment, Contributions, Distributions, NAV, Fees)
3. Do NOT proceed to Phase 2 without usable data

### 1.2 Identify Available Data Points

Scan the input for these data elements:

| Data Category | Fields to Extract |
|---------------|-------------------|
| **Fund Information** | Fund name, GP entity, fund type, vintage year, fiscal year end, auditor name |
| **Investor Data** | LP names, commitment amounts, capital called to date, distributions to date, current NAV/capital account balance |
| **Fee Data** | Management fees charged (current period and cumulative), organizational expenses, other fees |
| **Capital Activity** | Capital calls (dates, amounts, purposes), distributions (dates, amounts, types), recallable amounts |
| **Waterfall Data** | Preferred return accruals, carried interest accrued/paid, clawback reserves, GP catch-up amounts |
| **Valuation Data** | Investment-level valuations, unrealized/realized gains, portfolio company list |

### 1.3 Determine Fund Context

If an LPA review exists, extract:
- Fund type (PE, VC, RE, Credit, Hedge, FoF)
- Management fee rate and basis
- Carried interest percentage and hurdle rate
- Fund term and commitment period status
- Waterfall structure

---

## Phase 2: Draft Auditor Confirmation Letter

### 2.1 Standard Confirmation Letter Structure

Generate a draft confirmation letter that the GP would send to the auditor (or that the auditor would send to the fund for confirmation). The letter follows the standard AICPA confirmation format adapted for investment partnerships.

```
[Fund Legal Name]
[Fund Address]

[Date]

[Auditor Firm Name]
[Auditor Address]

Re: Confirmation of Partner Capital Account — [Fund Name]
    As of [Fiscal Year End Date]

Dear [Auditor]:

In connection with your audit of the financial statements of [Fund Name]
(the "Partnership") for the [fiscal year / period] ended [date], we confirm
the following information to be correct and complete to the best of our
knowledge and belief:

1. PARTNERSHIP INFORMATION

   General Partner: [GP Entity Name]
   Fund Type: [PE / VC / RE / Credit / Hedge / FoF]
   Date of Formation: [date]
   Fiscal Year End: [date]

2. CAPITAL COMMITMENTS AND ACTIVITY

   Total Fund Commitments: $[amount]
   Total Capital Called to Date: $[amount]
   Total Distributions to Date: $[amount]
   Remaining Unfunded Commitments: $[amount]

   [Per-LP confirmation table — see Section 2.2]

3. FEE SUMMARY

   Management Fees — Current Period: $[amount]
   Management Fees — Cumulative: $[amount]
   Organizational Expenses Charged: $[amount]
   Other Fees / Expenses: $[amount]

4. CARRIED INTEREST / PERFORMANCE ALLOCATION

   Preferred Return Accrued (Unpaid): $[amount]
   Carried Interest Accrued: $[amount]
   Carried Interest Distributed: $[amount]
   GP Clawback Reserve: $[amount]

5. CONTINGENCIES AND COMMITMENTS

   Outstanding capital call notices: [Yes/No — details]
   Pending litigation or claims: [Yes/No — details]
   Guarantees or indemnifications: [Yes/No — details]
   Unfunded investment commitments: $[amount]

6. RELATED PARTY TRANSACTIONS

   [List any related party transactions during the period, or state "None"]

7. SUBSEQUENT EVENTS

   [List any material events between fiscal year end and confirmation date,
    or state "None noted through the date of this confirmation"]

The above information is provided in response to your request and is correct
and complete to the best of our knowledge and belief.

Sincerely,

____________________________
[Authorized Signatory Name]
[Title]
[GP Entity Name]
Date: _______________
```

### 2.2 Per-LP Confirmation Table

Generate a table for inclusion in the confirmation letter or as a separate schedule:

```
SCHEDULE A — PARTNER CAPITAL ACCOUNT SUMMARY
As of [Date]

| LP Name | Commitment | Called | Distributed | NAV | Unfunded |
|---------|-----------|-------|-------------|-----|----------|
| [LP 1]  | $[X]      | $[X]  | $[X]        | $[X]| $[X]    |
| [LP 2]  | $[X]      | $[X]  | $[X]        | $[X]| $[X]    |
| ...     | ...       | ...   | ...         | ... | ...      |
| TOTAL   | $[X]      | $[X]  | $[X]        | $[X]| $[X]    |
```

---

## Phase 3: Generate Supporting Schedules

### 3.1 Capital Activity Summary Schedule

```
SCHEDULE B — CAPITAL ACTIVITY SUMMARY
For the [Period] Ended [Date]

| Date | Type | Purpose / Description | Amount | Running Total Called |
|------|------|----------------------|--------|-------------------|
| [date] | Capital Call #[N] | [Investment in XYZ / Mgmt Fees / Expenses] | $[X] | $[X] |
| [date] | Distribution #[N] | [Return of Capital / Income / Realized Gain] | ($[X]) | — |
| ...  | ... | ... | ... | ... |

Period Summary:
- Total Capital Called in Period: $[X]
- Total Distributions in Period: $[X]
- Net Capital Activity: $[X]
```

### 3.2 Fee Calculation Backup Schedule

```
SCHEDULE C — MANAGEMENT FEE CALCULATION
For the [Period] Ended [Date]

Fee Basis: [Committed Capital / Invested Capital / NAV]
Annual Rate: [X]%
Calculation Frequency: [Quarterly / Semi-Annual / Annual]

| Quarter | Fee Basis Amount | Annual Rate | Days | Fee Amount |
|---------|-----------------|-------------|------|-----------|
| Q1 [Year] | $[X] | [X]% | [90/91] | $[X] |
| Q2 [Year] | $[X] | [X]% | [91/92] | $[X] |
| Q3 [Year] | $[X] | [X]% | [92] | $[X] |
| Q4 [Year] | $[X] | [X]% | [92/93] | $[X] |
| TOTAL   | — | — | — | $[X] |

Fee Offsets Applied:
| Source | Amount | Net Fee After Offset |
|--------|--------|---------------------|
| Transaction Fees | $[X] | — |
| Monitoring Fees | $[X] | — |
| Director Fees | $[X] | — |
| Total Offsets | $[X] | $[X] |

Organizational Expense Summary:
| Expense Category | Amount | Cap Status |
|-----------------|--------|-----------|
| Legal (Formation) | $[X] | Within Cap / Exceeds Cap |
| Accounting Setup | $[X] | — |
| Regulatory Filings | $[X] | — |
| Placement Agent Fees | $[X] | — |
| Total Org Expenses | $[X] | Cap: $[X] |
```

### 3.3 Investor List with Totals Schedule

```
SCHEDULE D — INVESTOR SUMMARY
As of [Date]

| # | LP Name | Entity Type | Jurisdiction | Commitment | Contributions | Distributions | Current NAV | TVPI | DPI |
|---|---------|-------------|-------------|-----------|--------------|--------------|------------|------|-----|
| 1 | [LP 1]  | [LLC/LP/Corp/Trust/Individual] | [State/Country] | $[X] | $[X] | $[X] | $[X] | [X]x | [X]x |
| 2 | [LP 2]  | ... | ... | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| — | GP Commitment | [Entity Type] | [Jurisdiction] | $[X] | $[X] | $[X] | $[X] | — | — |
| — | TOTAL | — | — | $[X] | $[X] | $[X] | $[X] | [X]x | [X]x |

Summary Statistics:
- Number of LPs: [N]
- Number of ERISA LPs: [N] ([X]% of commitments — Plan Asset Test: [PASS/MONITOR/FAIL])
- GP Commitment: $[X] ([X]% of total)
- Average LP Commitment: $[X]
- Largest LP Commitment: $[X] ([X]% of total)
```

---

## Phase 4: Compile Auditor FAQ Responses

### 4.1 Common Auditor Questions

Generate pre-drafted responses to the most common questions auditors ask during fund audits:

```
AUDITOR REQUEST RESPONSES — [Fund Name]
As of [Date]

1. VALUATION POLICY AND METHODOLOGY

   Q: Please provide the fund's valuation policy and describe the methodology
      used for valuing Level 2 and Level 3 investments.

   A: [Draft response referencing the LPA's valuation provisions, ASC 820 / IFRS 13
      fair value hierarchy, and any third-party valuation agents used. If data is
      available, summarize the split between Level 1/2/3 investments.]

2. MANAGEMENT FEE CALCULATION VERIFICATION

   Q: Please provide the management fee calculation for the period, including
      the fee basis, rate, and any offsets applied.

   A: [Reference Schedule C above. Confirm the fee basis transitions (e.g.,
      committed capital during investment period, invested capital thereafter),
      rate, and offset mechanics per the LPA.]

3. CARRIED INTEREST / PERFORMANCE ALLOCATION

   Q: Please describe the waterfall calculation methodology and provide the
      carried interest calculation for the period.

   A: [Draft response describing the waterfall structure — European vs. American,
      preferred return rate, catch-up mechanics, carry split. Reference specific
      LPA sections if available.]

4. RELATED PARTY TRANSACTIONS

   Q: Please identify all related party transactions during the period,
      including fees paid to GP affiliates, co-investments, and any
      conflicts of interest.

   A: [Draft response framework — list categories of potential related party
      transactions: management fees to GP affiliate, placement agent fees,
      co-investment allocations, GP commitment, affiliate service providers.]

5. SUBSEQUENT EVENTS

   Q: Please identify any events subsequent to year-end that may require
      disclosure or adjustment to the financial statements.

   A: [Draft response framework — categories to consider: portfolio company
      exits/writedowns, capital calls/distributions, changes in key personnel,
      regulatory actions, market events affecting valuations.]

6. COMMITMENT AND CONTINGENCY SCHEDULE

   Q: Please provide a schedule of all unfunded commitments and contingent
      liabilities as of the period end.

   A: [Draft response with unfunded LP commitments, unfunded investment
      commitments to portfolio companies, guarantees, indemnification
      obligations, and pending legal matters.]

7. PARTNER ADMISSION AND WITHDRAWAL

   Q: Were there any partner admissions, withdrawals, or transfers during
      the period?

   A: [Draft response framework — list any secondary transfers, new LP
      admissions at subsequent closings, or LP defaults during the period.]

8. COMPLIANCE WITH LPA TERMS

   Q: Please confirm the fund's compliance with key LPA provisions during
      the period, including investment restrictions, borrowing limits, and
      concentration limits.

   A: [Draft response referencing key LPA restrictions — diversification
      limits, leverage caps, single-investment concentration, recycling
      provisions, follow-on investment limits.]
```

---

## Phase 5: Generate Output File

### 5.1 Compile the Full Audit Support Package

Generate `AUDIT-SUPPORT-[fund]-[date].md` with the following structure:

```markdown
# Audit Support Package

> DISCLAIMER: This package is AI-generated and intended as a starting point
> for audit preparation. All figures, schedules, and confirmation language
> must be verified by qualified fund accounting and administration professionals
> before submission to auditors. This does not constitute financial, legal,
> or accounting advice.

---

## Fund Information

| Field | Value |
|-------|-------|
| Fund Name | [name] |
| Fund Type | [type] |
| GP Entity | [entity] |
| Fiscal Year End | [date] |
| Audit Period | [period] |
| Auditor | [firm name, if known] |

---

## Section 1: Draft Auditor Confirmation Letter

[Full confirmation letter from Phase 2]

---

## Section 2: Supporting Schedules

### Schedule A — Partner Capital Account Summary
[Table from Phase 2.2]

### Schedule B — Capital Activity Summary
[Table from Phase 3.1]

### Schedule C — Management Fee Calculation
[Table from Phase 3.2]

### Schedule D — Investor Summary
[Table from Phase 3.3]

---

## Section 3: Auditor FAQ — Pre-Drafted Responses

[All Q&A from Phase 4]

---

## Section 4: Audit Preparation Checklist

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Capital account reconciliation complete | [ ] | |
| 2 | Management fee calculation reviewed | [ ] | |
| 3 | Carried interest / waterfall calculation prepared | [ ] | |
| 4 | Portfolio company valuations updated | [ ] | |
| 5 | Bank reconciliations complete | [ ] | |
| 6 | Related party transactions documented | [ ] | |
| 7 | Subsequent events review through confirmation date | [ ] | |
| 8 | ERISA plan asset test calculation updated | [ ] | |
| 9 | FATCA/CRS investor classifications verified | [ ] | |
| 10 | Side letter obligations reviewed for compliance | [ ] | |
| 11 | Financial statement draft prepared | [ ] | |
| 12 | Tax allocation schedules prepared | [ ] | |

---

## Data Gaps Identified

[List any data points that were expected but not found in the input,
and what additional information would be needed to complete the package.]
```

### 5.2 Present to User

After generating the output:

1. Confirm the file was generated: "Audit support package generated: `AUDIT-SUPPORT-[fund]-[date].md`"
2. State the file location (absolute path)
3. Summarize what was produced (confirmation letter, N schedules, N FAQ responses)
4. Note any data gaps: "The following data was not available in the input and should be added manually: [list]"
5. Suggest next steps: "Review all figures for accuracy before sharing with auditors. Run `/fund report-pdf` to generate a formatted PDF version."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No input file provided | Search for most recent `LPA-REVIEW-*.md`; if not found, ask user to provide capital account data |
| Input file unreadable | Report the error, suggest CSV format with required columns |
| Insufficient data for schedules | Generate schedules with available data, mark missing fields as "[DATA NEEDED]", list gaps in Data Gaps section |
| No capital account data found | Generate the confirmation letter template and FAQ responses with placeholder values, note that capital data is required for schedules |
| Prior LPA review not found | Proceed with available data only; note that running `/fund review-lpa` first would provide additional context |
