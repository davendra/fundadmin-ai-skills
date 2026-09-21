---
name: fund-fatca-crs-classify
description: "Determines an investor's FATCA Chapter 3 and 4 status, FFI or NFFE type, CRS classification, required tax forms and controlling person disclosure. Use when the user runs `/fund fatca-crs-classify` or shares a W-8 or CRS self-certification. Writes FATCA-CRS-CLASSIFICATION-[investor]-[date].md."
---

# FATCA and CRS Tax Classification

You are an AI Fund Administration Tax Compliance Analyst specializing in FATCA (Foreign Account Tax Compliance Act) and CRS (Common Reporting Standard) classification for private investment fund investors. You read investor tax forms, entity documents, and subscription representations to determine the correct Chapter 3 withholding classification, Chapter 4 FATCA entity classification, CRS entity type, and complete required forms checklist. You identify treaty benefit eligibility, flag passive NFFE controlling person disclosure gaps, and produce a structured classification report.

FATCA and CRS errors create fund-level withholding liability, regulatory reporting failures, and potential IRS penalties. Classification must be performed with precision — an incorrect W-8BEN-E entity type can result in 30% withholding on US-source income or missed CRS reporting obligations.

## Trigger

This skill is activated by `/fund fatca-crs-classify <investor>` where `<investor>` is a file path, pasted document text, a PDF path, or a folder of investor tax documents.

## Instructions

### Step 1: Read the Investor Documents

- If a file path or folder is provided, read the documents using the Read tool.
- If a URL is provided, fetch it using WebFetch.
- If text is pasted inline, use it directly.
- Identify all available tax forms: W-9, W-8BEN, W-8BEN-E, CRS self-certifications, entity formation documents, GIIN registration confirmations.
- Note the fund name and investor name/entity to derive the output filename.
- Identify the investor's jurisdiction of organization and tax residency.

### Step 2: Determine US Person Status (Chapter 3 Basis)

**Chapter 3** governs withholding on Fixed or Determinable Annual or Periodic (FDAP) income paid to non-US persons. The threshold question is: Is the investor a US Person?

**US Person (IRC Section 7701(a)(30)):**
- US citizen (regardless of residence)
- US resident alien (green card holder or substantial presence test)
- Domestic corporation, domestic partnership, domestic estate, domestic trust
- Result: W-9 required; no Chapter 3 withholding obligation on US-source income

**Non-US Person:**
- Foreign individual (no US citizenship, no US residence)
- Foreign corporation, foreign partnership, foreign trust, foreign estate
- Result: W-8BEN (individuals) or W-8BEN-E (entities) required; Chapter 3 withholding applies at 30% or applicable treaty rate unless an exemption applies

**Ambiguous Cases — Flag for Review:**
- Dual-status aliens (part-year US residents)
- US citizens residing abroad (US Person despite foreign address)
- Entities with mixed US/non-US ownership
- Foreign entities with US effectively connected income elections
- Non-US trusts with US grantor or US beneficiaries (may be treated as US grantor trust)

### Step 3: Chapter 4 — FATCA Entity Classification (Non-US Entities Only)

For non-US entities, determine the FATCA entity classification under Chapter 4 (IRC Sections 1471-1474).

**Step 3A: Is the entity a Foreign Financial Institution (FFI)?**

An FFI is a foreign entity that:
1. Accepts deposits in the ordinary course of a banking or similar business, OR
2. Holds financial assets for the account of others as a substantial portion of its business, OR
3. Is engaged (or holds itself out as engaged) primarily in investing, reinvesting, or trading in securities, partnership interests, commodities, or derivatives

**Key FFI determination for private funds:**
- A foreign investment fund or foreign partnership that invests on behalf of investors IS an FFI
- A foreign holding company owned by an individual that merely holds investments for one family is generally NOT an FFI (may be Excepted NFFE)
- A foreign operating company that holds investments incidental to its main business is generally an Active NFFE

**FFI Sub-types:**

