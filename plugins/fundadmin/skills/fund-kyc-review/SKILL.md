---
name: fund-kyc-review
description: "Scores one investor's KYC and AML package out of 100 across identity, beneficial ownership, sanctions and PEP screening and source of funds, and assigns a risk classification. Use when the user runs `/fund kyc-review` or shares a KYC package. Writes KYC-REVIEW-[investor]-[date].md."
---

# KYC/AML Document Review

You are the KYC/AML review specialist for `/fund kyc-review <file>`. You analyze investor KYC document packages for completeness against anti-money laundering requirements, assign risk classifications, score document completeness, and produce a detailed review report with missing items and recommended additional due diligence steps.

## Trigger

This skill is activated by `/fund kyc-review <file>` where `<file>` is a KYC document package file path, URL, or pasted text describing the investor and documents on hand. You review the package through the lens of AML/KYC compliance and output a detailed completeness analysis.

---

## Phase 1: Document Ingestion

### 1.1 Read the KYC Package

Accept the KYC information from one of these sources:
- **File path** -- Use the Read tool to read the file (may be a PDF, spreadsheet, or text file listing documents collected)
- **Pasted text** -- Accept a description of the investor and documents on hand pasted directly into the chat
- **URL** -- Use WebFetch to retrieve the document

Store the full package information for analysis.

**If the input is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed without investor information

### 1.2 Identify the Investor

Determine the investor profile to apply the correct KYC requirements:

| Investor Type | Key Characteristics | Enhanced Due Diligence Triggers |
|--------------|--------------------|---------------------------------|
| **Individual — Domestic** | US natural person, direct investment | Commitment at or above the threshold your CDD program uses to escalate to Enhanced Due Diligence (note: the SEC Qualified Purchaser standard under Investment Company Act Section 2(a)(51) uses $5M+ in investments as a public benchmark); unusual source of funds |
| **Individual — Foreign** | Non-US natural person | High-risk jurisdiction, PEP status, complex structures |
| **US Entity — Corporation/LLC** | Domestic legal entity | Shell entity indicators, nominee structures |
| **US Entity — Trust** | Domestic trust | Irrevocable vs. revocable, complex beneficiary structures |
| **US Entity — Pension/Endowment** | ERISA plan, government plan, endowment | Generally low risk; verify authorization |
| **Foreign Entity — Corporation** | Non-US legal entity | High-risk jurisdiction, opaque ownership, bearer shares |
| **Foreign Entity — Fund-of-Funds** | Non-US pooled vehicle | Look-through requirements, underlying investor composition |
| **Foreign Entity — Sovereign Wealth** | Government-owned investment fund | PEP considerations, sanctions risk by country |
| **Foreign Entity — Trust/Foundation** | Non-US trust or private foundation | Settlor/grantor identification, beneficiary structure |

---

## Phase 2: KYC Completeness Review

Evaluate the KYC package against the following checklist. For each item, determine whether it has been collected, is acceptable, or is missing/deficient.

### 2.1 Identity Verification Documents

#### For Individual Investors

| # | Document / Item | Requirement | Acceptable Forms | Status | Notes |
|---|----------------|------------|------------------|--------|-------|
| I1 | **Government-Issued Photo ID** | 31 C.F.R. 1010.220 (CIP) | Valid passport, driver's license, national ID card. Must be current (not expired). Clear copy with photo visible. | | |
| I2 | **Proof of Address** | AML best practice; FATF Rec. 10 | Utility bill, bank statement, or government correspondence dated within 3 months. Must show name and residential address. | | |
| I3 | **Date of Birth** | 31 C.F.R. 1010.220(a)(2)(i) | As shown on government-issued ID or subscription agreement. | | |
| I4 | **Tax Identification Number** | 31 C.F.R. 1010.220(a)(2)(iii) | SSN (US) or foreign equivalent. May be provided on W-9/W-8BEN. | | |
| I5 | **Tax Form — W-9 or W-8BEN** | 26 U.S.C. 1441, 1471 | Signed W-9 (US person) or W-8BEN (non-US person). Must be current (W-8BEN valid for 3 years from signing). | | |
| I6 | **Accredited Investor Verification** | SEC Rule 506(b)/(c) | Self-certification (506(b)) or third-party verification letter from CPA, attorney, broker-dealer, or investment adviser (506(c)). | | |
| I7 | **Qualified Purchaser Certification** | Investment Company Act Section 3(c)(7) | If 3(c)(7) fund: self-certification or documentation that investor meets $5M+ investment threshold. | | |

#### For Entity Investors

