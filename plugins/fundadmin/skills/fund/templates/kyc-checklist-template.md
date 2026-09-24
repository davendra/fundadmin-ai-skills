# KYC / AML Completeness Checklist

<!--
Know Your Customer / Anti-Money Laundering document checklist, used by /fund kyc-review.
For investor onboarding in PE, VC, RE, Credit, Hedge, and Fund of Funds structures.
States, completeness, tax-form validity and the disposition come from
scripts/fund_kyc.py evaluate (see docs/production/kyc.md); do not compute them by hand.
Requirement bases come from the firm's validated rules grid and applicable law
(e.g. FinCEN CDD Rule, 31 CFR 1010.230; FATCA; CRS; EU AML rules), never from this template.
Personal data: pseudonymous references only (LP-001, bo-1, ctl-1); ID, tax and account
numbers masked to the last four; no residential addresses, personal emails, full dates
of birth or signatures.
-->

---

**Disposition:** [ESCALATE FOR EDD / REQUEST DOCUMENTS / HOLD / PRELIMINARY READY FOR HUMAN REVIEW] (from `fund_kyc.py evaluate`; routes work to a person, never an admission, rejection or clearance)

**Readiness:** [HOLD / ESCALATE / PRELIMINARY READY FOR HUMAN REVIEW] | **Document completeness:** [received/required (pct%) from the helper, or NOT CALCULABLE]

---

## Investor Identification

| Field | Value |
|-------|-------|
| **Investor Reference** | [Pseudonymous ID, e.g. LP-001 / investor-07; never the legal name] |
| **Applicant Type** | [individual / corporate / partnership / trust / fund / pension / foundation_endowment / sovereign / nominee_intermediary / other, as in the KYC record schema] |
| **Jurisdiction of Formation / Nationality** | [ISO country code, or UNKNOWN] |
| **Legal Name Present in a Primary Document** | [YES / NO — source locator] |
| **Registration or ID Number Present** | [YES / NO — masked, last four only: ****1234 — source locator] |
| **Date of Formation** | [YYYY-MM-DD, entities only; no dates of birth] |
| **Tax Identification Number** | [Masked, last four only: ****1234] |
| **GIIN (FATCA)** | [If applicable] |
| **LEI (Legal Entity Identifier)** | [If applicable] |
| **CRS Classification** | [From /fund fatca-crs-classify, or UNKNOWN] |
| **FATCA Classification** | [From /fund fatca-crs-classify, or UNKNOWN] |
| **Regulated Entity** | [Yes / No / UNKNOWN — if yes: regulator and source locator] |

---

## Beneficial Ownership Information

<!-- Threshold and control test come from the applicable rule and the firm's grid (ubo_threshold_pct). FinCEN CDD, where it applies, also requires one control person even when threshold owners exist. Where a chain stops at an entity, record the entity; do not invent the people behind it. -->

### Beneficial Owners (at or above the applicable threshold, or percentage unknown)

| # | Owner Ref | Natural Person | Jurisdiction | Ownership % (look-through) | Chain Depth | ID Document Type | ID Number (last four) | Screening | Source |
|---|-----------|----------------|--------------|---------------------------:|------------:|------------------|-----------------------|-----------|--------|
| 1 | [bo-1] | [Y/N] | [code] | [X]% or UNKNOWN | [n] | [type] | [****1234] | [NO MATCH REPORTED / POTENTIAL MATCH / INCOMPLETE / NOT PERFORMED] | [source-N p.x] |
| 2 | [bo-2] | [Y/N] | [code] | [X]% or UNKNOWN | [n] | [type] | [****1234] | [state] | [source-N p.x] |

### Controllers (directors, trustees, general partners, authorised signatories)

| # | Controller Ref | Role | Jurisdiction | ID Document Type | ID Number (last four) | Screening | Source |
|---|----------------|------|--------------|------------------|-----------------------|-----------|--------|
| 1 | [ctl-1] | [role] | [code] | [type] | [****1234] | [state] | [source-N p.x] |

---

## Document Checklist

<!-- State uses the helper's vocabulary: MISSING / INCOMPLETE / EXPIRED / EXPIRING / RECEIVED, or N/A WITH BASIS when the grid does not require the item. Verification is separate and defaults to NOT PERFORMED; VERIFIED WITH EVIDENCE only with supplied evidence of who verified what and when. A readable copy is not verification. -->

### Identity and Formation Documents