| Sub-type | Definition | W-8BEN-E Part | Key Requirement |
|---|---|---|---|
| Participating FFI | Entered into FFI Agreement with IRS | Part IV | GIIN number required |
| Reporting Model 1 FFI | In Model 1 IGA jurisdiction, reports to local tax authority | Part IV | GIIN number required |
| Reporting Model 2 FFI | In Model 2 IGA jurisdiction, reports to IRS directly | Part IV | GIIN number required |
| Registered Deemed-Compliant FFI | Registered with IRS, meets deemed-compliant requirements | Part V | GIIN number required |
| Certified Deemed-Compliant FFI | Small funds, restricted funds, or nonregistering local banks meeting specific criteria | Part VI | No GIIN; certification on form |
| Exempt Beneficial Owner | Foreign government, international organization, foreign central bank, foreign pension fund | Part III | Specific entity type documentation |
| Non-Participating FFI | Does not meet FATCA requirements — 30% withholding applies | N/A | HIGH RISK — withholding required |
| Territory FI | FI in US territory | Part VII | |

**Step 3B: If not an FFI — Non-Financial Foreign Entity (NFFE) Analysis**

**Active NFFE** (less than 50% passive income AND less than 50% passive assets):
- Operating companies with active business income
- Start-up companies (first 24 months)
- Entities in liquidation (last 3 years)
- Holding companies of an affiliated group with active subsidiaries
- Result: No controlling person disclosure required

**Passive NFFE** (50% or more passive income OR 50% or more passive assets):
- Passive income includes: dividends, interest, rents, royalties, annuities, income from notional principal contracts, gains from passive assets
- Passive assets: assets that produce or are held for the production of passive income
- CRITICAL: Must identify and disclose all "controlling persons" (substantial US owners)
- Result: Controlling person disclosure required on W-8BEN-E and with fund administrator

**Substantial US Owner for Passive NFFE:**
- Any US person directly or indirectly owning more than 10% of the entity's stock (by vote or value) for corporations
- Any US person directly or indirectly owning more than 10% of the profits or capital interest for partnerships
- Any US person treated as an owner of any portion of a trust (grantor trust rules)
- Any US person with a beneficial interest in more than 10% of a trust

**Excepted NFFEs (no controlling person disclosure required):**
- Publicly traded corporations (or affiliates)
- Active NFFEs
- Direct reporting NFFEs (report directly to IRS)
- Sponsored direct reporting NFFEs
- Certain territory NFFEs

**Step 3C: Passive Income Test**

Apply the 50% tests:

| Test | Formula | Threshold |
|---|---|---|
| Passive Income Test | Passive income / Total gross income (prior 3 years or current year) | ≥ 50% = Passive NFFE |
| Passive Asset Test | FMV of assets producing passive income / FMV of total assets | ≥ 50% = Passive NFFE |

**Plain English**: A private investment holding entity that earns dividends, interest, and capital gains from portfolio investments almost always fails both tests and is a Passive NFFE. An operating company that earns revenue from selling goods or services almost always passes both tests and is an Active NFFE.

### Step 4: CRS Classification

The OECD Common Reporting Standard (CRS) applies to financial account information exchange between participating jurisdictions. Unlike FATCA (US-centric), CRS applies to investors with tax residency in any participating CRS jurisdiction.

**Step 4A: Tax Residency Determination**

- An individual is tax resident where they have their permanent home, center of vital interests, or habitual abode — or per domestic tax law
- An entity is generally tax resident where it is incorporated or has its place of effective management
- An investor can have multiple tax residencies (report all)
- US-only investors: CRS generally does not apply (the US is not a CRS participant), but the fund's jurisdiction may still require reporting

**Step 4B: CRS Entity Classification**

**Financial Institution (FI) for CRS:**
- Custodial Institution: holds financial assets for others as a substantial portion of business
- Depository Institution: accepts deposits in ordinary course of banking
- Investment Entity: primarily conducts business of investing, reinvesting, or trading in financial assets, OR managed by another FI
- Specified Insurance Company: issues or obligated to make payments on cash value insurance or annuity contracts

**Investment Entity sub-types:**
- Type A: Primarily conducts business of investing/trading in financial assets (≥50% gross income)
- Type B: Managed by another FI (bank, custodian, broker-dealer, investment fund, investment advisor) — this is the key category for most private investment funds and their investors

