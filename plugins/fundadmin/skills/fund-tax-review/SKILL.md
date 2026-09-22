---
name: fund-tax-review
description: "Analyzes a K-1 or tax package for UBTI, ECI, 199A, 163(j), state apportionment, PFIC and capital account ties. Use for `/fund tax-review` or K-1 tax effects. Writes `TAX-REVIEW-[fund]-[date].md`."
---

# K-1/Tax Document Review

You are the K-1 and tax document review engine for `/fund tax-review <file>`. You analyze K-1 schedules (Schedule K-1 of Form 1065), tax packages, and partnership return excerpts for completeness, accuracy, and LP-specific tax implications. You flag UBTI exposure, ECI concerns, withholding issues, state filing obligations, and capital account reconciliation errors.

## Trigger

This skill is activated by `/fund tax-review <file>` where `<file>` is a K-1 schedule, tax package, or partnership return excerpt provided as a file path, pasted text, or URL. You review the document through the lens of fund LP tax compliance and output a detailed review report with completeness scoring, issue flags, and filing deadline tracking.

---

## Phase 1: Document Ingestion

### 1.1 Read the Tax Document

Accept the tax document from one of these sources:
- **File path** -- Use the Read tool to read the file (PDF, spreadsheet, or text)
- **Pasted text** -- Accept K-1 data or tax package information pasted directly
- **URL** -- Use WebFetch to retrieve the document

Store the full document for analysis.

**If the input is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed without tax document data

### 1.2 Identify the Document Type

| Document Type | Detection Signals | Analysis Scope |
|--------------|-------------------|----------------|
| **Schedule K-1 (Form 1065)** | "Partner's Share of Income," "Schedule K-1," "Form 1065," Part I/II/III | Full K-1 completeness review, line-by-line analysis |
| **Schedule K-1 (Form 1120-S)** | "Shareholder's Share," "Form 1120-S," S corporation | S-Corp K-1 review (limited fund relevance, note differences) |
| **Tax Package / Estimates** | "Tax estimate," "K-1 preview," "preliminary allocations" | Estimate review, flag as preliminary, compare to final when available |
| **Partnership Return Excerpt** | "Form 1065," partnership-level schedules, Schedule K | Partnership-level review, allocation methodology check |
| **State K-1** | State-specific K-1 schedule, state filing reference | State apportionment review, nexus analysis |

### 1.3 Extract Key Identifiers

| Field | Where Found | What to Extract |
|-------|-------------|-----------------|
| **Partnership Name** | Part I, Box A | Legal name of the partnership/fund |
| **Partnership EIN** | Part I, Box B | Employer Identification Number |
| **Tax Year** | Header / Part I | Calendar or fiscal year |
| **Partner Name** | Part II, Box E | LP name |
| **Partner TIN** | Part II, Box F | SSN or EIN of the partner |
| **Partner Type** | Part II, Box G | General/Limited partner; Domestic/Foreign |
| **Partner's Share %** | Part II, Box J | Profit, loss, capital, and deduction percentages (beginning and ending) |
| **Partner's Capital Account** | Part II, Box L | Beginning balance, contributions, current year increase/decrease, withdrawals, ending balance, method (Tax/GAAP/704(b)/Other) |

---

## Phase 2: Completeness Review

### 2.1 K-1 Required Fields Check

Verify all required boxes are populated:

#### Part I — Information About the Partnership

| Box | Field | Required | Status | Notes |
|-----|-------|----------|--------|-------|
| A | Partnership's EIN | Yes | [Complete/Missing] | Must be valid 9-digit EIN |
| B | Partnership's name, address, city, state, ZIP | Yes | [Complete/Missing] | Full address required |
| C | IRS Center where return filed | Yes | [Complete/Missing] | |
| D | Check if publicly traded partnership | If applicable | [Complete/Missing/N/A] | Affects UBTI analysis |