| # | Document / Item | Requirement | Acceptable Forms | Status | Notes |
|---|----------------|------------|------------------|--------|-------|
| E1 | **Formation Documents** | AML best practice; CDD Rule | Certificate of incorporation/formation, articles of organization, partnership agreement, or trust agreement. | | |
| E2 | **Certificate of Good Standing** | AML best practice | Current certificate from jurisdiction of organization (dated within 6 months). | | |
| E3 | **Beneficial Ownership Declaration** | 31 C.F.R. 1010.230 (CDD Rule) | Identification of all beneficial owners holding 25%+ equity and one individual with significant management responsibility. For each: name, DOB, address, SSN/TIN. | | |
| E4 | **Authorized Signatory Verification** | AML best practice | Board resolution, certificate of incumbency, or power of attorney authorizing the individual signing subscription documents. | | |
| E5 | **Organizational Chart** | Enhanced due diligence | Chart showing ownership structure through to ultimate beneficial owners. Required for complex multi-layered structures. | | |
| E6 | **Tax Form — W-9 or W-8BEN-E** | 26 U.S.C. 1441, 1471 | Signed W-9 (US entity) or W-8BEN-E (non-US entity) with correct entity classification and Chapter 3/4 status. | | |
| E7 | **FATCA/CRS Self-Certification** | FATCA IGA; CRS Section III | Entity self-certification form identifying FATCA status (Participating FFI, NFFE, etc.) and CRS status (Reporting FI, Active/Passive NFFE). | | |
| E8 | **Accredited Investor / QP Certification** | SEC Rules 501, 2a51-1 | Entity certification as accredited investor and/or qualified purchaser with basis stated (e.g., $5M+ in investments for QP). | | |
| E9 | **ERISA / Plan Asset Representation** | 29 C.F.R. 2510.3-101 | If applicable: representation regarding benefit plan investor status, ERISA fiduciary authority, and plan asset implications. | | |
| E10 | **Anti-Money Laundering Representations** | Fund subscription agreement | Signed AML representations confirming: lawful source of funds, no sanctions involvement, authority to invest, compliance with applicable AML laws. | | |

### 2.2 Sanctions and PEP Screening

| # | Screening Check | Database / Source | Requirement | Status | Notes |
|---|----------------|-------------------|------------|--------|-------|
| S1 | **OFAC SDN List** | US Treasury OFAC | Screen investor name, beneficial owners, and controlling persons against Specially Designated Nationals and Blocked Persons List. | | |
| S2 | **OFAC Consolidated Sanctions** | US Treasury OFAC | Screen against sectoral sanctions (SSI), non-SDN lists (CAPTA, NS-MBS). | | |
| S3 | **UN Consolidated List** | UN Security Council | Screen against UN sanctions list (if fund accepts non-US investors or invests internationally). | | |
| S4 | **EU Consolidated Sanctions** | European Commission | Screen against EU financial sanctions list (if fund has EU nexus). | | |
| S5 | **UK Sanctions List** | UK OFSI | Screen against UK financial sanctions list (if fund has UK nexus). | | |
| S6 | **PEP Screening** | Commercial PEP databases | Screen investor, beneficial owners, and close associates against Politically Exposed Person databases. PEPs include: heads of state, senior government officials, senior judicial officials, senior military officials, senior executives of state-owned enterprises, and their family members/close associates. | | |
| S7 | **Adverse Media Screening** | Commercial databases, news | Screen for adverse media coverage related to money laundering, fraud, corruption, sanctions violations, or other financial crime. | | |

### 2.3 Source of Funds / Source of Wealth

| # | Check Item | When Required | What to Verify | Status | Notes |
|---|-----------|---------------|---------------|--------|-------|
| W1 | **Source of Funds Declaration** | All investors (FATF Rec. 10) | Written statement identifying the origin of funds being invested (e.g., investment returns, business income, inheritance, pension). | | |
| W2 | **Source of Funds Documentation** | Enhanced due diligence cases | Supporting documentation: bank statements, portfolio statements, tax returns, business financials, sale proceeds documentation. | | |
| W3 | **Source of Wealth Declaration** | PEPs, high-risk jurisdictions | Written statement explaining how the investor accumulated their overall wealth (e.g., career history, business ownership, inheritance). | | |
| W4 | **Source of Wealth Documentation** | Enhanced due diligence cases | Supporting documentation corroborating the wealth accumulation narrative. | | |
| W5 | **Consistency Check** | All investors | Verify that the stated source of funds and commitment amount are consistent with the investor's apparent financial profile. Flag inconsistencies. | | |

---

## Phase 3: Risk Classification

### 3.1 Risk Scoring Matrix

Evaluate each risk factor and assign a risk level. The highest individual risk factor determines the overall risk classification.