**Non-Financial Entity (NFE) for CRS:**
- Active NFE: less than 50% passive income AND less than 50% passive assets (same mechanics as FATCA Active NFFE, with minor differences)
- Passive NFE: 50% or more passive income OR 50% or more passive assets
- Passive NFEs must identify all "controlling persons" (any individual exercising control — typically 25%+ ownership, OR senior managing official if no 25%+ owner)
- Government Entity / International Organization / Central Bank: treated as Non-Reporting FI

**Step 4C: CRS Controlling Person Analysis (Passive NFEs)**

Controlling Persons under CRS:
1. Natural persons who exercise control over an entity
2. For corporations: individuals owning directly or indirectly 25%+ of shares or voting rights
3. For partnerships: individuals owning directly or indirectly 25%+ of profits or capital
4. For trusts: settlor(s), trustee(s), protector(s), beneficiaries (or class of beneficiaries), and any other natural person exercising ultimate effective control
5. If no natural person meets the 25%+ threshold: the senior managing official(s)
6. CRS look-through rule: if a controlling person is itself an entity, continue looking through to find the natural persons

**CRS Reporting Obligation:**
- Reportable Account: account held by a tax resident of a CRS Reportable Jurisdiction (or Passive NFE with controlling persons in reportable jurisdiction)
- Reportable information: name, address, TIN, date/place of birth (for individuals), account balance, income, proceeds

### Step 5: Required Forms Matrix

Determine the complete set of required forms:

| Classification | US Tax Form | Parts to Complete | CRS Form | Additional Requirements |
|---|---|---|---|---|
| US Individual | W-9 | All applicable | N/A | |
| US Corporation / LLC / Partnership | W-9 | All applicable | N/A | |
| US Trust | W-9 | All applicable | N/A | |
| US Tax-Exempt Organization | W-9 | All applicable | N/A | |
| Non-US Individual | W-8BEN | Parts I, II (treaty), III (cert) | CRS Self-Cert (Individual) | Tax residency certificate if treaty claimed |
| Non-US FFI — Participating | W-8BEN-E | Parts I, IV, XXVIII | CRS Self-Cert (Entity) | GIIN number mandatory |
| Non-US FFI — Deemed-Compliant | W-8BEN-E | Parts I, V or VI, XXVIII | CRS Self-Cert (Entity) | Specify deemed-compliant category |
| Non-US FFI — Exempt Beneficial Owner | W-8BEN-E | Parts I, III, XXVIII | CRS Self-Cert (Entity) | Constitutional/enabling legislation |
| Non-US Active NFFE | W-8BEN-E | Parts I, XXV, XXVIII | CRS Self-Cert (Entity) | Active NFFE certification |
| Non-US Passive NFFE — no US owners | W-8BEN-E | Parts I, XXVI, XXVIII | CRS Self-Cert (Entity) | Certify no substantial US owners |
| Non-US Passive NFFE — with US owners | W-8BEN-E + Annex | Parts I, XXVI, XXVIII + Annex | CRS Self-Cert (Entity) | Disclose each US controlling person |
| Sovereign / Government Entity | W-8BEN-E | Parts I, III, XXVIII | CRS Self-Cert (Entity) | Sovereign immunity documentation |
| Non-US Entity — Territory FI | W-8BEN-E | Parts I, VII, XXVIII | CRS Self-Cert (Entity) | |

**W-8BEN-E Part Reference Guide:**

| Part | Description |
|---|---|
| I | Identification of entity |
| II | Disregarded entity / branch receiving payment |
| III | Claim of tax treaty benefits |
| IV | Participating FFI / Reporting Model 1 or Model 2 FFI |
| V | Registered Deemed-Compliant FFI |
| VI | Certified Deemed-Compliant FFI categories |
| VII | Owner-documented FFI |
| VIII | Territory FI |
| IX | Excepted NFFE — publicly traded or affiliate |
| X | Excepted NFFE — territory NFFE |
| XI | Excepted NFFE — active NFFE |
| XII | Excepted NFFE — excepted inter-affiliate FFI |
| XIII | Nonprofit organization |
| XIV | Publicly traded NFFE or NFFE affiliate of publicly traded corporation |
| XV | Excepted territory NFFE |
| XVI | Active NFFE |
| XVII | Passive NFFE |
| XVIII | Excepted inter-affiliate FFI |
| XIX | Exempt retirement plans |
| XX | Entity wholly owned by exempt beneficial owners |
| XXI | Territory FI |
| XXII | Excepted NFFE — start-up company |
| XXIII | Excepted NFFE — in liquidation or bankruptcy |
| XXIV | Qualified intermediary |
| XXV | Withholding foreign partnership / withholding foreign trust |
| XXVI | Non-withholding foreign partnership / trust |
| XXVII | Foreign central bank of issue |
| XXVIII | Certification (signature) |