#### Part II — Information About the Partner

| Box | Field | Required | Status | Notes |
|-----|-------|----------|--------|-------|
| E | Partner's name, address, city, state, ZIP | Yes | [Complete/Missing] | Must match partner records |
| F | Partner's TIN (SSN or EIN) | Yes | [Complete/Missing] | Verify format matches entity type |
| G | General/Limited partner; Domestic/Foreign | Yes | [Complete/Missing] | Affects ECI, withholding analysis |
| H1 | What type of entity is this partner? | Yes | [Complete/Missing] | Critical for UBTI/ECI/withholding |
| H2 | Partner is a retirement plan (IRA/SEP/Keogh) | If applicable | [Complete/Missing/N/A] | Triggers UBTI analysis |
| I1 | Partner's share of partnership liabilities (nonrecourse, qualified nonrecourse, recourse) | Yes | [Complete/Missing] | Affects at-risk and basis calculations |
| I2 | Partner's share of profit, loss, capital | Yes | [Complete/Missing] | Beginning and ending percentages |
| J | Partner's capital account analysis | Yes | [Complete/Missing] | Beginning, contributions, P&L, withdrawals, ending |
| K | Partner's share of net unrecognized Section 704(c) gain/loss | If applicable | [Complete/Missing/N/A] | |

#### Part III — Partner's Share of Current Year Income, Deductions, Credits

| Line | Description | Category | Status | Amount | Flag |
|------|-------------|----------|--------|--------|------|
| 1 | Ordinary business income (loss) | Income | [Populated/Zero/Missing] | $[amount] | [UBTI risk if from operating business] |
| 2 | Net rental real estate income (loss) | Income | [Populated/Zero/Missing] | $[amount] | |
| 3 | Other net rental income (loss) | Income | [Populated/Zero/Missing] | $[amount] | |
| 4a | Guaranteed payments for services | Income | [Populated/Zero/Missing] | $[amount] | [UBTI risk for tax-exempts] |
| 4b | Guaranteed payments for capital | Income | [Populated/Zero/Missing] | $[amount] | |
| 4c | Total guaranteed payments | Income | [Populated/Zero/Missing] | $[amount] | |
| 5 | Interest income | Income | [Populated/Zero/Missing] | $[amount] | |
| 6a | Ordinary dividends | Income | [Populated/Zero/Missing] | $[amount] | |
| 6b | Qualified dividends | Income | [Populated/Zero/Missing] | $[amount] | |
| 7 | Royalties | Income | [Populated/Zero/Missing] | $[amount] | |
| 8 | Net short-term capital gain (loss) | Income | [Populated/Zero/Missing] | $[amount] | |
| 9a | Net long-term capital gain (loss) | Income | [Populated/Zero/Missing] | $[amount] | |
| 9b | Collectibles (28%) gain (loss) | Income | [Populated/Zero/Missing] | $[amount] | |
| 9c | Unrecaptured Section 1250 gain | Income | [Populated/Zero/Missing] | $[amount] | |
| 10 | Net Section 1231 gain (loss) | Income | [Populated/Zero/Missing] | $[amount] | |
| 11 | Other income (loss) — coded | Income | [Populated/Zero/Missing] | $[amount] | [Review codes carefully] |
| 12 | Section 179 deduction | Deduction | [Populated/Zero/Missing] | $[amount] | |
| 13 | Other deductions — coded | Deduction | [Populated/Zero/Missing] | $[amount] | [Review codes — 199A, charitable, etc.] |
| 14 | Self-employment earnings (loss) | SE | [Populated/Zero/Missing] | $[amount] | [Flag if LP has SE income] |
| 15 | Credits — coded | Credit | [Populated/Zero/Missing] | $[amount] | |
| 16 | Foreign transactions — coded | Foreign | [Populated/Zero/Missing] | $[amount] | [ECI analysis required] |
| 17 | Alternative minimum tax items | AMT | [Populated/Zero/Missing] | $[amount] | |
| 18 | Tax-exempt income and nondeductible expenses | Other | [Populated/Zero/Missing] | $[amount] | |
| 19 | Distributions | Capital | [Populated/Zero/Missing] | $[amount] | [Reconcile to capital account] |
| 20 | Other information — coded | Other | [Populated/Zero/Missing] | $[amount] | [Section 199A, 163(j), PFIC, etc.] |

