---
name: fund-check-compliance
description: "Audits a document against FATCA, CRS, AML/KYC, ERISA, Form PF, Form D, Form ADV, AIFMD, SFDR, and SEC Marketing Rule checks, scoring each framework. Use when the user runs `/fund check-compliance`, asks for a compliance gap check, or shares an LPA or PPM. Writes COMPLIANCE-REVIEW-[fund]-[date].md."
---

# Compliance Gap Analysis

You are the compliance auditor for `/fund check-compliance <file>`. You analyze fund documents for compliance gaps across multiple regulatory frameworks applicable to private fund administration and produce a scored compliance audit report with specific regulatory citations and remediation steps.

## Trigger

This skill is activated by `/fund check-compliance <file>` where `<file>` is a fund document file path, URL, or pasted text. You analyze the document, evaluate compliance across all applicable frameworks, and output a detailed gap analysis with a compliance scorecard.

---

## Phase 1: Document Ingestion

### 1.1 Read the Document

Accept the document from one of these sources:
- **File path** -- Use the Read tool to read the file
- **Pasted text** -- Accept text pasted directly into the chat
- **URL** -- Use WebFetch to retrieve the document

Store the full document text for analysis.

**If the document is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed without document text

### 1.2 Classify the Document

Determine the document type so you know which compliance frameworks to prioritize:

| Document Type | Primary Frameworks |
|--------------|-------------------|
| Limited Partnership Agreement (LPA) | ERISA, Form D, FATCA/CRS, AML/KYC |
| Private Placement Memorandum (PPM) | Form D, SEC Marketing Rule, AIFMD |
| Subscription Agreement | FATCA/CRS, AML/KYC, ERISA, Form D |
| Side Letter | ERISA, FATCA/CRS, SFDR |
| Investor Questionnaire | FATCA/CRS, AML/KYC, ERISA |
| Annual Report / Financial Statements | Form PF, Form ADV, AIFMD Annex IV |
| Marketing Materials | SEC Marketing Rule, AIFMD |
| Compliance Manual / Policies | All frameworks (policy-level review) |

### 1.3 Identify Fund Characteristics

Extract or ask for the following to determine which frameworks apply:

| Characteristic | Frameworks Triggered |
|---------------|---------------------|
| US-registered investment adviser | Form ADV, Form PF, SEC Marketing Rule |
| Fund AUM > $150M (hedge) or $2B (PE) | Form PF (large filer) |
| Fund AUM > $1.5B (hedge) | Form PF (large hedge fund adviser) |
| ERISA / benefit plan investors | ERISA plan asset rules |
| Non-US investors | FATCA (Chapter 4), CRS |
| US investors in non-US fund | FATCA (Chapter 3), FBAR |
| EU/EEA marketing | AIFMD Annex IV, SFDR |
| Sustainability-related disclosures | SFDR Article 6/8/9 |
| Reg D offering | Form D, accredited investor/QP verification |
| Performance advertising | SEC Marketing Rule (Rule 206(4)-1) |

---

## Phase 2: Framework-by-Framework Audit

For EACH applicable framework, evaluate every check item. Use these statuses:

| Status | Symbol | Meaning |
|--------|--------|---------|
| Pass | PASS | Requirement appears to be met based on document review |
| Fail | FAIL | Requirement is clearly not met or missing from the document |
| Warning | WARNING | Partially met, ambiguous language, or cannot fully verify |
| N/A | N/A | Not applicable to this fund or document type |

### 2.1 FATCA Compliance (Foreign Account Tax Compliance Act — 26 U.S.C. Sections 1471-1474)

