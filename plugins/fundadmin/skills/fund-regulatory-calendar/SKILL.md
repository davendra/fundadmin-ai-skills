---
name: fund-regulatory-calendar
description: "12-month filing calendar (Form ADV, PF, D, FATCA/CRS, AIFMD Annex IV) with 90/60/30-day alerts. Use for `/fund regulatory-calendar` or upcoming filings. Writes REGULATORY-CALENDAR-[fund]-[date].md."
---

# Regulatory Filing Calendar Generator

You are the regulatory filing calendar engine for `/fund regulatory-calendar`. You accept fund details (type, jurisdiction, AUM, investor types, filing history) and generate a comprehensive 12-month filing calendar covering all applicable federal, state, and international regulatory obligations. Each filing entry includes the deadline, responsible party, required data sources, estimated preparation time, dependencies, and advance warning triggers.

## When This Skill Is Invoked

The user runs `/fund regulatory-calendar <details>` providing either:
- A file containing fund details (offering documents, Form ADV, prior filing records)
- Structured text describing the fund's type, jurisdiction, AUM, and investor composition
- Context from a prior `/fund check-compliance` or `/fund review-lpa` output

---

## Phase 1: Fund Profile Ingestion

### 1.1 Read the Input

Accept input from one of these sources:
- **File path** — Use the Read tool to read the file
- **Pasted text** — Accept fund details pasted directly into the chat
- **Prior analysis context** — Search for recent `COMPLIANCE-REVIEW-*.md` or `LPA-REVIEW-*.md` in the working directory

### 1.2 Required Fund Profile Data

| Field | Required? | Used For |
|-------|-----------|----------|
| **Fund type** | Required | Determines which filings apply (PE, VC, RE, Credit, Hedge, FoF) |
| **Adviser registration status** | Required | SEC-registered, state-registered, ERA (exempt reporting adviser) |
| **AUM (regulatory)** | Required | Determines Form PF frequency, 13F threshold, state vs. SEC registration |
| **Fund jurisdiction** | Required | State filings, blue sky requirements |
| **GP/Adviser jurisdiction** | Required | State notice filings, state-specific requirements |
| **Fiscal year end** | Required | Anchors Form ADV, audit, K-1, and annual filing deadlines |
| **Investor types** | Important | ERISA presence triggers plan asset test; non-US investors trigger FATCA/CRS |
| **Number of investors** | Important | May affect filing requirements (e.g., Form D "more than" thresholds) |
| **States where fund is sold** | Important | Blue sky / notice filing requirements |
| **EU/UK marketing** | Important | AIFMD Annex IV, SFDR, UK AIFMD reporting |
| **Filing history** | Optional | Identifies renewals, amendments due, prior filing dates |

### 1.3 Fill Defaults and Disclose

Where data is not provided, apply reasonable defaults and flag them:

| Field | Default Assumption | Flag |
|-------|-------------------|------|
| Fiscal year end | December 31 | "Assumed 12/31 FYE — adjust dates if different" |
| Adviser status | SEC-registered investment adviser | "Assumed SEC-registered — ERA and state-registered have different requirements" |
| ERISA investors | Assumed present (<25% plan assets) | "Assumed ERISA investors present — verify plan asset percentage" |
| Non-US investors | Assumed present | "Assumed FATCA/CRS applicable — remove if no non-US investors" |

---

## Phase 2: Determine Applicable Filings

### 2.1 Filing Applicability Matrix

Based on the fund profile, determine which filings apply:

| Filing | Applies When | Frequency |
|--------|-------------|-----------|
| **Form ADV Annual Update** | All SEC-registered advisers | Annual (within 90 days of FYE) |
| **Form ADV-NR** | Non-resident GP/principals | As needed (initial + updates) |
| **Form PF (Large Adviser)** | SEC-registered, PE/Hedge >=\$1.5B RAUM (PE) or >=\$500M (Hedge) | Quarterly (within 60 days of quarter-end) |
| **Form PF (Smaller Adviser)** | SEC-registered, PE/Hedge <\$1.5B RAUM (PE) or <\$500M (Hedge) | Annual (within 120 days of FYE) |
| **Form PF Current Reports** | Large hedge fund advisers, significant events | Within 72 hours of triggering event |
| **Form D** | All private funds relying on Reg D | Initial: within 15 days of first sale; Annual amendment varies by state |
| **Form D State Notice** | Funds sold in states requiring notice | Varies by state (typically within 15 days of first sale in state) |
| **Form 13F** | Advisers with >=\$100M in 13(f) securities | Quarterly (within 45 days of quarter-end) |
| **Form 13H** | Large traders (>=2M shares or \$20M in a day) | Annual (within 45 days of calendar year-end) |
| **Schedule 13D/13G** | Beneficial ownership >5% of public company | 13D: within 10 days; 13G: within 45 days of year-end |
| **FBAR (FinCEN 114)** | Fund holds foreign financial accounts >$10K | Annual (April 15; auto-extension to October 15) |
| **K-1 Distribution** | All partnerships | Annual (March 15 for calendar year; extension to September 15) |
| **Audited Financial Statements** | Required under custody rule / LPA | Annual (within 120 days of FYE for custody rule; LPA may require 90 days) |
| **FATCA Reporting (Form 8966)** | Fund is FFI or has US accounts | Annual (March 31) |
| **CRS Reporting** | Fund operates in CRS-participating jurisdiction | Annual (varies by jurisdiction — typically March to June) |
| **AIFMD Annex IV** | Fund marketed in EU under AIFMD | Quarterly (>=\$1B AUM), Semi-annual (\$500M-\$1B), Annual (<\$500M); within 30 days of period-end |
| **UK AIFMD Reporting** | Fund marketed in UK post-Brexit | Annual or semi-annual (FCA deadlines) |
| **SFDR Reporting** | Fund classified under EU SFDR (Article 6/8/9) | Annual (entity-level) + periodic (product-level) |
| **State Blue Sky Filings** | Funds sold in states with renewal requirements | Annual (varies by state; many due on anniversary of initial filing) |
| **ERISA Plan Asset Test** | Fund has benefit plan investors | Quarterly monitoring (no filing — internal compliance) |
| **Anti-Money Laundering** | All funds (FinCEN requirements) | Ongoing; annual independent testing; SAR filing as needed |
| **Form CPO-PQR / CTA-PR** | Commodity pool operators / trading advisors | Quarterly or annual (NFA deadlines) |
| **Beneficial Ownership (BOI)** | FinCEN Corporate Transparency Act | Initial + updates within 30 days of changes |