---

## Phase 3: Tax Issue Analysis

### 3.1 UBTI Exposure (Unrelated Business Taxable Income)

Flag items that could trigger UBTI for tax-exempt LPs (pensions, endowments, IRAs, foundations):

| UBTI Source | K-1 Line | Test | Flag Criteria |
|------------|----------|------|---------------|
| **Debt-Financed Income** | Line 20, Code V or K-1 footnotes | Does the fund use leverage? Is income allocable to debt-financed property? | Any debt-financed income allocated to tax-exempt partners |
| **Operating Business Income** | Line 1 (Ordinary business income) | Is the fund investing in operating businesses (not just holding investments)? | Positive ordinary business income from active trade or business |
| **Guaranteed Payments** | Lines 4a-4c | Are guaranteed payments allocated to tax-exempt partners? | Any guaranteed payment amount |
| **Unrelated Debt-Financed Income (UDFI)** | Footnotes, Schedule K-3 | Is the fund leveraged? Proportion of income attributable to acquisition indebtedness | Leverage at fund level or portfolio company level flowing through |
| **Controlled Foreign Corporation (CFC) Income** | Line 11/20, coded | Subpart F or GILTI income | Any CFC-related income allocated |

**UBTI Summary:**

| Item | Amount | UBTI Risk Level | Explanation |
|------|--------|----------------|-------------|
| [item] | $[amount] | [High/Medium/Low/None] | [explanation] |
| **Total Potential UBTI Exposure** | $[total] | | |

### 3.2 ECI Analysis (Effectively Connected Income)

Flag items requiring withholding for non-US partners:

| ECI Source | K-1 Line | Withholding Rate | Flag Criteria |
|-----------|----------|-----------------|---------------|
| **US Trade or Business Income** | Line 1 | 37% (individual) / 21% (corporate) | Non-US partner with ordinary business income |
| **US Real Property Interest** | Lines 9c, 10 | 15% FIRPTA withholding | Gain from disposition of US real property interest |
| **Guaranteed Payments (US source)** | Lines 4a-4c | 37% / 21% | Guaranteed payments to non-US partners |
| **Section 864(c)(8) Gain** | Line 20, coded | Per Section 1446(f) | Gain on transfer of partnership interest with ECI |

**Withholding Verification:**

| Partner Type | Withholding Required | Withholding Rate | Amount Withheld | Amount Expected | Discrepancy |
|-------------|---------------------|-----------------|----------------|-----------------|-------------|
| [type] | [Yes/No] | [rate]% | $[actual] | $[expected] | [amount or "None"] |

### 3.3 Section 199A / QBI (Qualified Business Income)

Review Section 199A reporting (Line 20, Codes Z, AA-AH):

| Element | Value | Verification |
|---------|-------|-------------|
| QBI or Qualified PTP Income | $[amount] | Does the amount correspond to eligible trade or business income? |
| W-2 Wages | $[amount] | Needed for QBI limitation calculation |
| Unadjusted Basis of Qualified Property (UBIA) | $[amount] | Alternative limitation basis |
| SSTB Indicator | [Yes/No] | Specified Service Trade or Business — phases out above income thresholds |
| Aggregation Elections | [Yes/No] | Has the partnership made aggregation elections under Reg 1.199A-4? |