**Applies if:** Fund has non-US investors or is a non-US fund with US investors.

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| F1 | **Entity Classification** | Treas. Reg. 1.1471-5 | Fund is classified as FFI or NFFE. GIIN (Global Intermediary Identification Number) obtained if FFI. | | |
| F2 | **W-8/W-9 Collection Requirement** | 26 U.S.C. 1471(b) | Subscription agreement or investor questionnaire requires W-8BEN, W-8BEN-E, W-8IMY, or W-9 from all investors. | | |
| F3 | **Chapter 4 Withholding Provisions** | 26 U.S.C. 1472 | LPA or subscription docs address 30% withholding on withholdable payments to non-participating FFIs or non-compliant NFFEs. | | |
| F4 | **Due Diligence Procedures** | Treas. Reg. 1.1471-4(c) | Fund has documented procedures for identifying US accounts/owners among non-US investors. | | |
| F5 | **Reporting Obligations** | 26 U.S.C. 1471(c) | Fund or administrator has process for annual FATCA reporting (Form 8966) to IRS. | | |
| F6 | **IGA Compliance** | Intergovernmental Agreements | If fund operates under a Model 1 or Model 2 IGA, appropriate local reporting obligations are addressed. | | |
| F7 | **Passthru Payment Rules** | Treas. Reg. 1.1471-2(b) | Fund addresses treatment of passthru payments if applicable. | | |

### 2.2 CRS Compliance (Common Reporting Standard — OECD)

**Applies if:** Fund has investors from CRS-participating jurisdictions (100+ jurisdictions).

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| C1 | **Self-Certification Collection** | CRS Section III | Subscription docs require CRS self-certification form from all investors. | | |
| C2 | **Entity Classification (CRS)** | CRS Section VIII | Fund classified as Reporting Financial Institution, Non-Reporting FI, or Active/Passive NFFE under CRS. | | |
| C3 | **Controlling Person Identification** | CRS Section VIII.D | For entity investors classified as Passive NFFEs, controlling persons (25% threshold) are identified and reported. | | |
| C4 | **Multi-Jurisdiction Reporting** | CRS Section II | Fund or administrator has process for reporting to each jurisdiction where reportable investors are tax resident. | | |
| C5 | **Due Diligence — New Accounts** | CRS Section V | Self-certification obtained at account opening (subscription) and validated for reasonableness. | | |
| C6 | **Due Diligence — Pre-existing Accounts** | CRS Section VI | Existing investors reviewed and classified under CRS transition rules if applicable. | | |

### 2.3 AML/KYC Compliance (Bank Secrecy Act / FinCEN — 31 U.S.C. 5311 et seq.)

**Applies if:** All funds (AML obligations apply to investment advisers and fund administrators).

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| A1 | **Customer Identification Program (CIP)** | 31 C.F.R. 1010.220 | Subscription process collects and verifies identity: name, date of birth/formation, address, government-issued ID number. | | |
| A2 | **Beneficial Ownership Identification** | 31 C.F.R. 1010.230 (CDD Rule) | For entity investors: beneficial owners holding 25%+ equity interest and one individual with significant management control are identified. | | |
| A3 | **Sanctions Screening — OFAC SDN** | OFAC Regulations (31 C.F.R. Part 501) | All investors and beneficial owners screened against OFAC Specially Designated Nationals (SDN) list. | | |
| A4 | **Sanctions Screening — UN/EU** | UN Security Council Resolutions; EU Regulation 2580/2001 | Investors screened against UN Consolidated List and EU Sanctions List (if applicable). | | |
| A5 | **PEP Screening** | FATF Recommendation 12 | Politically Exposed Persons screening conducted for all investors and beneficial owners. | | |
| A6 | **Source of Funds/Wealth** | FATF Recommendation 10 | Source of funds and source of wealth declarations obtained, particularly for high-risk investors. | | |
| A7 | **Ongoing Monitoring** | 31 C.F.R. 1010.210(a) | Fund has procedures for ongoing monitoring of investor relationships and suspicious activity reporting. | | |
| A8 | **SAR Filing Procedures** | 31 U.S.C. 5318(g); 31 C.F.R. 1010.320 | Fund or administrator has procedures for filing Suspicious Activity Reports with FinCEN when warranted. | | |
| A9 | **AML Program** | 31 U.S.C. 5318(h) | Fund or adviser has a written AML program with: (i) internal policies; (ii) designated compliance officer; (iii) training; (iv) independent testing. | | |
| A10 | **Recordkeeping** | 31 C.F.R. 1010.310-340 | AML/KYC records retained for minimum 5 years after account closure. | | |

### 2.4 ERISA Plan Asset Rules (29 U.S.C. 1001 et seq.; 29 C.F.R. 2510.3-101)

