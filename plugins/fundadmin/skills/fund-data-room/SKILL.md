---
name: fund-data-room
description: "Generates an ILPA-aligned virtual data room index across eight categories with Required/Recommended/Optional status, gap priorities, and access tiers by investor type. Use when the user runs `/fund data-room <type>` or asks how to organize a fundraising data room. Writes DATA-ROOM-[type]-[date].md."
---

# Virtual Data Room Organizer

You are the virtual data room organization engine for `/fund data-room`. You accept fund type and fundraising stage details and generate a comprehensive, ILPA-aligned data room structure with categorized folder hierarchies, document checklists with status indicators (Required / Recommended / Optional), missing document identification, and access permission recommendations by investor tier.

## When This Skill Is Invoked

The user runs `/fund data-room <type>` providing either:
- A description of the fund type and fundraising stage (e.g., "PE Fund IV, initial close")
- A file listing available documents for the data room
- Context from prior `/fund review-lpa`, `/fund review-ppm`, or `/fund ddq-respond` outputs

---

## Phase 1: Fund and Fundraising Context

### 1.1 Read the Input

Accept input from one of these sources:
- **Text description** — Fund type, strategy, fundraising stage, and any specific requirements
- **File path** — Use the Read tool to read a document list or fund summary
- **Prior analysis context** — Search for recent fund review outputs in the working directory

### 1.2 Required Context

| Field | Required? | Options |
|-------|-----------|---------|
| **Fund type** | Required | Private Equity, Venture Capital, Real Estate, Credit/Debt, Hedge Fund, Fund of Funds, Infrastructure, Secondaries |
| **Fundraising stage** | Required | Initial Close, Subsequent Close, Final Close, Secondary Sale, Re-Up (next fund) |
| **Fund number/vintage** | Important | Fund I (first-time), Fund II-III (emerging), Fund IV+ (established) |
| **Strategy** | Important | Buyout, Growth, Venture, Distressed, Opportunistic, Core, Core-Plus, Value-Add, etc. |
| **Target fund size** | Optional | Helps determine document depth expectations |
| **GP track record** | Optional | First-time fund vs. successor fund changes data room requirements |
| **Available documents** | Optional | List of documents already prepared (to identify gaps) |

### 1.3 Adjust for Fundraising Stage

| Stage | Data Room Focus |
|-------|----------------|
| **Initial Close** | Full data room — all categories populated; emphasis on PPM, LPA, track record, and team materials |
| **Subsequent Close** | Updated data room — add interim performance data, updated references, any portfolio activity since initial close |
| **Final Close** | Complete data room — all prior materials plus final LP list, amended LPA (if applicable), updated financials |
| **Secondary Sale** | Specialized data room — portfolio detail, NAV bridge, cash flow history, LP consent requirements, transfer docs |
| **Re-Up (Next Fund)** | Prior fund performance emphasis — audited financials, attribution, lessons learned, team continuity, strategy evolution |

---

## Phase 2: Generate Data Room Structure

### 2.1 Master Folder Structure (ILPA Best Practices)

Generate the complete data room hierarchy organized into these top-level categories:

#### Category 1: Fund Terms

| # | Document | Status | Description |
|---|----------|--------|-------------|
| 1.01 | Limited Partnership Agreement (LPA) | Required | Executed or near-final LPA |
| 1.02 | LPA Summary / Term Sheet | Required | Plain-English summary of key economic and governance terms |
| 1.03 | Private Placement Memorandum (PPM) | Required | Offering memorandum with strategy, risks, and terms |
| 1.04 | Subscription Agreement | Required | Template subscription documents for LP execution |
| 1.05 | Side Letter Template | Recommended | Template side letter showing negotiable provisions |
| 1.06 | Fee Schedule / Fee Letter | Required | Detailed management fee, carry, and expense terms |
| 1.07 | GP Commitment Letter | Recommended | Documentation of GP/principal co-investment commitment |
| 1.08 | LPAC Charter | Recommended | LP Advisory Committee composition, powers, and procedures |
| 1.09 | Investment Guidelines | Recommended | Detailed investment parameters and restrictions |
| 1.10 | Distribution Policy | Recommended | Distribution waterfall mechanics and timing |

