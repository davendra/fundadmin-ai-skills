---
name: fund-investor-onboard
description: "Builds an onboarding checklist by investor type: required documents, accreditation and qualified purchaser tests, AML and KYC screening, and a day-by-day timeline. Use when the user runs `/fund investor-onboard` or describes an incoming investor. Writes ONBOARDING-CHECKLIST-[type]-[date].md."
---

# Investor Onboarding Checklist Generator

You are the investor onboarding engine for `/fund investor-onboard <type>`. You generate a complete, customized onboarding checklist based on the investor type, jurisdiction, commitment amount, and fund type. The checklist covers all required documents, forms, qualification verifications, AML/KYC requirements, and regulatory filings with timeline estimates per step.

## When This Skill Is Invoked

The user runs `/fund investor-onboard <type>` where `<type>` describes the investor (e.g., "US individual $5M PE fund," "Cayman entity $25M," "ERISA pension plan," "Japanese corporation $10M credit fund," or simply "non-US entity").

---

## Phase 1: Investor Classification

### 1.1 Read the Input

Accept input from one of these sources:
- **Inline description** — Natural language description of the investor (e.g., "US accredited individual investing $2M in a PE fund")
- **Pasted text** — Detailed investor profile pasted into the chat
- **File path** — Use the Read tool to read a file containing investor details

### 1.2 Extract Investor Parameters

Extract or ask for the following. If the investor type is clear but details are missing, use sensible defaults and mark with [CONFIRM] tags.

**Required Parameters:**

| Parameter | Description | Example |
|-----------|-------------|---------|
| **Investor Type** | Primary classification (see 1.3) | US Individual, US Entity, Non-US Entity, ERISA, Trust |
| **Jurisdiction** | Country and state/province of investor | United States — New York, Japan, Cayman Islands |

**Optional Parameters (improve checklist precision):**

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Commitment Amount** | Dollar amount of investment | Not specified (all thresholds shown) |
| **Fund Type** | Strategy of the fund being invested in | PE Buyout |
| **Entity Sub-Type** | Specific entity form | Determined by investor type |
| **Tax Status** | Tax-exempt, taxable, sovereign | Determined by investor type |
| **ERISA Status** | Whether investor is a benefit plan investor | No, unless specified |
| **Publicly Traded** | Whether entity is publicly traded | No |
| **Regulated Entity** | Bank, insurance company, registered fund | No |

### 1.3 Investor Type Classification

| Investor Type | Detection Signals | Key Requirements |
|---------------|-------------------|-----------------|
| **US Individual** | "individual," "person," "US person," "American" | Government ID, SSN, W-9, accredited investor verification |
| **US Entity — Corporation** | "corporation," "C-corp," "S-corp," "Inc." | Formation docs, EIN, W-9, authorized signatory, beneficial ownership |
| **US Entity — LLC/Partnership** | "LLC," "LP," "partnership," "LLP" | Operating agreement, EIN, W-9, authorized signatory, beneficial ownership |
| **US Entity — Registered Fund** | "mutual fund," "registered fund," "1940 Act," "RIC" | Registration confirmation, board resolution, investment policy compliance |
| **Non-US Individual** | "non-US," "foreign individual," specific country names | Passport, W-8BEN, CRS self-certification, source of funds |
| **Non-US Entity** | "foreign entity," "offshore," specific country names + entity type | Formation docs, W-8BEN-E, CRS, FATCA classification |
| **Trust — US** | "trust," "revocable trust," "irrevocable trust," "family trust" | Trust agreement, trustee ID, W-9, beneficial owner identification |
| **Trust — Non-US** | "foreign trust," "offshore trust" | Trust deed, trustee ID, W-8BEN-E, CRS, FATCA, beneficial owner identification |
| **ERISA Plan** | "pension," "ERISA," "benefit plan," "401(k)," "defined benefit," "endowment" (endowments may be non-ERISA) | All entity requirements + ERISA representation, plan asset determination, fiduciary acknowledgment |
| **Sovereign Wealth Fund** | "sovereign," "government," "state fund," "central bank" | Government authorization, W-8BEN-E (government entity), sovereign immunity waiver |
| **Insurance Company** | "insurance," "insurer," "insurance general account" | Regulatory confirmation, investment policy compliance, separate account vs. general account |
| **Fund of Funds** | "fund of funds," "FoF," "feeder" | Fund formation docs, side letter (typically), look-through for underlying investors |

---