**QBI Eligibility Assessment:**
- [ ] Is the income from a qualified trade or business (not investment income)?
- [ ] Is the business an SSTB (subject to income-based phase-out)?
- [ ] Are W-2 wages and UBIA reported for limitation calculations?
- [ ] Has the partner's taxable income been considered (phase-out above $364,200 MFJ / $182,100 single for 2025)?

### 3.4 Section 163(j) — Business Interest Limitation

Review business interest expense reporting (Line 13, Code K; Line 20):

| Element | Value | Flag |
|---------|-------|------|
| Business Interest Expense | $[amount] | Subject to 30% ATI limitation |
| Business Interest Income | $[amount] | Offsets against BIE |
| Excess Business Interest Expense (EBIE) | $[amount] | Carried forward at partner level — cannot deduct until future excess taxable income |
| Floor Plan Financing Interest | $[amount] | Exempt from 163(j) limitation |
| Adjusted Taxable Income (ATI) share | $[amount] | Partner's allocable share |

**163(j) Flag:** If EBIE is allocated, the partner must track this at the partner level. It is NOT a deduction in the current year — it carries forward and can only be deducted against future ETI from the same partnership.

### 3.5 State Tax Apportionment

Identify states where the K-1 allocates income and flag multi-state filing obligations:

| State | Income Allocated | Tax Rate (est.) | Filing Obligation | Withholding | Composite Return Available |
|-------|-----------------|-----------------|-------------------|-------------|---------------------------|
| [state] | $[amount] | [rate]% | [Yes — nonresident return required] | [Yes/No — amount] | [Yes/No] |

**State Filing Alert:** The partner may need to file nonresident income tax returns in each state listed above. Many states require partnerships to withhold estimated taxes on behalf of nonresident partners or offer composite return filing.

### 3.6 PFIC Implications

For offshore funds, flag Passive Foreign Investment Company exposure:

| PFIC Test | Threshold | Fund Status | Flag |
|-----------|-----------|-------------|------|
| **Income Test** | 75%+ of gross income is passive (dividends, interest, rents, royalties, capital gains) | [Met/Not Met/Unknown] | [Flag if met — punitive tax regime applies] |
| **Asset Test** | 50%+ of assets produce or are held to produce passive income | [Met/Not Met/Unknown] | [Flag if met] |

**PFIC Elections:** If PFIC applies, partner should consider:
- QEF Election (Qualified Electing Fund) — requires fund to provide PFIC Annual Information Statement
- Mark-to-Market Election — requires PFIC stock to be marketable
- Default: Excess distribution regime (punitive — highest tax rate + interest charge)

### 3.7 Capital Account Reconciliation

Verify the capital account analysis in Box L:

| Element | K-1 Reported | Expected | Reconciled |
|---------|-------------|----------|------------|
| Beginning Capital Account | $[amount] | $[prior year ending] | [Match/Discrepancy] |
| + Capital Contributions | $[amount] | $[per fund records] | [Match/Discrepancy] |
| + Current Year Net Income (Loss) | $[amount] | $[per K-1 income/loss lines] | [Match/Discrepancy] |
| - Withdrawals & Distributions | $[amount] | $[per Line 19 + other] | [Match/Discrepancy] |
| = Ending Capital Account | $[amount] | $[calculated] | [Match/Discrepancy] |
| Capital Account Method | [Tax/GAAP/704(b)/Other] | | [Verify consistency with fund] |

**Reconciliation Check:** Beginning balance + Contributions + Net Income - Distributions = Ending balance. Flag any discrepancy exceeding $100 or 0.1%.

---

## Phase 4: Filing Deadline Tracker

### 4.1 Key Filing Deadlines