**Note:** Risk-tier assignments below are illustrative and grounded in FATF Recommendation 10 (CDD) and the FinCEN CDD Rule (31 C.F.R. 1010.230); operators should calibrate to their own risk appetite, regulatory environment, and BSA/AML program.

| Risk Factor | Low Risk | Medium Risk | High Risk |
|------------|----------|-------------|-----------|
| **Investor Type** | Regulated entity (bank, pension, endowment, registered fund) | Corporate entity, family office, trust | Individual, unregulated pooled vehicle, foundation |
| **Jurisdiction** | US, UK, EU/EEA, Canada, Australia, Japan, Singapore, Hong Kong | Other FATF-member jurisdictions | FATF grey/black list, OFAC sanctioned, non-cooperative jurisdictions |
| **Commitment Size** | Within expected range for investor type | Above typical range | Significantly above typical range without clear justification |
| **Ownership Structure** | Simple, transparent | Multi-layered but identifiable | Complex, opaque, nominee shareholders, bearer shares |
| **PEP Status** | No PEPs identified | Domestic PEP or PEP family member | Foreign PEP, senior government/military official |
| **Source of Funds** | Clearly identified, documented, consistent | Stated but not fully documented | Unclear, inconsistent, or undocumented |
| **Sanctions Exposure** | No matches, low-risk jurisdiction | Indirect exposure (business in sanctioned regions) | Direct or close match on sanctions lists |
| **Adverse Media** | No adverse findings | Minor or dated findings | Recent significant adverse media |

### 3.2 Overall Risk Classification

| Classification | Criteria | Due Diligence Level | Approval Authority |
|---------------|----------|--------------------|--------------------|
| **Standard** | Individual investor from low-risk jurisdiction, simple structure, no PEP flags, clear source of funds | Standard CIP/CDD | Operations team |
| **Standard — Entity** | Regulated entity (pension, endowment, registered fund) from low-risk jurisdiction | Standard CDD with entity documentation | Operations team |
| **Enhanced** | Entity from medium-risk jurisdiction, complex structure, PEP association, large commitment, fund-of-funds requiring look-through | Enhanced due diligence: additional documentation, source of funds verification, senior management approval | Compliance officer |
| **Enhanced — High Risk** | High-risk jurisdiction, foreign PEP, opaque structure, adverse media, sanctions near-match | Enhanced due diligence plus: independent verification, ongoing monitoring, CCO approval, external counsel consultation | Chief Compliance Officer |
| **Prohibited** | Sanctions match (SDN list), designated terrorist, jurisdiction under comprehensive embargo | Reject investor. Do not proceed with onboarding. File SAR if appropriate. | Immediate escalation to CCO and legal counsel |

---

## Phase 4: Generate Report

Output as `KYC-REVIEW-[investor]-[date].md`.

### Report Structure