#### Category 2: Track Record

| # | Document | Status | Description |
|---|----------|--------|-------------|
| 2.01 | Historical Performance Summary | Required | Gross and net IRR, TVPI, DPI by fund and vintage |
| 2.02 | Deal-Level Attribution | Required | Investment-by-investment performance with entry/exit detail |
| 2.03 | Case Studies (Top 3-5 Deals) | Required | Detailed narratives on best-performing investments |
| 2.04 | Loss Analysis | Recommended | Explanation of write-downs and write-offs |
| 2.05 | Prior Fund Audited Financial Statements | Required | Most recent 2-3 years of audited financials for prior funds |
| 2.06 | Prior Fund Capital Account Statements | Recommended | Sample LP capital account statements from prior funds |
| 2.07 | PME / Benchmark Comparison | Recommended | Performance vs. public market equivalents and peer benchmarks |
| 2.08 | J-Curve Analysis | Optional | Capital deployment and return timing analysis |
| 2.09 | Vintage Year Comparison | Optional | Performance relative to same-vintage peers |
| 2.10 | Co-Investment Track Record | Optional | Performance of co-investment opportunities offered |

#### Category 3: Team

| # | Document | Status | Description |
|---|----------|--------|-------------|
| 3.01 | Team Biographies | Required | Professional backgrounds of all investment professionals |
| 3.02 | Organizational Chart | Required | Firm structure showing reporting lines and committees |
| 3.03 | Compensation Structure Overview | Recommended | How professionals are incentivized (carry allocation, bonus) |
| 3.04 | Key Person Provisions | Required | Key person identification and trigger mechanisms |
| 3.05 | Succession Plan | Recommended | Leadership transition planning |
| 3.06 | Team Stability / Tenure | Recommended | Historical team turnover data |
| 3.07 | Diversity & Inclusion Data | Recommended | Team demographics, D&I initiatives, EDCI commitment |
| 3.08 | Advisory Board / Operating Partners | Optional | External advisors and their roles |
| 3.09 | Professional References | Recommended | Contact information for professional references |

#### Category 4: Operations

| # | Document | Status | Description |
|---|----------|--------|-------------|
| 4.01 | Service Provider List | Required | Auditor, legal counsel, fund administrator, custodian, prime broker |
| 4.02 | Compliance Manual (Summary) | Required | Overview of compliance policies and procedures |
| 4.03 | Valuation Policy | Required | Investment valuation methodology and governance |
| 4.04 | Business Continuity Plan (Summary) | Recommended | Disaster recovery and business continuity overview |
| 4.05 | Cybersecurity Policy (Summary) | Recommended | Information security framework and incident response |
| 4.06 | Operational Due Diligence Deck | Recommended | Comprehensive operational overview presentation |
| 4.07 | Sample Investor Reporting | Recommended | Example quarterly/annual reports sent to LPs |
| 4.08 | Cash Management Policy | Optional | Treasury and cash management procedures |
| 4.09 | Trade Allocation Policy | Optional | How investment opportunities are allocated across vehicles |
| 4.10 | Proxy Voting Policy | Optional | Policy on voting portfolio company proxies |

#### Category 5: Legal and Compliance

| # | Document | Status | Description |
|---|----------|--------|-------------|
| 5.01 | Form ADV Parts 1 and 2 | Required | SEC registration and brochure |
| 5.02 | Regulatory Registrations | Required | All registrations (SEC, state, NFA, FCA, etc.) |
| 5.03 | Litigation Disclosure | Required | Current and recent litigation involving the GP or funds |
| 5.04 | Regulatory Examination History | Recommended | Summary of SEC or other regulatory examinations |
| 5.05 | Insurance Certificates | Recommended | D&O, E&O, cyber liability, fidelity bond coverage |
| 5.06 | Code of Ethics | Recommended | Personal trading and ethics policies |
| 5.07 | Political Contributions Policy | Recommended | Pay-to-play compliance (Rule 206(4)-5) |
| 5.08 | Anti-Money Laundering Policy | Recommended | AML/KYC program overview |
| 5.09 | Conflicts of Interest Disclosure | Required | Identification and management of conflicts |
| 5.10 | Privacy Policy | Optional | Data protection and investor privacy |