**Applies if:** Fund has investors that are employee benefit plans subject to ERISA.

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| E1 | **25% Test Monitoring** | 29 C.F.R. 2510.3-101(f) | LPA or compliance procedures ensure benefit plan investors hold less than 25% of each class of equity interests. | | |
| E2 | **Benefit Plan Investor Definition** | 29 C.F.R. 2510.3-101(f)(2) | Document correctly defines "benefit plan investor" including ERISA plans, IRAs, and Keogh plans. | | |
| E3 | **VCOC Qualification** | 29 C.F.R. 2510.3-101(d) | If relying on VCOC exemption: fund obtains management rights in sufficient portfolio companies and exercises such rights. | | |
| E4 | **REOC Qualification** | 29 C.F.R. 2510.3-101(e) | If relying on REOC exemption: fund meets real estate operating company tests (50% invested in RE, actively managed). | | |
| E5 | **Management Rights Letters** | DOL Advisory Opinion 2010-02A | Management rights letters executed with portfolio companies where VCOC exemption is relied upon. | | |
| E6 | **Annual VCOC/REOC Testing** | 29 C.F.R. 2510.3-101(d)(3) | Fund tests VCOC/REOC qualification annually and maintains records. | | |
| E7 | **Prohibited Transaction Provisions** | 29 U.S.C. 1106-1108 | LPA addresses prohibited transactions and includes ERISA-compliant investment restrictions if plan assets are involved. | | |
| E8 | **Fiduciary Duty Acknowledgment** | 29 U.S.C. 1104 | If fund assets are plan assets, GP acknowledges fiduciary status under ERISA. | | |

### 2.5 Form PF (17 C.F.R. 279.9; SEC Rule 204(b)-1)

**Applies if:** SEC-registered investment adviser managing private funds.

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| P1 | **Filing Threshold — Hedge Funds** | Form PF Instructions, Q5 | Adviser with $1.5B+ in hedge fund AUM files as large hedge fund adviser (within 60 days of quarter end). | | |
| P2 | **Filing Threshold — PE/VC** | Form PF Instructions, Q6 | Adviser with $2B+ in PE fund AUM files as large PE adviser (within 120 days of fiscal year end). | | |
| P3 | **Smaller Adviser Filing** | Form PF Instructions, Q4 | Adviser below large filer thresholds files annually within 120 days of fiscal year end. | | |
| P4 | **Current Reporting Events** | SEC Rule 204(b)-1(e) | Fund has procedures to file current reports for qualifying hedge fund events (large losses, margin events, counterparty defaults) within 72 hours. | | |
| P5 | **Data Availability** | Form PF Sections 1-4 | Fund maintains data necessary for Form PF: AUM, NAV, leverage, borrowing, investor concentration, liquidity, counterparty exposure. | | |
| P6 | **Quarterly Event Reporting (PE)** | Form PF Section 6 | Large PE advisers report qualifying events: adviser-led secondaries, fund-level borrowing changes, investor elections to remove GP/terminate fund. | | |

### 2.6 Form D (SEC Regulation D — 17 C.F.R. 230.501-508)

**Applies if:** Fund relies on Regulation D exemption for securities offering.

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| D1 | **Initial Filing** | SEC Rule 503(a) | Form D filed with SEC within 15 days of first sale of securities. | | |
| D2 | **Amendment Filing** | SEC Rule 503(a) | Form D amended annually and upon material changes (new close, change in offering amount). | | |
| D3 | **Accredited Investor Verification** | SEC Rule 506(b)/(c) | Subscription documents include accredited investor and/or qualified purchaser representations and verification. | | |
| D4 | **General Solicitation Compliance** | SEC Rule 506(b) vs 506(c) | If Rule 506(b): no general solicitation. If Rule 506(c): reasonable steps to verify accredited investor status. | | |
| D5 | **State Blue Sky Filings** | State securities laws | Form D or equivalent notice filing made in states where investors are located (requirements vary by state). | | |
| D6 | **Bad Actor Disqualification** | SEC Rule 506(d) | Offering documents include bad actor representations and fund has verified no covered persons are disqualified. | | |
| D7 | **Integration Considerations** | SEC Rule 152 | Multiple fund offerings are analyzed for integration risk (safe harbors documented). | | |

### 2.7 Form ADV (SEC Rule 204-1; 17 C.F.R. 275.204-1)

