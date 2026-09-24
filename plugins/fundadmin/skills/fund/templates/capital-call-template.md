# Capital Call Notice

<!--
Capital call drafting template for qualified human review.
No compliance certification. Populate contractual terms from identified sources;
retain [MISSING] wherever the governing provision or required evidence is absent.
-->

> DRAFT — Not financial, legal or tax advice. Qualified human review is required.
> This template does not issue a notice or approve payment. Any ILPA comparison
> requires an identified publication/version, mapped checklist and supporting evidence.

---

## CAPITAL CALL NOTICE NO. [NUMBER]

**[FUND LEGAL NAME]**
([Sourced entity form and jurisdiction; otherwise MISSING])

---

| Field | Value |
|-------|-------|
| **Fund Name** | [Full legal name of the fund] |
| **Capital Call Number** | [Sequential number — e.g., Capital Call No. 7] |
| **Date of Notice** | [YYYY-MM-DD] |
| **Due Date** | [Sourced date, time and timezone; otherwise MISSING] |
| **Notice Terms** | [Provision, service rules, business-day calendar and calculation; otherwise MISSING] |
| **Total Amount Called** | $[Total amount being called from all LPs] |

---

## Legal Basis

This Capital Call is made pursuant to Section [X.X] of the Amended and Restated Agreement of Limited Partnership of [Fund Legal Name], dated [LPA Date] (the "Partnership Agreement"). Capitalized terms used herein and not otherwise defined have the meanings assigned to them in the Partnership Agreement.

The General Partner, [GP Entity Legal Name], proposes the following call amounts under [sourced allocation provisions and eligible pools; otherwise MISSING].

---

## Purpose of Capital Call

<!-- Describe the purpose(s) for which the capital is being called. Be specific about allocations. -->

| Purpose | Amount | % of Call |
|---------|--------|-----------|
| [e.g., "Investment in Portfolio Company ABC, Inc."] | $[amount] | [X]% |
| [e.g., "Follow-on investment in Portfolio Company XYZ Corp."] | $[amount] | [X]% |
| [e.g., "Management fees — Q[X] [Year]"] | $[amount] | [X]% |
| [e.g., "Fund expenses (legal, audit, administration)"] | $[amount] | [X]% |
| [e.g., "Organizational expenses"] | $[amount] | [X]% |
| [e.g., "Subscription facility repayment (original use: [investment / fees / expenses])"; state that the call repays the facility and show facility interest and fees as separate lines] | $[amount] | [X]% |
| **Total** | **$[total]** | **100%** |

---

## Per-LP Capital Call Schedule

| Investor ID | Total Commitment | Previously Called | This Call | Remaining Unfunded | % of Commitment Called to Date |
|-------------|-----------------|-------------------|-----------|-------------------|-------------------------------|
| [LP-001] | $[commitment] | $[cumulative prior calls] | $[this call amount] | $[remaining] | [X]% |
| [LP-002] | $[commitment] | $[cumulative prior calls] | $[this call amount] | $[remaining] | [X]% |
| [LP-003] | $[commitment] | $[cumulative prior calls] | $[this call amount] | $[remaining] | [X]% |
| [LP-004] | $[commitment] | $[cumulative prior calls] | $[this call amount] | $[remaining] | [X]% |
| [LP-005] | $[commitment] | $[cumulative prior calls] | $[this call amount] | $[remaining] | [X]% |
| **TOTAL** | **$[total commitments]** | **$[total previously called]** | **$[total this call]** | **$[total remaining]** | **[X]%** |

---

## Impact on Unfunded Commitment

<!-- Use only the actual LPA recallability/recycling terms; purpose alone does not establish them. ILPA's Capital Call & Distribution Template v2.0 (released 11 Sep 2025; implementation Q1 2027) expresses recallability through each line's impact on unfunded commitment: an ILPA published position, not a compliance test. -->

| Purpose line | Amount | Impact on Unfunded Commitment | Governing provision |
|--------------|--------|-------------------------------|---------------------|
| [purpose] | $[amount] | [Reduces unfunded / Restores unfunded (recallable or recycled amount) / No effect / MISSING] | [provision / MISSING] |