#### Category 6: ESG

| # | Document | Status | Description |
|---|----------|--------|-------------|
| 6.01 | ESG Policy | Required (if applicable) | Firm-level ESG policy and integration approach |
| 6.02 | UN PRI Signatory Status | Recommended | PRI membership and assessment results |
| 6.03 | SFDR Classification | Required (if EU) | Article 6, 8, or 9 classification and disclosures |
| 6.04 | Sample ESG Reporting | Recommended | Example ESG reports from prior/current funds |
| 6.05 | TCFD Disclosure | Recommended | Climate-related financial disclosures |
| 6.06 | DEI Metrics (EDCI) | Recommended | ESG Data Convergence Initiative metrics |
| 6.07 | Impact Measurement Framework | Optional | For impact-focused funds: measurement methodology |

#### Category 7: Tax

| # | Document | Status | Description |
|---|----------|--------|-------------|
| 7.01 | Tax Structure Overview | Required | Fund structure diagram with tax treatment annotations |
| 7.02 | Estimated Tax Allocations | Recommended | Expected allocation methodology and tax character |
| 7.03 | UBTI / ECI Analysis | Required (if US) | Analysis of unrelated business taxable income and effectively connected income exposure |
| 7.04 | ERISA Analysis | Required (if applicable) | Plan asset test analysis and VCOC/REOC qualification |
| 7.05 | FATCA / CRS Classification | Recommended | Fund's classification under FATCA and CRS |
| 7.06 | State Tax Nexus Analysis | Optional | Analysis of state tax obligations for domestic investors |
| 7.07 | Sample K-1 | Optional | Example K-1 from a prior fund |
| 7.08 | Blocker Entity Structure | Optional | Description of tax-advantaged structures for tax-exempt/non-US investors |

#### Category 8: References and Due Diligence

| # | Document | Status | Description |
|---|----------|--------|-------------|
| 8.01 | LP Reference List | Required | Contact information for existing LP references |
| 8.02 | Portfolio Company References | Recommended | Contact information for portfolio company management teams |
| 8.03 | DDQ Responses (ILPA Template) | Required | Completed ILPA Due Diligence Questionnaire |
| 8.04 | Operational DD Materials | Recommended | Materials supporting operational due diligence review |
| 8.05 | Cybersecurity Assessment | Recommended | Third-party cybersecurity assessment results |
| 8.06 | SOC 1 / SOC 2 Reports | Recommended | Service organization control reports (fund admin, custodian) |
| 8.07 | Co-Investment Examples | Optional | Case studies and terms of prior co-investment opportunities |
| 8.08 | Background Check Authorization | Optional | Authorization forms for principal background checks |
| 8.09 | Financial Statements (GP Entity) | Optional | GP or management company financial statements |

---

### GP Portal Template Validation

When generating data room structure, validate against common GP portal templates:
- Allvue: check for required metadata fields per document type
- InvestorFlow: verify access permission groups align with LP tiers
- Flag any documents that exist in the vault but are not mapped to a data room folder

## Phase 3: Document Gap Analysis

### 3.1 Identify Available vs. Missing Documents

If the user provided a list of available documents, map them to the checklist:

| Document | Category | Status | Available? | Gap Priority |
|----------|----------|--------|-----------|-------------|
| LPA | Fund Terms | Required | [YES/NO] | [CRITICAL/HIGH/MEDIUM/LOW] |
| PPM | Fund Terms | Required | [YES/NO] | [CRITICAL/HIGH/MEDIUM/LOW] |
| ... | ... | ... | ... | ... |

### 3.2 Gap Priority Classification

| Priority | Criteria |
|----------|---------|
| **CRITICAL** | Required document that is missing — fundraising should not proceed without it |
| **HIGH** | Required or Recommended document that sophisticated LPs will expect |
| **MEDIUM** | Recommended document that enhances credibility but is not blocking |
| **LOW** | Optional document that differentiates from competitors |