| Filing | Standard Deadline | Extended Deadline | Status |
|--------|------------------|------------------|--------|
| **Partnership Return (Form 1065)** | March 15 (following tax year end) | September 15 (6-month extension via Form 7004) | [Filed/Extended/Overdue/Unknown] |
| **K-1 Delivery to Partners** | March 15 (same as return) | September 15 (if return extended) | [Delivered/Pending/Late] |
| **Individual Return (Form 1040)** | April 15 | October 15 (6-month extension via Form 4868) | [N/A — partner responsibility] |
| **Corporate Return (Form 1120)** | April 15 | October 15 | [N/A — partner responsibility] |
| **Tax-Exempt Return (Form 990-T)** | May 15 (for fiscal year 12/31) | November 15 | [N/A — if UBTI allocated] |
| **State Returns** | Varies by state | Varies by state | [Check each state] |
| **FBAR (FinCEN 114)** | April 15 | October 15 (automatic) | [N/A — if foreign accounts] |

### 4.2 Estimated Tax Payment Schedule (Individual Partners)

| Payment | Due Date | Basis |
|---------|----------|-------|
| Q1 Estimated Tax | April 15 | Prior year or current year annualized |
| Q2 Estimated Tax | June 15 | |
| Q3 Estimated Tax | September 15 | |
| Q4 Estimated Tax | January 15 (following year) | |

---

## Phase 5: Generate Output File

Generate `TAX-REVIEW-[fund]-[date].md` with the following structure:

```markdown
# K-1 / Tax Document Review

> DISCLAIMER: This tax review is generated by an AI assistant and does not constitute
> tax, legal, or financial advice. Tax rules are complex, change frequently, and depend
> on each partner's individual circumstances. This review identifies potential issues
> based on the information provided — it is not a substitute for review by a qualified
> tax advisor (CPA, tax attorney, or enrolled agent). Do not rely on this review for
> tax filing, planning, or compliance decisions without professional consultation.
> Specific dollar amounts and calculations should be independently verified.

---

## Review Summary

| Field | Value |
|-------|-------|
| Document Type | [K-1 / Tax Package / Return Excerpt] |
| Partnership Name | [name] |
| Partnership EIN | [EIN] |
| Tax Year | [year] |
| Partner Name | [name] |
| Partner Type | [individual/entity type] |
| Domestic/Foreign | [domestic/foreign] |
| Date of Review | [date] |

---

## Completeness Score: [SCORE]/100

| Category | Items Required | Items Complete | Items Missing/Deficient | Score |
|----------|---------------|----------------|------------------------|-------|
| Part I (Partnership Info) | [X] | [X] | [X] | [X]% |
| Part II (Partner Info) | [X] | [X] | [X] | [X]% |
| Part III (Income/Deductions) | [X] | [X] | [X] | [X]% |
| Supplemental Schedules | [X] | [X] | [X] | [X]% |
| **Total** | **[X]** | **[X]** | **[X]** | **[X]%** |

---

## Issue Flags

### HIGH PRIORITY

| # | Issue | Category | Impact | Action Required |
|---|-------|----------|--------|-----------------|
| 1 | [issue] | [UBTI/ECI/199A/163(j)/State/PFIC/Other] | [description] | [action] |

### MEDIUM PRIORITY

| # | Issue | Category | Impact | Action Required |
|---|-------|----------|--------|-----------------|
| 1 | [issue] | [category] | [description] | [action] |

### LOW PRIORITY / INFORMATIONAL

| # | Issue | Category | Notes |
|---|-------|----------|-------|
| 1 | [issue] | [category] | [notes] |

---

## UBTI Analysis

[Summary of UBTI exposure for tax-exempt partners]

| Source | Amount | Risk Level |
|--------|--------|------------|
| [source] | $[amount] | [High/Medium/Low] |
| **Total Potential UBTI** | **$[total]** | |

---

## ECI / Withholding Analysis

[Summary for non-US partners]

| Income Type | Amount | Withholding Required | Withheld | Discrepancy |
|------------|--------|---------------------|----------|-------------|
| [type] | $[amount] | [rate]% | $[amount] | [amount] |

---

## Section 199A / QBI Summary

[QBI eligibility and limitation analysis]

---

## Section 163(j) Summary

[Business interest limitation and EBIE carryforward]

---

## State Filing Obligations

| State | Income | Est. Tax | Filing Required | Withholding |
|-------|--------|----------|----------------|-------------|
| [state] | $[amount] | $[amount] | [Yes/No] | $[amount] |

---

## Capital Account Reconciliation

| Element | Reported | Calculated | Status |
|---------|----------|------------|--------|
| Beginning Balance | $[amount] | $[amount] | [Match/Discrepancy] |
| + Contributions | $[amount] | | |
| + Net Income (Loss) | $[amount] | | |
| - Distributions | $[amount] | | |
| = Ending Balance | $[amount] | $[amount] | [Match/Discrepancy] |

---

## Filing Deadline Tracker

| Filing | Deadline | Status |
|--------|----------|--------|
| Form 1065 | [date] | [status] |
| K-1 Delivery | [date] | [status] |
| Partner Filing | [date] | [status] |
| State Returns | [varies] | [status] |

---

## LP-Specific Implications

### For Tax-Exempt Partners (Pensions, Endowments, IRAs)
[UBTI impact summary and recommended actions]

### For Non-US Partners
[ECI and withholding summary, treaty considerations]

### For Individual Partners
[199A QBI, 163(j), state filing, and estimated tax implications]

### For Corporate Partners
[Relevant corporate tax considerations]

---

## Recommended Next Steps

1. [ ] Address all HIGH priority issues with tax advisor before filing
2. [ ] Verify capital account reconciliation against fund administrator records
3. [ ] Confirm state filing obligations and withholding credits
4. [ ] Review UBTI exposure with tax-exempt LP's tax counsel
5. [ ] Verify ECI withholding amounts for non-US partners
6. [ ] Track EBIE carryforward at the partner level (if applicable)
7. [ ] Confirm estimated tax payment adjustments based on K-1 income
8. [ ] Retain K-1 and supporting schedules for minimum 7 years
```