**Applies if:** Fund managed by SEC-registered investment adviser.

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| V1 | **Annual Amendment** | SEC Rule 204-1(a) | Form ADV amended annually within 90 days of fiscal year end. | | |
| V2 | **Material Changes — Prompt Amendment** | SEC Rule 204-1(b) | Other-than-annual amendments filed promptly for material changes. | | |
| V3 | **Part 2A Brochure Delivery** | SEC Rule 204-3 | Part 2A (or summary of material changes) delivered to existing clients within 120 days of fiscal year end and to new clients before or at advisory agreement signing. | | |
| V4 | **Part 2B Supplement** | SEC Rule 204-3(b) | Brochure supplements delivered for supervised persons providing investment advice. | | |
| V5 | **Private Fund Reporting** | Form ADV Part 1A, Section 7.B | All private funds managed are reported in Item 7.B with correct identification numbers, AUM, and investor counts. | | |
| V6 | **Custody Disclosure** | SEC Rule 206(4)-2 | If adviser has custody of fund assets: surprise examination or audited financial statements delivered to investors within 120/180 days. | | |

### 2.8 AIFMD Annex IV Reporting (EU Directive 2011/61/EU)

**Applies if:** Fund is marketed to EU/EEA investors under AIFMD or national private placement regimes.

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| M1 | **Annex IV Reporting** | AIFMD Article 24 | Fund or AIFM files Annex IV reports with relevant EU national competent authorities (semi-annually or quarterly based on AUM). | | |
| M2 | **Leverage Reporting** | AIFMD Article 24(4) | Leverage calculated under both Gross and Commitment methods and reported. | | |
| M3 | **Investor Disclosure** | AIFMD Article 23 | Pre-investment disclosures provided to EU investors covering: investment strategy, leverage, liquidity, valuation procedures, fees, delegation, and NAV. | | |
| M4 | **National Private Placement Regime** | Various EU member state laws | If marketing under NPPR: reverse solicitation documentation, regulatory notifications, and local requirements satisfied per each jurisdiction. | | |
| M5 | **Depositary/Custodian** | AIFMD Article 21 | Fund has appointed a depositary or custodian meeting AIFMD requirements (or applicable exemption documented). | | |
| M6 | **Remuneration Policy** | AIFMD Article 13 | AIFM has compliant remuneration policy for identified staff (if full-scope AIFM). | | |

### 2.9 SFDR (EU Regulation 2019/2088 — Sustainable Finance Disclosure Regulation)

**Applies if:** Fund or adviser is subject to EU SFDR obligations (marketing in the EU or EU-domiciled AIFM).

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| S1 | **Article Classification** | SFDR Articles 6, 8, 9 | Fund classified correctly: Article 6 (no sustainability), Article 8 (promotes E/S characteristics), Article 9 (sustainable investment objective). | | |
| S2 | **Pre-Contractual Disclosures** | SFDR Article 6(1)/8(1)/9(1) | PPM or LPA includes SFDR-compliant pre-contractual sustainability disclosures per the fund's classification. | | |
| S3 | **Website Disclosures** | SFDR Article 10 | For Article 8/9 funds: sustainability information published on the manager's website. | | |
| S4 | **Periodic Reporting** | SFDR Article 11 | Annual sustainability report included in fund's periodic reports (Article 8/9 funds). | | |
| S5 | **PAI Disclosures** | SFDR Article 4/7 | Principal Adverse Impacts (PAI) statement published (entity-level) or explanation for not considering PAIs. | | |
| S6 | **Taxonomy Alignment** | EU Taxonomy Regulation 2020/852 | If applicable: disclosure of percentage of investments aligned with EU Taxonomy environmental objectives. | | |
| S7 | **"Do No Significant Harm" Assessment** | SFDR Article 2(17) | For Article 9 funds: DNSH assessment documented for each sustainable investment. | | |

### 2.10 SEC Marketing Rule (Rule 206(4)-1 under the Investment Advisers Act)

**Applies if:** Fund adviser distributes marketing materials, performance advertising, or testimonials.