**Commitment Period Status:** [Active / Expired on [date]]

<!-- If the commitment period has expired, note the LPA basis for making this call (e.g., follow-on investments, expenses, or reserves per Section X.X). -->

---

## Due Date and Late Payment Terms

**Payment Due Date:** [YYYY-MM-DD]

**Receipt and settlement requirements:** [Sourced cut-off time, timezone, currency and settlement terms; otherwise MISSING].

**Late Payment Consequences:** [Exact governing provision; otherwise MISSING].

- **Default trigger and cure period:** [Sourced conditions and timing; otherwise MISSING]
- **Default Interest:** [Only the sourced rate, basis, accrual dates and conditions; otherwise MISSING]
- **Other remedies:** [Only remedies established by the governing provisions, including conditions and limits; otherwise MISSING]

**If you anticipate any difficulty in meeting the Due Date, please contact [Contact Name] at [email/phone] immediately.**

---

## Wire Instructions

Please wire funds to the following account:

| Field | Value |
|-------|-------|
| **Bank Name** | [Bank name] |
| **Bank Address** | [Bank address] |
| **ABA / Routing Number** | [masked — last four only] |
| **Account Name** | [Fund legal name or custodial account name] |
| **Account Number** | [masked — last four only] |
| **SWIFT Code** | [SWIFT code — for international wires] |
| **Reference** | [investor reference ID — Capital Call No. [X]] |

**For international transfers, please also include:**

| Field | Value |
|-------|-------|
| **Intermediary Bank** | [intermediary bank name, if applicable] |
| **Intermediary SWIFT** | [intermediary SWIFT code] |

Please ensure the wire reference includes your investor reference and the capital call number for proper allocation.

<!-- The saved draft shows masked account details only. The authorised operator inserts the full payment instructions from the verified system of record at issue, outside the saved report, after independent callback verification of any new or changed instruction. Legal names are merged from the protected investor register at issue. -->

---

## Confirmation

Upon sending your wire, please confirm payment by emailing [confirmation email address] with:
1. Wire confirmation / reference number
2. Date of wire
3. Amount wired
4. Investor reference

---

## General Partner Signature

On behalf of the General Partner:

**[GP Entity Legal Name]**

By: ____________________________

Name: [Authorized Signatory Name]

Title: [Title — e.g., Managing Director, Authorized Person]

Date: ____________________________

---

## Status, limitations and data handling
- Report status: [DRAFT / PARTIAL / BLOCKED / READY_FOR_REVIEW] — the same value as the evidence sidecar.
- Assumptions: [list]
- Limitations and checks not performed: [list; UNKNOWN / NOT PERFORMED items]
- Data handling: the packaged helpers ran locally and made no network calls; the AI host and its model provider processed the document content; connectors used: [none / list]. Confirm the source documents' confidentiality terms permit this processing.

Not financial, legal or tax advice. Qualified human review is required.

---

<!--
TEMPLATE USAGE NOTES:

1. Use sourced values and citations; keep missing terms visible. Dollar placeholders are illustrative: use the actual single currency throughout.
2. Identify eligible pools, excused/excluded LPs and any sourced GP participation; do not assume every partner participates in every purpose.
3. Use fund_calculations.py allocate for each eligible pool; preserve the requests, rounded allocations and residual workpapers. Reconcile their sum to the total call amount.
4. Reconcile commitments and capital activity against the supplied ledger and governing recycling/recallability terms, recording adjustments explicitly rather than assuming a simple identity fits all structures.
5. Late payment terms should match the specific provisions in the LPA — do not use generic terms.
6. Wire instructions should be verified with the fund administrator before each capital call.
7. Designate recallability only from governing terms; bridge financing or a short duration does not establish recallability.
8. If the commitment period has expired, confirm the LPA basis for the call.
9. Derive the notice interval, service rules, cut-off and business-day calendar from identified governing provisions. Do not substitute a customary minimum or assumed time.
10. This template should be reviewed by fund counsel before first use.
11. Preserve the full legal fund name in content. Obtain the CAPITAL-CALL basename from fund_report.py filename and save using the shared report contract's isolated run and write-report helper; never create a basename by replacing spaces alone.
-->