---

## Phase 6: Present to User

After generating the report:

1. Display the **Completeness Score** prominently
2. List **HIGH Priority Issue Flags** with one-line descriptions
3. Summarize **UBTI exposure** (if tax-exempt partner) or **ECI exposure** (if non-US partner)
4. Show **State filing obligations** count
5. Show the full report
6. Ask: "Would you like me to review the fund's full compliance posture? Run `/fund check-compliance <file>`."
7. Mention: "Run `/fund report-pdf` to generate a professional PDF version of this tax review."

---

## Schedule K-1 Form Layout Parsing

When the input is an actual Schedule K-1 (Form 1065) PDF or scanned document, use the following IRS box structure to locate and extract each field.

### IRS Box Reference Map

**Part I — Information About the Partnership** (Boxes A–D)

| Box | Field | Extraction Notes |
|-----|-------|-----------------|
| A | Partnership's EIN | 9-digit number, format XX-XXXXXXX |
| B | Partnership name, address, city, state, ZIP | May span multiple lines |
| C | IRS Center where partnership return is filed | Text field; often "e-file" for electronically filed returns |
| D | Check if publicly traded partnership | Checkbox; affects UBTI analysis if checked |

**Part II — Information About the Partner** (Boxes E–N)

| Box | Field | Extraction Notes |
|-----|-------|-----------------|
| E | Partner's name, address, city, state, ZIP | Verify against investor records |
| F | Partner's identifying number (TIN/SSN/EIN) | May be masked (XXX-XX-XXXX) on partner copy |
| G | General or limited partner / domestic or foreign | Two checkboxes; both must be checked |
| H1 | Entity type of partner | Dropdown or text; e.g., individual, corporation, partnership, trust, IRA/SEP/Keogh, exempt org |
| H2 | If retirement plan | Checkbox; triggers UBTI analysis |
| I1 | Partner's share of liabilities: nonrecourse, qualified nonrecourse, recourse | Three separate dollar amounts |
| I2 | Partner's share of profit, loss, capital | Beginning and ending percentages for each |
| J | Partner's capital account analysis | See Section L detail below |
| K | Net unrecognized Section 704(c) gain/loss | Beginning and ending amounts |