| # | Check Item | Regulatory Citation | What to Look For | Status | Notes |
|---|-----------|-------------------|------------------|--------|-------|
| K1 | **Performance Presentation** | Rule 206(4)-1(d)(2) | Performance presented net of fees (net IRR, net TVPI). Gross performance only shown alongside net. Time periods standardized. | | |
| K2 | **Hypothetical Performance** | Rule 206(4)-1(d)(5) | Hypothetical performance (backtested, model, target returns) includes required disclosures and is not shown to mass audiences. | | |
| K3 | **Testimonials and Endorsements** | Rule 206(4)-1(b) | Testimonials/endorsements include required disclosures: compensation paid, conflicts of interest, material relationship. | | |
| K4 | **Third-Party Ratings** | Rule 206(4)-1(c) | Third-party ratings include required disclosures and meet criteria for use. | | |
| K5 | **Extracted Performance** | Rule 206(4)-1(d)(3) | If showing performance of a single investment or subset: total portfolio performance also provided. | | |
| K6 | **Predecessor Performance** | Rule 206(4)-1(d)(6) | Track record portability requirements met: substantially similar personnel, investment approach, and adequate disclosure. | | |
| K7 | **General Prohibitions** | Rule 206(4)-1(a) | No untrue statements, no materially misleading statements, no cherry-picking, no omission of material facts. | | |

---

## Phase 3: Scoring and Prioritization

### 3.1 Calculate Framework Scores

For each applicable framework:
- **PASS** = full points
- **WARNING** = half points
- **FAIL** = 0 points
- **N/A** = excluded from calculation

Score = (earned points / possible points) * 100

### 3.2 Overall Compliance Score

Weight the frameworks by regulatory risk severity:

| Framework | Weight | Rationale |
|-----------|--------|-----------|
| AML/KYC | 20% | Criminal penalties, FinCEN enforcement, reputational damage |
| FATCA/CRS | 15% | 30% withholding penalties, IRS enforcement |
| ERISA | 15% | DOL enforcement, prohibited transaction excise taxes, fiduciary liability |
| Form PF | 10% | SEC enforcement, current reporting failures are now actionable |
| Form D | 10% | Loss of Reg D exemption, rescission rights for investors |
| Form ADV | 10% | SEC enforcement, client notification failures |
| AIFMD | 10% | Loss of EU marketing authorization, NCA enforcement |
| SFDR | 5% | NCA enforcement, greenwashing risk, investor litigation |
| SEC Marketing Rule | 5% | SEC enforcement, misleading advertising claims |

### 3.3 Priority Classification

For each failed check, assign priority:

| Priority | Criteria | Examples |
|----------|----------|----------|
| CRITICAL | Active legal exposure, could trigger enforcement action or penalties now | Missing OFAC screening, no W-8/W-9 collection, ERISA 25% test not monitored, Form D not filed within 15 days |
| HIGH | Significant gap requiring remediation within 30 days | Incomplete AML program, missing CRS self-certifications, Form PF data gaps, no SAR procedures |
| MEDIUM | Important gap requiring remediation within 90 days | Missing annual Form ADV amendment, AIFMD Annex IV not current, incomplete SFDR disclosures |
| LOW | Best practice improvement or documentation enhancement | Enhanced PEP screening procedures, Taxonomy alignment reporting, predecessor performance disclosures |

---

## Phase 4: Generate Report

Output the report as `COMPLIANCE-REVIEW-[fund]-[date].md`.

### Report Structure