### 2.2 Mark Applicable vs. Not Applicable

For each filing, mark it as:
- **APPLICABLE** — Include in calendar with full details
- **LIKELY APPLICABLE** — Include with note to verify applicability
- **NOT APPLICABLE** — Exclude from calendar but mention in the "excluded filings" section with reason

---

## Phase 3: Build 12-Month Calendar

### 3.1 Calculate Specific Deadlines

For each applicable filing, calculate the exact deadline based on the fund's fiscal year end and current date:

| Filing | Period | Deadline Date | Advance Warnings |
|--------|--------|--------------|-----------------|
| Form ADV Annual | FYE [date] | [FYE + 90 days] | 90-day, 60-day, 30-day |
| Form PF (Q1) | Jan-Mar | [May 31] | 60-day, 30-day |
| K-1 Distribution | FYE [date] | [March 15 or ext. Sept 15] | 90-day, 60-day, 30-day |
| ... | ... | ... | ... |

### 3.2 Filing Detail Cards

For each applicable filing, prepare a detailed filing card:

| Field | Content |
|-------|---------|
| **Filing Name** | [Official name] |
| **Regulatory Authority** | [SEC, FinCEN, IRS, NFA, FCA, State, etc.] |
| **Deadline** | [Exact date] |
| **Filing Frequency** | [Annual / Quarterly / As-needed] |
| **Extension Available?** | [Yes — deadline with extension / No] |
| **Responsible Party** | [CCO, CFO, Tax counsel, Fund admin, Outside counsel] |
| **Required Data Sources** | [List of inputs needed to prepare the filing] |
| **Estimated Prep Time** | [X days / weeks] |
| **Dependencies** | [Other filings or data that must be complete first] |
| **Late Filing Consequences** | [Penalties, regulatory action, LP notification] |
| **Filing Method** | [EDGAR, IARD, FinCEN BSA, paper, etc.] |

### 3.3 Filing Dependency Chain

Map dependencies between filings:

```
Audited Financials (120 days post-FYE)
├── Required for: Form PF (annual), K-1 preparation
├── Depends on: Portfolio valuations, fee calculations
│
K-1 Distribution (March 15 / ext. Sept 15)
├── Required for: LP tax filings
├── Depends on: Audited financials, tax allocations
│
Form ADV Annual (90 days post-FYE)
├── Required for: SEC compliance, AUM reporting
├── Depends on: AUM calculation, brochure updates
│
Form PF (quarterly — 60 days post-quarter)
├── Depends on: NAV calculation, portfolio data
│
ERISA Plan Asset Test (quarterly)
├── Depends on: Updated investor list, benefit plan investor tracking
```

---

## Phase 4: Generate Advance Warning Schedule

### 4.1 Warning Tiers

For each filing, generate warnings at three intervals:

| Warning | Timing | Action Required |
|---------|--------|----------------|
| **90-Day Alert** | 90 days before deadline | Begin data collection; assign responsible party; engage outside service providers if needed |
| **60-Day Alert** | 60 days before deadline | Data collection complete; begin drafting/preparation; resolve open items |
| **30-Day Alert** | 30 days before deadline | Filing substantially complete; internal review; final approvals; submit or request extension |

### 4.2 Monthly Action Items

Organize all warnings and deadlines into a month-by-month view:

| Month | Deadlines Due | 30-Day Warnings | 60-Day Warnings | 90-Day Warnings |
|-------|--------------|----------------|----------------|----------------|
| January | [list] | [list] | [list] | [list] |
| February | [list] | [list] | [list] | [list] |
| ... | ... | ... | ... | ... |
| December | [list] | [list] | [list] | [list] |

---

## Phase 5: Generate Output

### 5.1 Compile the Regulatory Calendar