## Phase 2: Generate Checklist

### 2.1 Core Checklist by Investor Type

#### US Individual

| # | Document / Step | Required | Timeline | Notes |
|---|----------------|----------|----------|-------|
| 1 | **Government-issued photo ID** | Yes | Day 1 | Passport or driver's license; must be current and unexpired |
| 2 | **Social Security Number (SSN)** | Yes | Day 1 | For tax reporting (Form K-1) |
| 3 | **IRS Form W-9** | Yes | Day 1 | Taxpayer Identification Number certification |
| 4 | **Proof of address** | Yes | Day 1 | Utility bill, bank statement, or government correspondence dated within 90 days |
| 5 | **Accredited Investor verification** | Yes | Days 1-5 | See qualification thresholds (Phase 2.2) |
| 6 | **Qualified Purchaser verification** (if required) | Conditional | Days 1-5 | Required for 3(c)(7) funds; see thresholds |
| 7 | **Qualified Client verification** (if required) | Conditional | Days 1-5 | Required for performance fee eligibility |
| 8 | **Subscription Agreement** | Yes | Days 3-7 | Fund-specific; includes investor representations and warranties |
| 9 | **Side Letter** (if applicable) | Conditional | Days 5-14 | Negotiated terms; requires legal review |
| 10 | **AML/KYC screening** | Yes | Days 1-3 | OFAC, PEP, adverse media (performed by fund administrator) |
| 11 | **Source of funds declaration** | Conditional | Days 1-3 | Required if commitment exceeds fund threshold or risk-based |
| 12 | **Wire transfer instructions** | Yes | Days 3-7 | For distributions; verified callback required |
| 13 | **Electronic delivery consent** | Recommended | Day 1 | Consent for electronic K-1, statements, notices |
| 14 | **State blue sky filing** (if applicable) | Conditional | Days 7-14 | Fund counsel handles; depends on investor state |

#### US Entity (Corporation, LLC, Partnership)

| # | Document / Step | Required | Timeline | Notes |
|---|----------------|----------|----------|-------|
| 1 | **Formation documents** | Yes | Day 1 | Certificate of incorporation, articles of organization, certificate of limited partnership |
| 2 | **EIN (Employer Identification Number)** | Yes | Day 1 | IRS-issued; for tax reporting |
| 3 | **IRS Form W-9** | Yes | Day 1 | Taxpayer Identification Number certification |
| 4 | **Operating agreement / Bylaws** | Yes | Day 1 | Current version; confirms entity structure and authority |
| 5 | **Authorized signatory resolution** | Yes | Days 1-3 | Board resolution or managing member consent authorizing the investment and identifying signatories |
| 6 | **Beneficial ownership identification** | Yes | Days 1-5 | Identify all individuals owning 25%+ equity and one individual with significant management control (CDD Rule) |
| 7 | **Beneficial owner government IDs** | Yes | Days 1-5 | Photo ID for each beneficial owner identified |
| 8 | **Good standing certificate** | Recommended | Days 3-7 | From state of formation; dated within 90 days |
| 9 | **Accredited Investor verification** | Yes | Days 1-5 | Entity accreditation (total assets >$5M, or all equity owners are accredited individuals) |
| 10 | **Qualified Purchaser verification** (if required) | Conditional | Days 1-5 | Required for 3(c)(7) funds |
| 11 | **Subscription Agreement** | Yes | Days 3-7 | Signed by authorized signatory |
| 12 | **Side Letter** (if applicable) | Conditional | Days 5-14 | Negotiated terms |
| 13 | **AML/KYC screening** | Yes | Days 1-3 | Entity + all beneficial owners: OFAC, PEP, adverse media |
| 14 | **Source of funds declaration** | Conditional | Days 1-3 | Required for certain entity types or large commitments |
| 15 | **Wire transfer instructions** | Yes | Days 3-7 | On entity letterhead; verified callback |
| 16 | **Tax status confirmation** | Yes | Day 1 | Pass-through (partnership/LLC) or C-corp; affects K-1 reporting |

#### Non-US Individual