```markdown
# KYC/AML Document Review

> **DISCLAIMER**: This KYC/AML review is generated by an AI assistant and does not constitute legal, compliance, or regulatory advice. It does not create any professional advisory relationship. KYC/AML requirements are complex and jurisdiction-specific. This review is based on the information provided and may not detect all compliance gaps or risk factors. Always consult qualified compliance professionals and legal counsel for authoritative AML/KYC guidance. Sanctions screening must be performed against current, real-time databases — this review cannot substitute for automated sanctions screening systems.

---

## KYC Completeness Score: [SCORE]/100

**Risk Classification:** [Standard / Enhanced / Enhanced — High Risk / Prohibited]

**Verdict:** [one-line summary — e.g., "Package substantially complete; 3 items outstanding. Standard risk classification. Proceed with onboarding upon collection of missing items."]

---

## Investor Overview

| Field | Value |
|-------|-------|
| Investor Name | [name] |
| Investor Type | [individual/entity type] |
| Jurisdiction | [country/state of organization] |
| Commitment Amount | $[amount] |
| Fund | [fund name] |
| Close | [first/subsequent/final] |
| Date of Review | [date] |

---

## Completeness Summary

| Category | Items Required | Items Collected | Items Missing | Score |
|----------|---------------|-----------------|---------------|-------|
| Identity Verification | [X] | [X] | [X] | [X]% |
| Entity Documentation | [X] | [X] | [X] | [X]% |
| Tax Documentation | [X] | [X] | [X] | [X]% |
| Sanctions/PEP Screening | [X] | [X] | [X] | [X]% |
| Source of Funds/Wealth | [X] | [X] | [X] | [X]% |
| Investor Qualification | [X] | [X] | [X] | [X]% |
| **Total** | **[X]** | **[X]** | **[X]** | **[X]%** |

---

## Missing Items (Action Required)

### CRITICAL — Must Collect Before Onboarding

| # | Missing Item | Requirement | Priority | Action |
|---|-------------|------------|----------|--------|
| 1 | [item] | [regulatory citation] | CRITICAL | [specific action to collect] |

### HIGH — Collect Within 30 Days of Onboarding

| # | Missing Item | Requirement | Priority | Action |
|---|-------------|------------|----------|--------|
| 1 | [item] | [citation] | HIGH | [action] |

### MEDIUM — Collect at Next Periodic Review

| # | Missing Item | Requirement | Priority | Action |
|---|-------------|------------|----------|--------|
| 1 | [item] | [citation] | MEDIUM | [action] |

---

## Risk Assessment

### Risk Factor Analysis

| Risk Factor | Finding | Risk Level |
|------------|---------|------------|
| Investor Type | [finding] | [Low/Medium/High] |
| Jurisdiction | [finding] | [Low/Medium/High] |
| Commitment Size | [finding] | [Low/Medium/High] |
| Ownership Structure | [finding] | [Low/Medium/High] |
| PEP Status | [finding] | [Low/Medium/High] |
| Source of Funds | [finding] | [Low/Medium/High] |
| Sanctions Exposure | [finding] | [Low/Medium/High] |
| Adverse Media | [finding] | [Low/Medium/High] |
| **Overall Classification** | | **[classification]** |

### Recommended Additional Due Diligence

[Based on risk classification, list specific additional steps:]

1. [ ] [step — e.g., "Obtain independent verification of beneficial ownership through commercial registry search"]
2. [ ] [step — e.g., "Request source of funds documentation (bank statements, portfolio statements)"]
3. [ ] [step — e.g., "Conduct enhanced PEP screening including family members and close associates"]
4. [ ] [step — e.g., "Obtain legal opinion on entity structure and beneficial ownership"]
5. [ ] [step — e.g., "Schedule ongoing enhanced monitoring with quarterly re-screening"]

---

## Detailed Checklist

### Identity Verification

| # | Item | Required | Collected | Acceptable | Notes |
|---|------|----------|-----------|------------|-------|
| I1 | Government-Issued Photo ID | [Yes/No] | [Yes/No] | [Yes/No/N/A] | [notes] |
| I2 | Proof of Address | [Yes/No] | [Yes/No] | [Yes/No/N/A] | [notes] |
[... continue for all items ...]

### Entity Documentation

[Same format for entity items]

### Sanctions and PEP Screening

[Same format for screening items]

### Source of Funds / Wealth

[Same format for source of funds items]

---

## Sanctions Screening Results

| Database | Screened | Result | Date | Notes |
|----------|---------|--------|------|-------|
| OFAC SDN | [Yes/No/Unable] | [Clear/Match/Near-Match] | [date] | [notes] |
| OFAC Consolidated | [Yes/No/Unable] | [Clear/Match/Near-Match] | [date] | [notes] |
| UN Consolidated | [Yes/No/Unable] | [Clear/Match/Near-Match] | [date] | [notes] |
| EU Sanctions | [Yes/No/Unable] | [Clear/Match/Near-Match] | [date] | [notes] |
| PEP Database | [Yes/No/Unable] | [Clear/Match] | [date] | [notes] |
| Adverse Media | [Yes/No/Unable] | [Clear/Findings] | [date] | [notes] |

**NOTE:** This review indicates whether screening has been documented as completed. Actual real-time sanctions screening must be performed using authorized screening systems against current databases. AI-generated analysis cannot substitute for automated sanctions screening.

---

## Recommended Next Steps

1. [ ] Collect all CRITICAL missing items before proceeding with investor onboarding
2. [ ] Complete sanctions screening through authorized screening system if not yet performed
3. [ ] Obtain compliance officer sign-off for [Standard / Enhanced] due diligence level
4. [ ] [If Enhanced:] Schedule senior management review and approval
5. [ ] Set reminder for periodic KYC refresh ([12 months for high risk / 24 months for medium / 36 months for low])
6. [ ] File completed KYC package in investor records with retention for minimum 5 years post-relationship
7. [ ] [If issues found:] Consult legal counsel regarding [specific issue]
```

---

## Phase 5: Present to User

After generating the report:

1. Display the **KYC Completeness Score** prominently
2. Display the **Risk Classification** with one-line justification
3. List **Missing Items** grouped by priority (CRITICAL, HIGH, MEDIUM)
4. Show the **Sanctions Screening Summary** status
5. Show the full report
6. Ask: "Would you like me to run a compliance check on the full fund documentation? Run `/fund check-compliance <file>`."
7. Mention: "Run `/fund report-pdf` to generate a professional PDF version of this KYC review."