### 3.3 Fund-Type-Specific Adjustments

Adjust document requirements based on fund type:

| Fund Type | Additional Required | Can Omit |
|-----------|-------------------|----------|
| **Venture Capital** | Portfolio company pipeline, sector thesis | Detailed attribution (early-stage marks unreliable) |
| **Real Estate** | Property-level data, appraisals, rent rolls | PME benchmark (use property index instead) |
| **Credit / Debt** | Loan book summary, default rates, recovery analysis | J-curve analysis (less applicable) |
| **Hedge Fund** | Strategy tear sheet, drawdown analysis, Sharpe ratio | Case studies (replaced by performance analytics) |
| **Fund of Funds** | Underlying manager list, portfolio construction, fee layering analysis | Deal-level attribution (replaced by manager selection track record) |
| **Secondaries** | Portfolio NAV detail, discount/premium analysis, seller motivation | PPM (may not apply for direct secondaries) |

---

## Phase 4: Access Permission Recommendations

### 4.1 Investor Tier Definitions

| Tier | Description | Access Level |
|------|-------------|-------------|
| **Tier 1 — Anchor / Seed** | First-close investors committing significant capital | Full access — all categories, all documents |
| **Tier 2 — Institutional** | Pension funds, endowments, sovereign wealth, insurance companies | Full access with potential NDAs for sensitive compensation data |
| **Tier 3 — Standard LP** | Fund of funds, family offices, high-net-worth individuals | Standard access — excludes detailed compensation, may exclude some references |
| **Tier 4 — Prospect** | LPs in early diligence, not yet committed | Limited access — Fund Terms (summary only), Track Record (summary), Team, ESG overview |
| **Tier 5 — Placement Agent** | Third-party distribution partners | Marketing materials, term sheet, performance summary; no LPA, no full DDQ |

### 4.2 Access Matrix

| Category | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|----------|--------|--------|--------|--------|--------|
| 1. Fund Terms | Full | Full | Full | Summary only | Term sheet only |
| 2. Track Record | Full | Full | Full | Summary only | Summary only |
| 3. Team | Full | Full | Bios + Org only | Bios only | Bios only |
| 4. Operations | Full | Full | Service providers + reporting | Overview only | None |
| 5. Legal & Compliance | Full | Full | Form ADV + litigation | Form ADV only | None |
| 6. ESG | Full | Full | Full | Policy only | Policy only |
| 7. Tax | Full | Full | Structure + UBTI | Structure only | None |
| 8. References & DD | Full | Full | DDQ + references | None | None |

---

## Phase 5: Generate Output

### 5.1 Compile the Data Room Index

Generate `DATA-ROOM-[type]-[date].md` with the following structure:

```markdown
# Virtual Data Room Index

> DISCLAIMER: This data room structure is AI-generated and does not
> constitute legal, financial, or compliance advice. Data room organization
> for fundraising involves regulatory considerations (PPM accuracy,
> marketing rule compliance, investor suitability) that require qualified
> fund formation counsel and compliance professionals. This index is a
> planning tool — always consult your legal counsel before distributing
> fund documents to prospective investors.

---

## Data Room Overview

| Field | Value |
|-------|-------|
| Fund Name | [name] |
| Fund Type | [type] |
| Strategy | [strategy] |
| Fundraising Stage | [initial close / subsequent close / etc.] |
| Target Fund Size | $[X] |
| Data Room Generated | [date] |

---

## Document Checklist Summary

| Category | Total Docs | Required | Recommended | Optional | Available | Missing |
|----------|-----------|----------|-------------|----------|-----------|---------|
| 1. Fund Terms | [N] | [N] | [N] | [N] | [N] | [N] |
| 2. Track Record | [N] | [N] | [N] | [N] | [N] | [N] |
| 3. Team | [N] | [N] | [N] | [N] | [N] | [N] |
| 4. Operations | [N] | [N] | [N] | [N] | [N] | [N] |
| 5. Legal & Compliance | [N] | [N] | [N] | [N] | [N] | [N] |
| 6. ESG | [N] | [N] | [N] | [N] | [N] | [N] |
| 7. Tax | [N] | [N] | [N] | [N] | [N] | [N] |
| 8. References & DD | [N] | [N] | [N] | [N] | [N] | [N] |
| **TOTAL** | **[N]** | **[N]** | **[N]** | **[N]** | **[N]** | **[N]** |

**Data Room Readiness**: [X]% of Required documents available

---

## Folder Structure

### 1. Fund Terms
[Full document list with status indicators from Phase 2 Category 1]

### 2. Track Record
[Full document list from Category 2]

### 3. Team
[Full document list from Category 3]

### 4. Operations
[Full document list from Category 4]

### 5. Legal & Compliance
[Full document list from Category 5]

### 6. ESG
[Full document list from Category 6]

### 7. Tax
[Full document list from Category 7]

### 8. References & Due Diligence
[Full document list from Category 8]

---

## Missing Documents — Gap Analysis

### CRITICAL Gaps (Must Address Before Fundraising)

| # | Document | Category | Why Critical |
|---|----------|----------|-------------|
| 1 | [document] | [category] | [explanation] |

### HIGH Priority Gaps

| # | Document | Category | Impact |
|---|----------|----------|--------|
| 1 | [document] | [category] | [explanation] |

### MEDIUM Priority Gaps

| # | Document | Category | Notes |
|---|----------|----------|-------|
| 1 | [document] | [category] | [explanation] |

---

## Access Permission Matrix

[Table from Phase 4.2]

### Tier Definitions
[Definitions from Phase 4.1]

---

## Data Room Best Practices

1. **Version control** — Date-stamp all documents; maintain a version log for updated materials
2. **Watermarking** — Apply investor-specific watermarks to track document distribution
3. **Activity tracking** — Monitor which documents each prospect reviews and for how long
4. **NDA first** — Require executed NDA before granting Tier 3+ access
5. **Regular updates** — Update performance data quarterly; refresh financials when new audits are available
6. **Q&A log** — Maintain a running Q&A log to track investor questions and GP responses
7. **Redaction review** — Ensure sensitive data (individual compensation, LP names from prior funds) is appropriately redacted per tier

---

## Recommended Next Steps

1. [ ] Prepare all CRITICAL gap documents before opening the data room
2. [ ] Have fund counsel review all materials for regulatory compliance
3. [ ] Set up data room platform with appropriate access controls per tier
4. [ ] Run `/fund review-lpa` on the LPA before including it in the data room
5. [ ] Run `/fund review-ppm` on the PPM for accuracy and completeness
6. [ ] Run `/fund ddq-respond` to prepare DDQ responses for inclusion
7. [ ] Run `/fund esg-report` to generate ESG disclosures if not already prepared
8. [ ] Configure investor-specific watermarking and activity tracking
```

### 5.2 Present to User

After generating the output:

1. Confirm the file was generated: "Data room index generated: `DATA-ROOM-[type]-[date].md`"
2. State the file location (absolute path)
3. Summarize the structure: "[N] documents across 8 categories: [N] Required, [N] Recommended, [N] Optional"
4. Report readiness: "Data room is [X]% ready — [N] Required documents available, [N] CRITICAL gaps to address"
5. Highlight the most important missing documents (CRITICAL gaps)
6. Note any fund-type-specific adjustments made
7. Suggest: "Run `/fund review-lpa` and `/fund review-ppm` to validate key documents before including them"

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No fund type provided | List the available fund types and ask user to select one |
| No fundraising stage provided | Default to "Initial Close" (most comprehensive) and disclose the assumption |
| Unknown fund type | Use the Private Equity template as a base; note the assumption; ask user to confirm or clarify |
| Available document list unclear | Generate the full checklist with all items marked as "Status: TBD — verify availability" |
| First-time fund manager | Adjust requirements: no prior fund financials required; emphasize team track record from prior employers; note that first-fund data rooms require extra diligence materials |
| Prior analysis not found | Proceed with user-provided context; note that prior `/fund review-lpa` output would enhance the data room recommendations |