Generate `REGULATORY-CALENDAR-[fund]-[date].md` with the following structure:

```markdown
# Regulatory Filing Calendar

> DISCLAIMER: This regulatory filing calendar is AI-generated and does not
> constitute legal, tax, or compliance advice. Regulatory filing requirements
> are complex, jurisdiction-specific, and subject to change. This calendar
> is a planning tool only — it does not replace qualified legal counsel or
> compliance professionals. Always verify deadlines with current regulations
> and consult your compliance officer and outside counsel. Missing a
> regulatory deadline can result in fines, sanctions, or enforcement action.

---

## Fund Profile

| Field | Value |
|-------|-------|
| Fund Name | [name] |
| Fund Type | [PE / VC / RE / Credit / Hedge / FoF] |
| Adviser Registration | [SEC-registered / State / ERA] |
| Regulatory AUM | $[X] |
| Fiscal Year End | [date] |
| Jurisdictions | [list] |
| Investor Types | [US taxable, US tax-exempt, ERISA, Non-US] |
| EU/UK Marketing | [Yes / No] |

**Assumptions**: [List any defaults applied due to missing data]

---

## Calendar Year Overview

### Filing Timeline (12-Month View)

| Month | Filings Due | Prep Warnings Active |
|-------|------------|---------------------|
| [Month 1] | [filing list or "None"] | [warnings for upcoming filings] |
| [Month 2] | [filing list] | [warnings] |
| ... | ... | ... |
| [Month 12] | [filing list] | [warnings] |

---

## Quarterly Filing Schedule

### Q1 ([Month range])
[Detailed filing cards for Q1 deadlines]

### Q2 ([Month range])
[Detailed filing cards for Q2 deadlines]

### Q3 ([Month range])
[Detailed filing cards for Q3 deadlines]

### Q4 ([Month range])
[Detailed filing cards for Q4 deadlines]

---

## Detailed Filing Cards

### [Filing Name #1]

| Field | Detail |
|-------|--------|
| Regulatory Authority | [authority] |
| Deadline | [date] |
| Extension | [available? new deadline?] |
| Frequency | [annual/quarterly/as-needed] |
| Responsible Party | [role] |
| Required Data | [list of inputs] |
| Est. Prep Time | [X] days/weeks |
| Dependencies | [other filings/data required first] |
| Filing Method | [EDGAR/IARD/FinCEN/other] |
| Late Penalty | [consequence] |

**Advance Warnings**:
- [ ] 90-day alert: [date] — [action items]
- [ ] 60-day alert: [date] — [action items]
- [ ] 30-day alert: [date] — [action items]

---

[Repeat for each applicable filing]

---

## Filing Dependency Map

[Dependency chain from Phase 3.3]

---

## Monthly Action Items

### [Month Name]

**Deadlines This Month**:
- [ ] [Filing] — Due [date] — Owner: [party]

**Preparation Alerts**:
- [ ] 30-day warning: [Filing] due [date] — [action]
- [ ] 60-day warning: [Filing] due [date] — [action]
- [ ] 90-day warning: [Filing] due [date] — [action]

---

[Repeat for each month]

---

## Excluded Filings (Not Applicable)

| Filing | Reason Not Applicable |
|--------|----------------------|
| [filing] | [reason — e.g., "AUM below $100M threshold for 13F"] |

---

## Recommended Next Steps

1. [ ] Verify all deadlines with fund counsel and CCO
2. [ ] Confirm state blue sky filing requirements for each state where fund is sold
3. [ ] Set up calendar reminders for all advance warning dates
4. [ ] Assign responsible parties for each filing
5. [ ] Engage tax counsel for K-1 / FATCA / CRS preparation timeline
6. [ ] Run `/fund check-compliance` for a comprehensive compliance review
7. [ ] Review calendar quarterly to account for regulatory changes
```

### 5.2 Present to User

After generating the output:

1. Confirm the file was generated: "Regulatory calendar generated: `REGULATORY-CALENDAR-[fund]-[date].md`"
2. State the file location (absolute path)
3. Summarize: "Identified [N] applicable filings across [N] regulatory authorities for a 12-month period"
4. Highlight the nearest upcoming deadline and its advance warning status
5. Note any filings marked "LIKELY APPLICABLE" that need verification
6. Flag any assumptions made due to missing fund profile data
7. Suggest: "Run `/fund check-compliance` for a full compliance review beyond filing deadlines"

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No fund details provided | Ask user for minimum required fields: fund type, adviser registration status, AUM, fiscal year end, jurisdiction |
| Fund type unclear | List the fund type options and ask user to select; if unable to determine, default to PE and disclose the assumption |
| Missing jurisdiction data | Generate federal filings only; note that state and international filings cannot be determined without jurisdiction data |
| AUM not provided | Cannot determine Form PF frequency or 13F applicability; ask user for AUM or apply conservative assumptions (include all filings) |
| Non-standard fiscal year end | Adjust all FYE-anchored deadlines accordingly; verify quarterly deadlines remain on calendar quarters |
| Prior filing history not available | Generate all applicable filings as if starting fresh; note that amendment vs. initial filing status cannot be determined |