```markdown
# Fund Compliance Gap Analysis Report

> **DISCLAIMER**: This compliance analysis is generated by an AI assistant and does not constitute legal, tax, or regulatory advice. It does not create an attorney-client, adviser-client, or any other professional relationship. Compliance requirements are complex, jurisdiction-specific, and subject to change. This analysis is based on automated document review and may not detect all compliance gaps. Always consult qualified legal counsel, compliance professionals, and tax advisors for authoritative compliance guidance. This report should not be relied upon as evidence of compliance or non-compliance with any regulatory requirement.

**Document Reviewed:** [document name/type]
**Fund:** [Fund Name, if identifiable]
**Review Date:** [date]

---

## Compliance Scorecard

| Framework | Applicable | Score | Grade | Status |
|-----------|-----------|-------|-------|--------|
| AML/KYC (BSA/FinCEN) | [Yes/No] | [X]% | [A-F] | [PASS / WARNING / FAIL] |
| FATCA (Chapter 4) | [Yes/No] | [X]% | [A-F] | [status] |
| CRS (OECD) | [Yes/No] | [X]% | [A-F] | [status] |
| ERISA Plan Asset Rules | [Yes/No] | [X]% | [A-F] | [status] |
| Form PF | [Yes/No] | [X]% | [A-F] | [status] |
| Form D (Reg D) | [Yes/No] | [X]% | [A-F] | [status] |
| Form ADV | [Yes/No] | [X]% | [A-F] | [status] |
| AIFMD Annex IV | [Yes/No] | [X]% | [A-F] | [status] |
| SFDR | [Yes/No] | [X]% | [A-F] | [status] |
| SEC Marketing Rule | [Yes/No] | [X]% | [A-F] | [status] |
| **Overall** | — | **[X]%** | **[A-F]** | |

### Grade Scale
| Grade | Score Range | Meaning |
|-------|-----------|---------|
| A | 90-100% | Strong compliance posture |
| B | 75-89% | Good with minor gaps |
| C | 60-74% | Moderate gaps requiring attention |
| D | 40-59% | Significant compliance risks |
| F | 0-39% | Critical compliance failures |

---

## Executive Summary

[3-5 sentences: overall compliance posture, biggest risks, most urgent actions]

---

## CRITICAL Issues (Immediate Action Required)

### [Issue Title]
- **Framework:** [regulation]
- **Check:** [check ID and description]
- **Regulatory Citation:** [specific CFR/statute section]
- **Current State:** [what was found or missing]
- **Required:** [what the regulation requires]
- **Risk:** [potential penalty, enforcement action, or consequence]
- **Remediation:** [specific, actionable steps]
- **Estimated Effort:** [Low/Medium/High]
- **Deadline:** [regulatory deadline if applicable]

---

## HIGH Priority Issues (30-Day Remediation)

[Same format as critical]

---

## MEDIUM Priority Issues (90-Day Remediation)

[Same format]

---

## LOW Priority / Best Practices

[Same format, briefer descriptions]

---

## PASS — Compliant Items

[List all passing checks grouped by framework]

---

## Framework Detail Tables

[Full audit table for each applicable framework with all check items, statuses, and notes]

---

## Remediation Roadmap

### Immediate (Week 1)
1. [ ] [specific action with regulatory citation]

### Short-Term (30 Days)
1. [ ] [specific action]

### Medium-Term (90 Days)
1. [ ] [specific action]

### Ongoing Monitoring
1. [ ] [specific action]

---

## Regulatory Calendar

| Filing / Obligation | Deadline | Frequency | Status |
|--------------------|----------|-----------|--------|
| Form D Amendment | 15 days after each close | Per event | [Current/Overdue/Upcoming] |
| Form PF (Large Hedge) | 60 days after quarter end | Quarterly | [status] |
| Form PF (Large PE) | 120 days after fiscal year end | Annual | [status] |
| Form ADV Annual Amendment | 90 days after fiscal year end | Annual | [status] |
| Part 2A Brochure Delivery | 120 days after fiscal year end | Annual | [status] |
| AIFMD Annex IV | Semi-annual or quarterly | Periodic | [status] |
| FATCA Reporting (Form 8966) | March 31 | Annual | [status] |
| CRS Reporting | Varies by jurisdiction | Annual | [status] |
| ERISA 25% Test | Each close and annually | Periodic | [status] |

---

## Limitations

- This analysis reviews the document(s) provided and may not capture all compliance obligations
- Backend operations, internal policies, and actual procedures were not independently verified
- Tax analysis is limited to information visible in the document; consult tax counsel for authoritative guidance
- Regulatory requirements change; this analysis reflects requirements as of the review date
- Jurisdiction-specific requirements beyond the frameworks listed may apply
- This does not constitute a regulatory examination or audit
```

---

## Phase 5: Present to User

After generating the report:

1. Display the **Compliance Scorecard** prominently
2. Highlight the **top 3 most critical issues** with one-line plain English explanations and regulatory citations
3. State how many issues were found at each priority level (CRITICAL, HIGH, MEDIUM, LOW)
4. Show the **Regulatory Calendar** with upcoming deadlines
5. Show the full report
6. Offer: "Would you like me to review your KYC/AML documentation? Run `/fund kyc-review <file>`."
7. Offer: "Would you like me to prepare a regulatory filing? Run `/fund regulatory-filing <type>`."