| # | Document Type | Requirement Basis | State | Verification | Expiry Date | Source | Notes |
|---|--------------|-------------------|-------|--------------|-------------|--------|-------|
| 1 | **Government-Issued Photo ID** (individuals / owners / controllers) | [law / contract / policy (grid name, date) / UNKNOWN] | [state] | [NOT PERFORMED] | [date] | [locator] | [An expired ID for an already verified investor is handled by the grid's document_expired rule] |
| 2 | **Proof of Address** (individuals) | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [Age limit per the firm's policy] |
| 3 | **Certificate of Incorporation / Formation** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | |
| 4 | **Certificate of Good Standing** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [Age limit per the firm's policy] |
| 5 | **Operating / Partnership / Trust Agreement / Bylaws** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | |
| 6 | **Beneficial Ownership Declaration** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [From the investor; US-formed entities no longer file BOI reports with FinCEN (final rule effective 14 Aug 2026)] |
| 7 | **Authorised Signatory List / Board Resolution** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | |
| 8 | **Power of Attorney** (if signing via agent) | [basis] | [state] | [NOT PERFORMED] | [date] | [locator] | |
| 9 | **Ownership Chart** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | |

### Tax Documents

| # | Document Type | Requirement Basis | State | Verification | Valid Until | Source | Notes |
|---|--------------|-------------------|-------|--------------|-------------|--------|-------|
| 10 | **IRS Form W-9** (US persons) | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [No routine expiry; changes in circumstances apply] |
| 11 | **IRS Form W-8BEN** (non-US individuals) | [basis] | [state] | [NOT PERFORMED] | [helper valid_until] | [locator] | [General rule: 31 December of the third succeeding calendar year after signature, subject to exceptions] |
| 12 | **IRS Form W-8BEN-E** (non-US entities) | [basis] | [state] | [NOT PERFORMED] | [helper valid_until] | [locator] | [Same general rule as W-8BEN] |
| 13 | **IRS Form W-8IMY** (intermediaries / flow-through entities) | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [No routine expiry in the helper; withholding statements and changes in circumstances need review] |
| 14 | **CRS Self-Certification** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [Individual or entity form, per /fund fatca-crs-classify] |

### Investor Qualification Documents

| # | Document Type | Requirement Basis | State | Verification | Expiry Date | Source | Notes |
|---|--------------|-------------------|-------|--------------|-------------|--------|-------|
| 15 | **Accredited Investor Evidence** | [basis] | [state] | [NOT PERFORMED] | [per fund procedure] | [locator] | [Rule 506(c): documentary verification, or the minimum-investment route (SEC staff no-action letter, 12 Mar 2025) with its written representations; see /fund suitability-check] |
| 16 | **Qualified Purchaser Representation** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [Section 2(a)(51)(A)(i)-(iv) route named; for an excepted investment company, the (C) beneficial-owner consents] |
| 17 | **Qualified Client Representation** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [Rule 205-3: at least $1.4M under management or net worth over $2.7M (SEC Order IA-6961, effective 29 Jun 2026); check transition rules] |
| 18 | **ERISA Status Representation** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [Benefit-plan-investor status; exactly 25% does not satisfy the less-than-25% exception] |

### AML / Compliance Documents

| # | Document Type | Requirement Basis | State | Verification | Expiry Date | Source | Notes |
|---|--------------|-------------------|-------|--------------|-------------|--------|-------|
| 19 | **Source of Funds Evidence** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [documented / asserted / not_stated, as in the record] |
| 20 | **Source of Wealth Evidence** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [documented / asserted / not_stated] |
| 21 | **AML Representations** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [A signed representation is not screening or verification] |
| 22 | **Bank Reference Letter** | [basis] | [state] | [NOT PERFORMED] | N/A | [locator] | [Only where the firm's policy requires it] |

---

## Sanctions and Screening Results

<!-- One row per subject and check: the record's subject_ref, each required owner and each controller. Results use the helper vocabulary only: NO MATCH REPORTED / POTENTIAL MATCH / INCOMPLETE / NOT PERFORMED. NO MATCH REPORTED describes the supplied search's scope and date; it is not clearance. Without fund_screening.py output, nothing can be NO MATCH REPORTED. -->

| # | Subject Ref | Check | Source / List | Result | Evidence As Of | Evidence Ref | Notes |
|---|-------------|-------|---------------|--------|----------------|--------------|-------|
| 1 | [investor-07] | Sanctions | [e.g. OFAC SDN and non-SDN lists; UN; EU; UK Sanctions List] | [NO MATCH REPORTED / POTENTIAL MATCH / INCOMPLETE / NOT PERFORMED] | [date] | [ref] | [OFAC 50% rule differs from UK/EU ownership and control tests] |
| 2 | [investor-07] | PEP | [provider / list version] | [result] | [date] | [ref] | [Foreign and domestic PEP measures differ; no automatic former-PEP expiry] |
| 3 | [investor-07] | Adverse media | [provider / scope] | [result] | [date] | [ref] | [Missing research is NOT PERFORMED, never "none found"] |
| 4 | [bo-1 / ctl-1 ...] | [check] | [source] | [result] | [date] | [ref] | |

**Subjects or checks not covered by the evidence (helper `screening.uncovered`):** [list, or none]

**FATF status of connected jurisdictions:** [Jurisdiction on the current FATF call-for-action or increased-monitoring statement: YES / NO / UNKNOWN, with statement date]. EDD follows applicable law and the firm's policy; increased monitoring alone is not an automatic EDD trigger.

### Screening Notes

[For each POTENTIAL MATCH, the facts supplied and the open adjudication question. Any human adjudication is recorded separately with who, when and the evidence relied on.]

---

## Risk Rating

<!-- The rating is the helper's risk_rating from the firm's grid (low / medium / high, or UNASSESSED without a grid). Any reviewer view is labelled commentary and never replaces it. -->

| Risk Factor (grid id) | Outcome | Points | Evidence |
|-----------------------|---------|-------:|----------|
| [RF-...] | [PRESENT / ABSENT / NOT EVALUATED] | [n] | [locator] |

**Risk rating (helper):** [low / medium / high / UNASSESSED] | **Rules grid:** [name, owner, effective date, or "example grid: not firm policy"]

**EDD measures required by the firm's policy:** [list with policy basis, or UNKNOWN]

---

## Completeness

<!-- Quote the helper's completeness {received, required, pct}; pct is rounded down, so 100 means every required document is on file. It measures document collection only, never readiness or compliance. Screening is not part of it. -->

| Measure | Value |
|---------|-------|
| Required documents (grid, this applicant type and rating) | [required] |
| Received (RECEIVED or EXPIRING) | [received] |
| Document completeness | [pct% or NOT CALCULABLE] |

### Outstanding Items

| # | Document / Item | Helper Reason | Owner | Target Date | Status |
|---|----------------|---------------|-------|-------------|--------|
| 1 | [e.g. "W-8BEN-E — EXPIRED, valid until 2025-12-31"] | [reason text] | [owner] | [date] | [Requested / Pending / Overdue] |
| 2 | [e.g. "ubo_declaration — INCOMPLETE"] | [reason text] | [owner] | [date] | [status] |

---

## Human Decisions (recorded separately)

| Decision | Reviewer Ref | Date | Evidence / Decision Reference |
|----------|--------------|------|-------------------------------|
| [e.g. adjudication of a potential match; EDD sign-off required by policy] | [role or pseudonymous ref] | [date] | [ref] |

<!-- The assistant never records a decision on its own; this table only holds decisions a person supplied. Whether higher-risk investors need senior management sign-off is set by the firm's AML policy; record the policy basis. -->

### Periodic Review Schedule

| Review Type | Frequency | Next Review Date |
|-------------|-----------|-----------------|
| **Sanctions Re-Screening** | [Per the firm's policy] | [date] |
| **KYC Refresh** | [Grid `refresh_months` for this rating; UNKNOWN without a grid] | [helper refresh_due; OVERDUE if refresh_overdue] |
| **Tax Document Renewal** | [Helper valid_until for W-8 forms; W-9 and W-8IMY have no routine expiry] | [date] |
| **Screening Record Retention** | [At least 10 years where OFAC rules apply (FR 2025-04864, 21 Mar 2025); otherwise per policy] | [date] |

---

## Status, limitations and data handling
- Report status: [DRAFT / PARTIAL / BLOCKED / READY_FOR_REVIEW] — the same value as the evidence sidecar. Readiness: HOLD / ESCALATE / PRELIMINARY READY FOR HUMAN REVIEW, mapped to the sidecar status with the table in `references/report-contract.md` (REQUEST DOCUMENTS and HOLD -> BLOCKED).
- Assumptions: [list]
- Limitations and checks not performed: [list; UNKNOWN / NOT PERFORMED items; reader mode]
- Data handling: the packaged helpers ran locally and made no network calls; the AI host and its model provider processed the document content; connectors used: [none / list]. Confirm the source documents' confidentiality terms permit this processing.

Not financial, legal or tax advice. Qualified human review is required.

<!--
TEMPLATE USAGE NOTES:

1. Replace all [bracketed placeholders] with values from the KYC record and the helper's evaluation.
2. Required documents come from the firm's validated rules grid (fund_kyc.py validate-grid) for the applicant type and risk rating. Without a firm grid every requirement basis is UNKNOWN; the shipped example grid is structure only and never a basis.
3. Screening must cover the record subject, every natural-person owner the grid's threshold catches (or whose percentage is unknown) and every controller, for sanctions, PEP and adverse media, dated on or after the review date.
4. EDD measures, approvals and review frequency come from the firm's approved AML/KYC policy and applicable law, as captured in its rules grid. There is no automatic EDD for FATF increased monitoring; UK firms apply MLR regulation 33 to a "FATF call for action country" (SI 2026/621).
5. Never write CLEAR, cleared, approved or rejected; use the helper's states and dispositions.
6. Retention of this checklist and its evidence follows the firm's policy and applicable law.
-->