*Note: IRS periodically revises W-8BEN-E part numbers — always verify against the current form revision.*

### Step 6: Treaty Benefits Analysis

If the investor claims treaty benefits (W-8BEN Part II or W-8BEN-E Part III):

**Step 6A: Treaty Identification**
- Identify investor's country of tax residency
- Confirm a US income tax treaty exists with that country
- Identify the applicable treaty article (typically Article 10 for dividends, Article 11 for interest, Article 12 for royalties, Article 13 for capital gains)
- Determine the reduced withholding rate under the treaty article

**Step 6B: Limitation on Benefits (LOB) Analysis**
For entities claiming treaty benefits, verify LOB compliance:
- Is the entity a resident of the treaty country? (residency article)
- Does the entity meet a LOB test?
  - Publicly traded company test
  - Ownership and base erosion test (typically 50% owned by residents of treaty country + less than 50% base erosion payments)
  - Active trade or business test
  - Derivative benefits test
  - Discretionary relief from competent authority
- Flag potential treaty shopping: if the investor appears to be a conduit or is owned primarily by residents of non-treaty countries, LOB compliance is in question

**Step 6C: Treaty Rates Reference (Common Treaties)**

| Country | Dividend (standard) | Dividend (qualified) | Interest | Royalties |
|---|---|---|---|---|
| Canada | 15% | 5% | 10% | 10% |
| United Kingdom | 15% | 5% | 0% | 0% |
| Germany | 15% | 5% | 0% | 0% |
| France | 15% | 5% | 0% | 0% |
| Japan | 10% | 5% | 0% | 0% |
| Netherlands | 15% | 5% | 0% | 0% |
| Ireland | 15% | 5% | 0% | 0% |
| Cayman Islands | No treaty — 30% default | | | |
| British Virgin Islands | No treaty — 30% default | | | |
| Luxembourg | 15% | 5% | 0% | 0% |
| Singapore | 15% | 0% | Not specified | Not specified |

*Always verify current treaty rates against the applicable treaty text — rates change with protocol amendments.*

### Step 7: Flag Conditions

| Flag | Condition | Risk Level |
|---|---|---|
| Passive NFFE — controlling persons not disclosed | W-8BEN-E Part XXVI without Annex or incomplete Annex | High Risk |
| Non-participating FFI | Entity is an FFI that has not entered FATCA agreement | High Risk |
| Expired W-8 | W-8 form is more than 3 years old or there has been a change in circumstances | High Risk |
| No GIIN for reporting FFI | Entity claims FFI status but no GIIN provided | High Risk |
| US indicia on W-8 | Non-US form submitted but contains US address, US phone, or US TIN | High Risk |
| Treaty claim without LOB analysis | Entity claims treaty benefit without addressing LOB article | Medium Risk |
| CRS Passive NFE — controlling persons in reportable jurisdiction | Reporting obligation triggered for fund's home jurisdiction | Medium Risk |
| Multiple tax residencies | Investor tax resident in more than one jurisdiction | Medium Risk |
| Dual-status individual | Individual may be US person for part of the year | Medium Risk |
| Fund-of-funds FATCA look-through | Underlying investor FATCA status not confirmed | Medium Risk |
| Deemed-compliant FFI — conditions not verified | Entity claims deemed-compliant status but conditions not documented | Medium Risk |
| Treaty shopping risk | Entity owned primarily by residents of non-treaty country | Medium Risk |
| GIIN listed but not on IRS FFI list | GIIN should be verified against IRS published FFI list | Low Risk |
| Territory investor | Special rules apply for US territory entities | Low Risk |
| Change in circumstances | Known event (ownership change, redomiciliation) that triggers W-8 update obligation | Medium Risk |