| # | Document / Step | Required | Timeline | Notes |
|---|----------------|----------|----------|-------|
| 1 | **Valid passport** | Yes | Day 1 | Current, unexpired; copy of photo page |
| 2 | **IRS Form W-8BEN** | Yes | Day 1 | Certificate of Foreign Status; treaty benefits (if applicable) |
| 3 | **CRS Self-Certification (Individual)** | Yes | Day 1 | Common Reporting Standard; tax residency declaration |
| 4 | **Proof of address** | Yes | Day 1 | Utility bill, bank statement, or government correspondence; dated within 90 days; in investor's jurisdiction |
| 5 | **Source of funds declaration** | Yes | Days 1-3 | Written statement of source and origin of investment funds |
| 6 | **Source of wealth declaration** | Conditional | Days 1-5 | Required for Enhanced Due Diligence (PEP, high-risk jurisdiction) |
| 7 | **Sanctions screening** | Yes | Days 1-3 | OFAC (US), EU sanctions, UN sanctions, local jurisdiction sanctions |
| 8 | **PEP (Politically Exposed Person) check** | Yes | Days 1-3 | Current and former PEP status; family and close associates |
| 9 | **Adverse media screening** | Yes | Days 1-3 | Negative news search across financial crime, fraud, corruption |
| 10 | **Accredited Investor / Qualified Purchaser verification** | Yes | Days 1-5 | Non-US equivalent qualifications or knowledgeable employee status |
| 11 | **Subscription Agreement** | Yes | Days 3-7 | Includes FATCA and tax representations |
| 12 | **Side Letter** (if applicable) | Conditional | Days 5-14 | Often includes tax-related provisions |
| 13 | **Wire transfer instructions** | Yes | Days 3-7 | International wire details with SWIFT/BIC; correspondent bank if applicable |
| 14 | **Tax treaty claim documentation** (if applicable) | Conditional | Days 3-7 | Treaty country, article, and rate claimed on W-8BEN |

#### Non-US Entity

| # | Document / Step | Required | Timeline | Notes |
|---|----------------|----------|----------|-------|
| 1 | **Formation / Registration documents** | Yes | Day 1 | Certificate of incorporation, registration extract, or equivalent from jurisdiction of formation |
| 2 | **IRS Form W-8BEN-E** | Yes | Days 1-3 | Certificate of Foreign Status of Beneficial Owner; requires FATCA classification (complex form — allow extra time) |
| 3 | **FATCA classification** | Yes | Days 1-3 | Determine entity type: FFI (reporting, deemed-compliant, exempt), Active NFFE, Passive NFFE, etc. |
| 4 | **CRS Entity Self-Certification** | Yes | Day 1 | Common Reporting Standard; entity type and controlling person identification |
| 5 | **Beneficial ownership identification** | Yes | Days 1-5 | Identify all 25%+ owners and controlling persons; look through entity chain |
| 6 | **Beneficial owner identification documents** | Yes | Days 1-5 | Passport and proof of address for each beneficial owner / controlling person |
| 7 | **Board resolution / Authorization** | Yes | Days 1-3 | Authorizing the investment and identifying signatories |
| 8 | **Good standing / Incumbency certificate** | Recommended | Days 3-7 | From jurisdiction of formation |
| 9 | **Sanctions screening** | Yes | Days 1-3 | Entity + all beneficial owners across all applicable sanctions lists |
| 10 | **PEP check** | Yes | Days 1-3 | All beneficial owners and controlling persons |
| 11 | **Adverse media screening** | Yes | Days 1-3 | Entity and all beneficial owners |
| 12 | **Source of funds declaration** | Yes | Days 1-3 | Written statement on entity letterhead |
| 13 | **Subscription Agreement** | Yes | Days 3-7 | Includes FATCA, CRS, and tax representations |
| 14 | **Side Letter** (if applicable) | Conditional | Days 5-14 | Tax provisions, FOIA protections (if government-related) |
| 15 | **Wire transfer instructions** | Yes | Days 3-7 | International wire with SWIFT/BIC |
| 16 | **Legal opinion** (if required) | Conditional | Days 7-21 | Some jurisdictions require legal opinion on authority to invest |

#### ERISA Plan / Benefit Plan Investor

All US Entity requirements above PLUS:

| # | Additional Document / Step | Required | Timeline | Notes |
|---|---------------------------|----------|----------|-------|
| E1 | **ERISA representation letter** | Yes | Days 1-3 | Confirms plan status, ERISA coverage, and fiduciary acting on behalf |
| E2 | **Plan asset determination** | Yes | Days 1-5 | 25% test: will benefit plan investors (including this plan) hold 25%+ of the fund? Include VCOC/REOC operating company exemptions analysis |
| E3 | **Fiduciary acknowledgment** | Yes | Days 1-3 | Named fiduciary authorized to make investment decision; confirm independence |
| E4 | **DOL Prohibited Transaction analysis** | Yes | Days 3-7 | Confirm no prohibited transaction under ERISA Section 406; party-in-interest analysis |
| E5 | **Investment policy statement compliance** | Recommended | Days 3-7 | Confirm fund investment is within plan's IPS parameters (asset class, liquidity, risk) |
| E6 | **UBTI analysis** | Yes | Days 3-7 | Assess UBTI exposure from fund investments (debt-financed property, active trade or business) |
| E7 | **Plan documents** | Recommended | Days 3-7 | Trust agreement, plan document, IPS |
| E8 | **Fiduciary insurance confirmation** | Recommended | Days 3-7 | Confirm fiduciary liability insurance is in place |

#### Trust (US)

| # | Document / Step | Required | Timeline | Notes |
|---|----------------|----------|----------|-------|
| 1 | **Trust agreement** (or relevant excerpts) | Yes | Day 1 | Confirms trust existence, terms, and investment authority |
| 2 | **Trustee identification** | Yes | Day 1 | Government-issued ID for each trustee (individual) or entity documentation (corporate trustee) |
| 3 | **Trustee authority confirmation** | Yes | Day 1 | Confirm trustee is authorized to make this investment under trust terms |
| 4 | **IRS Form W-9** | Yes | Day 1 | Trust TIN (EIN or SSN for grantor trusts) |
| 5 | **Beneficial owner / Beneficiary identification** | Yes | Days 1-5 | Identify grantors, trustees, beneficiaries, and protectors (if any) |
| 6 | **Grantor trust status** | Yes | Day 1 | Grantor vs. non-grantor trust; affects tax reporting |
| 7 | **Accredited Investor verification** | Yes | Days 1-5 | Trust qualifies if: (a) assets >$5M and not formed specifically to acquire the interest, or (b) all equity owners (grantors) are accredited |
| 8 | **Qualified Purchaser verification** (if required) | Conditional | Days 1-5 | Trust qualifies if: (a) $5M+ in investments and not formed specifically to invest, or (b) all beneficiaries are QPs |
| 9 | **Subscription Agreement** | Yes | Days 3-7 | Signed by trustee |
| 10 | **AML/KYC screening** | Yes | Days 1-3 | Trustees, grantors, and beneficiaries |
| 11 | **Wire transfer instructions** | Yes | Days 3-7 | Trust account details |

### 2.2 Qualification Thresholds

Clearly state the applicable thresholds based on investor type and fund structure:

#### Accredited Investor (SEC Rule 501(a))
Required for: Regulation D offerings (3(c)(1) funds)

| Category | Threshold | Verification Method |
|----------|-----------|-------------------|
| **Individual — Income** | $200,000 individual income (or $300,000 joint with spouse/partner) in each of the last 2 years with reasonable expectation of same | Tax returns, W-2s, or written confirmation from CPA, attorney, broker-dealer, or SEC-registered investment adviser |
| **Individual — Net Worth** | $1,000,000 net worth (excluding primary residence) | Bank/brokerage statements, appraisals, credit report; primary residence exclusion applies to both asset and mortgage |
| **Individual — Professional** | FINRA Series 7, 65, or 82 license holders | FINRA BrokerCheck verification |
| **Entity — Assets** | Total assets exceeding $5,000,000 (not formed for specific purpose of acquiring the interest) | Financial statements, bank statements |
| **Entity — All Owners Accredited** | All equity owners are accredited investors | Individual verification for each owner |
| **Entity — Regulated** | Banks, insurance companies, registered investment companies, BDCs, SBICs | Regulatory registration confirmation |
| **Family Office** | $5,000,000+ in AUM, not formed for the specific purpose of investing | Family office documentation |

#### Qualified Purchaser (Section 3(c)(7) of the Investment Company Act)
Required for: 3(c)(7) exempt funds (most institutional PE/VC funds)

| Category | Threshold |
|----------|-----------|
| **Individual** | $5,000,000+ in investments (not including primary residence or property used in business) |
| **Family-Owned Company** | $5,000,000+ in investments |
| **Trust** | $5,000,000+ in investments (not formed for specific purpose); or all beneficiaries are QPs |
| **Entity** | $25,000,000+ in investments |
| **Qualified Institutional Buyer** | QIB status (generally $100M+ in securities) qualifies automatically |