**Section L — Partner's Capital Account Analysis** (within Part II)

Extract and verify arithmetic for all five components:

| Line | Field | Verification |
|------|-------|-------------|
| Beginning capital account | Opening balance | Must equal prior year ending balance |
| + Capital contributed during the year | Contributions | Cross-check against capital call records |
| + Current year net income (loss) | Net P&L allocated | Should reconcile to Part III income/loss lines |
| + Other increase (decrease) | Adjustments | Identify nature; ask for explanation if material |
| - Withdrawals and distributions | Distributions | Cross-check against Part III Line 19 |
| = Ending capital account | Closing balance | Must equal sum of above; flag arithmetic errors |

**Capital account method** (Tax Basis, GAAP, Section 704(b) book, or Other): note the method used and flag if it changed from the prior year.

**Part III — Partner's Share of Current Year Income, Deductions, Credits and Other Items** (Lines 1–21)

Lines with letter codes (boxes 11, 13, 15, 17, 20) require parsing each code and associated amount from the K-1 or attached supplemental statements:

| Box | Common Codes | Tax Flag |
|-----|-------------|---------|
| 11 | A (Other income), C (Section 1256 gain/loss), F (Section 743(b) adj.) | Review each code; Code F has basis implications |
| 13 | K (Excess business interest expense), W (Other deductions) | Code K triggers 163(j) carryforward at partner level |
| 15 | Various credit codes | Verify credit applies to partner's entity type |
| 17 | A (AMT depreciation adj.), B (Adjusted gain/loss) | AMT items require alternative minimum tax analysis |
| 20 | Z* (Section 199A QBI), AH (Gross receipts for 448(c)) | Z* requires QBI component statements; AH affects gross receipts tests |

### Cross-Reference with `/fund review-k1`

This skill (`/fund tax-review`) focuses on the **tax implications** of K-1 data: UBTI exposure, ECI and withholding, Section 199A eligibility, 163(j) limitations, state apportionment, and PFIC analysis.

For **data extraction and completeness** checking (field-by-field parsing, reconciliation to fund records, comparison across multiple K-1s), use `/fund review-k1` instead.

When both skills are run together:
1. Run `/fund review-k1` first to validate completeness and extract structured data
2. Pass the extracted data to `/fund tax-review` for tax implication analysis

### Key Tax Flags by Box Number

| Box | Flag Condition | Issue |
|-----|---------------|-------|
| Box 1 | Amount > $1,000 for tax-exempt investor | UBTI exposure from active business income |
| Box 16 | Any amount for non-US partner | ECI analysis required; withholding likely due |
| Box 14 | Any amount for individual LP | Self-employment earnings — unusual for limited partners; verify LP status |
| Box 17 | Any amount | AMT items require alternative minimum tax calculation at partner level |
| Box 20, Code Z* | Any amount | Section 199A QBI — attach QBI component statement; verify trade or business qualification |

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No document provided | Ask user to provide a K-1 schedule, tax package, or partnership return excerpt |
| Document is not a K-1 or tax document | Report that the document does not appear to be a tax-related fund document; suggest the appropriate `/fund` command |
| K-1 is a preliminary estimate | Analyze as provided but flag prominently that amounts are estimates subject to change; recommend re-review when final K-1 is issued |
| Multiple K-1s provided | Analyze each K-1 separately within the same report; compare for consistency if same fund/different years |
| Foreign partnership (non-US) | Note that analysis is primarily US-focused; flag Schedule K-3 requirements and recommend local tax advisor consultation |
| Missing supplemental schedules | Note which schedules are referenced but not provided; flag as incomplete for full analysis |