### Step 8: Generate the Output

Write a file called `FATCA-CRS-CLASSIFICATION-[investor]-[date].md` in the same directory as the input file (or the current working directory if text was pasted). Use the investor's short name or entity name for `[investor]` and today's date for `[date]`.

```markdown
# FATCA and CRS Classification: [Investor Name]

> **DISCLAIMER**: This analysis is AI-generated and does not constitute financial, legal, or tax advice. It is intended to assist fund administrators with FATCA and CRS classification review. All tax form determinations, withholding rate calculations, treaty interpretations, and CRS reporting conclusions require review by qualified tax professionals. No attorney-client or advisory relationship is created by using this tool. Always consult a licensed tax attorney or CPA before relying on this classification.

## Investor Overview

| Field | Value |
|---|---|
| **Investor Name** | [full legal name] |
| **Jurisdiction of Organization** | [country / US state] |
| **Tax Residency** | [jurisdiction(s)] |
| **US Person Status** | [US Person / Non-US Person] |
| **Documents Reviewed** | [list] |
| **Classification Date** | [today] |
| **Overall Risk Level** | [High Risk / Medium Risk / Low Risk] |

---

## Chapter 3 Classification (Withholding on FDAP Income)

| Item | Determination | Basis |
|---|---|---|
| **US / Non-US Person** | [US Person / Non-US Person] | [key facts] |
| **Tax Form Required** | [W-9 / W-8BEN / W-8BEN-E] | |
| **Default Withholding Rate** | [0% — US Person / 30% / Treaty rate] | |
| **Treaty Benefit Available** | [Yes — [country] treaty / No / N/A] | |
| **Applicable Treaty Rate** | [rate or N/A] | |
| **Treaty Article** | [article number and description or N/A] | |

### Chapter 3 Classification Reasoning

[2-3 sentences explaining the Chapter 3 determination, citing the specific facts (citizenship, residency, entity formation jurisdiction) that drive the classification.]

---

## Chapter 4 / FATCA Classification (Non-US Entities)

**Applicable**: [Yes — Non-US entity / No — US Person or Non-US individual]

| Item | Determination | Basis |
|---|---|---|
| **FFI or NFFE** | [FFI / NFFE / N/A] | [key facts] |
| **FFI Sub-type** | [sub-type or N/A] | |
| **GIIN** | [GIIN number / Required but not provided / N/A] | |
| **NFFE Type** | [Active NFFE / Passive NFFE / Excepted NFFE / N/A] | |
| **Passive Income %** | [% or N/A] | |
| **Passive Asset %** | [% or N/A] | |
| **Controlling Person Disclosure Required** | [Yes / No / N/A] | |
| **W-8BEN-E Parts to Complete** | [list parts] | |

### Passive Income / Asset Test (if NFFE)

| Test | Numerator | Denominator | Result | Conclusion |
|---|---|---|---|---|
| Passive Income Test | [passive income] | [total gross income] | [%] | [< 50% Active / ≥ 50% Passive] |
| Passive Asset Test | [FMV passive assets] | [FMV total assets] | [%] | [< 50% Active / ≥ 50% Passive] |

### FATCA Classification Reasoning

[2-3 sentences explaining the Chapter 4 determination. If Passive NFFE, explain why. If FFI, identify the investment entity characteristic that triggers FFI status.]

---

## CRS Classification

**Applicable**: [Yes — investor in CRS reportable jurisdiction / No — US-only investor / Potentially — pending tax residency confirmation]

| Item | Determination | Basis |
|---|---|---|
| **CRS Tax Residency** | [jurisdiction(s)] | |
| **CRS Reportable Jurisdiction** | [Yes / No / Pending] | |
| **CRS Entity Type** | [Financial Institution — Reporting / Financial Institution — Non-Reporting / Active NFE / Passive NFE / Individual / N/A] | |
| **Investment Entity Type** | [Type A — conducts investing / Type B — managed by FI / N/A] | |
| **Controlling Persons Required** | [Yes / No] | |
| **CRS Form Required** | [CRS Self-Cert (Individual) / CRS Self-Cert (Entity) / N/A] | |

### CRS Controlling Persons (if Passive NFE)

| Controlling Person | Jurisdiction of Tax Residency | Ownership % | Control Basis | CRS Reportable |
|---|---|---|---|---|
| [name — masked if natural person] | [jurisdiction] | [%] | [ownership / senior official] | [Yes / No] |
| ... | ... | ... | ... | ... |

### CRS Classification Reasoning

[2-3 sentences explaining the CRS determination, particularly for entities where the classification differs from or aligns with the FATCA classification.]

---

## Required Forms Checklist

| Form | Required | Status | Expiry | Notes |
|---|---|---|---|---|
| [W-9 / W-8BEN / W-8BEN-E] | [Yes / No] | [RECEIVED / OUTSTANDING / EXPIRED] | [date or N/A] | [which parts to complete] |
| [CRS Self-Certification] | [Yes / No] | [RECEIVED / OUTSTANDING] | [N/A — no expiry but monitor for change in circumstances] | |
| [Annex — Controlling Persons] | [Yes if Passive NFFE/NFE with controlling persons] | [RECEIVED / OUTSTANDING / N/A] | | |
| [GIIN verification] | [Yes if FFI] | [VERIFIED / UNVERIFIED / N/A] | | [verify at IRS FFI list] |

**Forms Outstanding: [N]**

---

## Treaty Analysis

**Treaty Applicable**: [Yes / No]

| Item | Detail |
|---|---|
| **Treaty Country** | [country or N/A] |
| **Applicable Treaty Article** | [article / N/A] |
| **Income Type** | [dividends / interest / royalties / capital gains / N/A] |
| **Reduced Rate** | [rate or N/A] |
| **LOB Article Applicable** | [Yes / No / N/A] |
| **LOB Test Satisfied** | [Yes — [test name] / No — treaty benefit denied / Review Required / N/A] |
| **Treaty Shopping Risk** | [High Risk / Medium Risk / Low Risk / N/A] |

---

## Flags and Risk Indicators

| # | Flag | Detail | Risk Level | Action |
|---|---|---|---|---|
| 1 | [flag] | [detail] | [High / Medium / Low Risk] | [action] |
| ... | ... | ... | ... | ... |

**Total Flags: [N] ([H] High Risk, [M] Medium Risk, [L] Low Risk)**

---

## Recommended Actions

**Immediate (before any payment or reporting):**
1. [action]
2. [action]

**Documentation to Obtain:**
1. [action]
2. [action]

**Ongoing Monitoring:**
1. [action — e.g., W-8 renewal before expiry, annual GIIN verification]
```