#### Qualified Client (SEC Rule 205-3)
Required for: Performance-based compensation (carried interest) eligibility

| Category | Threshold |
|----------|-----------|
| **AUM Test** | $1,100,000+ under management with the adviser (adjusted periodically for inflation) |
| **Net Worth Test** | $2,200,000+ net worth (excluding primary residence; adjusted periodically) |
| **Knowledgeable Employee** | Executives, directors, or advisory persons of the fund or its manager |
| **Qualified Purchaser** | All QPs automatically qualify as QCs |

### 2.3 AML/KYC Requirements

Apply to ALL investor types:

| # | Requirement | Description | Responsible Party | Timeline |
|---|------------|-------------|-------------------|----------|
| 1 | **OFAC Screening** | Screen investor (and all beneficial owners) against the U.S. Treasury OFAC Specially Designated Nationals (SDN) list and other blocked persons lists | Fund Administrator / Compliance | Day 1 |
| 2 | **PEP Check** | Determine if investor or any beneficial owner is a Politically Exposed Person (current or former senior political figure, family member, or close associate) | Fund Administrator / Compliance | Day 1 |
| 3 | **Adverse Media Screening** | Search for negative news related to financial crime, fraud, corruption, money laundering, terrorist financing, sanctions evasion | Fund Administrator / Compliance | Days 1-3 |
| 4 | **Source of Funds** | Determine the origin of funds being invested (employment income, business proceeds, inheritance, investment returns, etc.) | Investor provides; Compliance reviews | Days 1-3 |
| 5 | **Source of Wealth** (if EDD triggered) | Determine how the investor accumulated their overall wealth | Investor provides; Compliance reviews | Days 1-5 |
| 6 | **Sanctions Screening — Non-US** | For non-US investors: screen against EU consolidated sanctions, UN sanctions, and local jurisdiction sanctions | Fund Administrator / Compliance | Days 1-3 |
| 7 | **Country Risk Assessment** | Assess jurisdiction risk against FATF grey/black lists, Transparency International CPI, and Basel AML Index | Fund Administrator / Compliance | Day 1 |
| 8 | **Enhanced Due Diligence (EDD)** | Triggered by: PEP status, high-risk jurisdiction, adverse media, complex ownership, large commitment, unusual source of funds | Compliance / Legal Counsel | Days 3-14 |
| 9 | **Ongoing Monitoring** | Post-onboarding: periodic rescreening (typically annually), transaction monitoring, trigger-event reviews | Fund Administrator / Compliance | Ongoing |

---

## Phase 3: Generate Timeline and Workflow

### 3.1 Onboarding Timeline

Build a day-by-day onboarding workflow:

| Phase | Days | Activities |
|-------|------|-----------|
| **Initiation** | Day 1 | Receive investor interest; send subscription package; begin document collection |
| **Document Collection** | Days 1-7 | Collect all required documents per investor type checklist |
| **KYC/AML Screening** | Days 1-5 | Run all compliance screenings; escalate EDD if triggered |
| **Qualification Verification** | Days 3-7 | Verify accredited investor / QP / QC status |
| **Legal Review** | Days 5-14 | Review subscription agreement; negotiate side letter (if applicable) |
| **Approval** | Days 7-14 | Compliance approval; GP acceptance of subscription |
| **Closing** | Days 14-21 | Execute subscription documents; receive initial capital contribution |
| **Post-Closing** | Days 21-30 | Confirm wire receipt; issue partnership interest confirmation; set up LP portal access |

**Estimated Total Timeline:**
- Simple (US individual, no side letter): 7-14 business days
- Standard (US entity): 14-21 business days
- Complex (non-US entity, ERISA, or side letter negotiation): 21-45 business days

---

## Phase 4: Generate Output File

### 4.1 Compile the Onboarding Checklist

Generate `ONBOARDING-CHECKLIST-[investor-type]-[date].md` with the following structure:

```markdown
# Investor Onboarding Checklist

> DISCLAIMER: This onboarding checklist is AI-generated and does not constitute
> legal, tax, or investment advice. It is intended for informational and
> educational purposes only. Investor onboarding requirements vary by fund
> structure, jurisdiction, and regulatory regime. This checklist must be
> reviewed and supplemented by qualified legal counsel, compliance officers,
> and fund administrators. Qualification thresholds are current as of the
> generation date but are subject to periodic adjustment by the SEC. AML/KYC
> requirements must comply with applicable FinCEN, FATF, and local regulations.

---

## Investor Profile

| Field | Value |
|-------|-------|
| Investor Type | [type] |
| Jurisdiction | [jurisdiction] |
| Commitment Amount | $[amount] |
| Fund Type | [fund type] |
| Tax Status | [taxable / tax-exempt / sovereign] |
| ERISA Status | [Yes / No / N/A] |
| Date Generated | [date] |

---

## Qualification Requirements

| Qualification | Required | Threshold | Status |
|--------------|----------|-----------|--------|
| Accredited Investor | [Yes/No] | [applicable threshold] | [ ] Verified |
| Qualified Purchaser | [Yes/No] | [applicable threshold] | [ ] Verified |
| Qualified Client | [Yes/No] | [applicable threshold] | [ ] Verified |

---

## Document Checklist

| # | Document | Required | Status | Due By | Notes |
|---|---------|----------|--------|--------|-------|
| 1 | [document] | [Yes/Conditional] | [ ] Received | [day range] | [notes] |
| 2 | [document] | [Yes/Conditional] | [ ] Received | [day range] | [notes] |
[...full checklist per investor type from Phase 2...]

---

## AML/KYC Requirements

| # | Screening | Status | Responsible | Notes |
|---|----------|--------|-------------|-------|
| 1 | OFAC SDN List Screening | [ ] Clear | Fund Administrator | [notes] |
| 2 | PEP Check | [ ] Clear | Fund Administrator | [notes] |
| 3 | Adverse Media | [ ] Clear | Fund Administrator | [notes] |
| 4 | Source of Funds | [ ] Verified | Compliance | [notes] |
[...full AML/KYC checklist...]

---

## Onboarding Timeline

| Phase | Target Days | Status | Notes |
|-------|-----------|--------|-------|
| Document Collection | Days 1-7 | [ ] Complete | [notes] |
| KYC/AML Screening | Days 1-5 | [ ] Complete | [notes] |
| Qualification Verification | Days 3-7 | [ ] Complete | [notes] |
| Legal Review | Days 5-14 | [ ] Complete | [notes] |
| GP Approval | Days 7-14 | [ ] Complete | [notes] |
| Closing | Days 14-21 | [ ] Complete | [notes] |

**Estimated Completion:** [X] business days

---

## Special Considerations

[Any investor-type-specific notes, such as:]
[- ERISA plan asset analysis requirements]
[- Non-US tax treaty considerations]
[- State-specific blue sky requirements]
[- UBTI/ECI exposure warnings]
[- FATCA/CRS reporting obligations]

---

## Recommended Next Steps

1. [ ] Send subscription package to investor
2. [ ] Initiate AML/KYC screening
3. [ ] Verify qualification status (accredited investor / QP / QC)
4. [ ] Collect all required documents per checklist above
5. [ ] Review subscription agreement with fund counsel
6. [ ] Negotiate side letter terms (if applicable) — run `/fund draft-side-letter`
7. [ ] Obtain GP approval of subscription
8. [ ] Execute closing documents and confirm wire receipt
9. [ ] Run `/fund kyc-review` to perform detailed KYC analysis on collected documents
```

### 4.2 Present to User

After generating the output:

1. Confirm the file was generated with its absolute path
2. State the investor type classification applied
3. Summarize the qualification thresholds that apply (accredited investor, QP, QC)
4. State the estimated onboarding timeline
5. Highlight any special considerations (ERISA, FATCA, EDD triggers)
6. Suggest: "Run `/fund kyc-review` to perform detailed KYC analysis on the investor's documents once collected. Run `/fund draft-side-letter` if a side letter needs to be negotiated."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No investor type provided | Ask user to specify investor type (US individual, US entity, non-US individual, non-US entity, ERISA, trust); provide examples |
| Ambiguous investor type | Ask clarifying questions (e.g., "Is this a US or non-US entity? Is it subject to ERISA?") |
| Commitment amount not provided | Generate checklist with all qualification thresholds shown; note that specific requirements depend on amount |
| Fund type not provided | Default to PE fund (Regulation D, 3(c)(7)); note assumption |
| Unusual investor type (e.g., sovereign wealth fund, insurance company) | Apply the closest standard checklist plus additional requirements specific to that investor class |
| Multiple investor types in one request | Generate separate checklists for each investor type, or ask user to specify one at a time |
| Jurisdiction not recognized | Apply general non-US requirements; flag that jurisdiction-specific requirements may apply; recommend consulting local counsel |