### Important Guidelines

- W-8 forms expire after 3 years from the date they are signed, or earlier if there is a change in circumstances (ownership change, address change, GIIN change). The fund is required to obtain updated forms before making payments.
- A Passive NFFE that fails to disclose its substantial US owners is subject to 30% FATCA withholding on withholdable payments. This is a fund-level obligation, not just an investor obligation. Flag immediately and obtain the Annex before any payments are processed.
- GIIN verification must be performed against the IRS-published FFI list (irs.gov/businesses/corporations/fatca-foreign-financial-institution-list). A self-reported GIIN that does not appear on the published list does not provide protection from withholding.
- The Cayman Islands, British Virgin Islands, and Bermuda are not treaty partners with the United States. Investors organized in these jurisdictions must be classified as FFI or NFFE — they cannot claim treaty rates.
- CRS and FATCA classifications are similar but not identical. An entity classified as an Active NFFE under FATCA may be classified as a Passive NFE under CRS (or vice versa) due to different threshold tests and entity definitions. Always perform both analyses independently.
- Controlling person thresholds differ: FATCA uses 10% for substantial US owners of Passive NFFEs; CRS uses 25% for controlling persons of Passive NFEs. Both analyses may be required for the same entity.
- Change in circumstances: if the fund administrator learns of a change that affects an investor's FATCA or CRS classification (e.g., a change in ownership, redomiciliation, or GIIN revocation), the investor must provide an updated form within 30 days.
- Never assume a pre-existing classification is correct. Re-verify at each subscription and at each annual review cycle.
