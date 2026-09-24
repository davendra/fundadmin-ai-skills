# LPA Review Report

> DISCLAIMER: This analysis is AI-generated. Not financial, legal or tax advice. Qualified human review is required. It is intended as a starting point for fund administration review. Always consult qualified legal counsel and fund administration professionals before relying on it or negotiating fund terms.

---

## LPA Document Favourability: [score/100 or unavailable] — Methodology v2

Heuristic document assessment, not a safety verdict, legal certification or investment recommendation. If the legacy “LPA Safety Score” label is used, retain this qualification.

Report status: [PARTIAL / READY_FOR_REVIEW] — the same value as the evidence sidecar.

## Score Calculation

| Dimension | Raw value | Normalised favourability | Weight / 80 | Contribution | Evidence / rationale |
|-----------|-----------|-------------------------|-------------|--------------|----------------------|
| Terms | [0–100 or unavailable] | [same] | 20/80 | [value] | [finding/source IDs] |
| Risk | [1–10 or unavailable; higher is worse] | [(10-risk) × 100/9] | 25/80 | [value] | [finding/source IDs] |
| Compliance | [0–100 or unavailable] | [same] | 20/80 | [value] | [finding/source IDs and authority] |
| Obligations | [0–100 or unavailable] | [same] | 15/80 | [value] | [finding/source IDs] |

Recommendations are excluded. Use `scripts/fund_lpa_score.py` and retain its exact JSON input/output and item calculations, following `docs/production/lpa-scoring.md`. Any unknown required dimension makes the aggregate unavailable; do not renormalise over available dimensions. Round the final result to two decimals, half up.

## Coverage and Confidence

[Assessed/expected checks and percentage, reviewed pages/sections, exclusions, unreadable or missing material, confidence rationale and unresolved questions. Coverage is separate from favourability and is not a probability of correctness.]

---

## Key Issues and Asks

| # | Issue | Source locator | Direct effect | Proposed stance |
|---|---|---|---|---|
| 1 | [issue] | [source-N, page/section] | [effect, taken from the source] | [push / trade / accept] |

Rank by materiality. A stance is a negotiation or remediation position, never an investment, admission, payment or compliance verdict.

<!-- Five to eight issues. Take stances from the recommendations agent; if recommendations are unavailable, write "not assessed — recommendations unavailable". -->

---

## Executive Summary

<!-- Write 3-4 sentences covering: what type of fund this is, the overall risk posture, the most significant finding, and its direct economic effect on LPs.

Describe; do not advise. Close on the severity and the scope of what would have
to change, not on what the reader should do with their money.

Do not write "we recommend committing", "do not commit", "proceed", "decline" or any variant.

The specific asks belong under Negotiation Priorities, and the reader's own
counsel decides the rest. -->

[This is a [fund type] fund managed by [GP Entity] with a target size of [fund size]. Document favourability under methodology v2 is [score/100 or unavailable, with the missing dimensions]; it is a heuristic, not a verdict. The most significant concern is [top risk — e.g., aggressive carry terms, weak clawback, broad GP discretion]. [One sentence on severity and scope — e.g., "Economics sit at the GP-favorable end on carry and post-investment-period fees, and the governance gaps are concentrated in key person and LPAC consent; the [n] priorities below set out what a revision would need to cover."]]

---

## Regulatory Intake

| Fact | Value (or UNKNOWN) | Date supplied | Status |
|------|--------------------|---------------|--------|
| Adviser / GP status (incl. carry recipient and custody route if registered) | [value or UNKNOWN] | [date] | User-supplied, not verified |
| Offering route and fund exclusion | [value or UNKNOWN] | [date] | User-supplied, not verified |
| Investor mix | [value or UNKNOWN] | [date] | User-supplied, not verified |
| Marketing jurisdictions | [value or UNKNOWN] | [date] | User-supplied, not verified |

Supplied facts decide applicability only; they are not evidence that any regulatory duty was met.

## Source Register

| Source ID | Document / authority | Version / checked date | Page, section or lines | Availability |
|-----------|----------------------|------------------------|------------------------|--------------|
| [ID] | [file or retrieved authority] | [version/date] | [locator] | [verified / secondary only / missing] |

Every finding below must carry a finding ID and source ID with an exact locator and quotation. Absence findings must describe the reviewed scope and search. Separate facts, assumptions and drafting proposals. All examples in this template are illustrative, not evidence: replace them with verified findings or unavailable values. Cite the source and scope of any benchmark; never infer market prevalence from sample ranges. Financial estimates require sourced inputs, formula and assumptions. No investment verdicts.

---

## Fund Details

| Field | Value |
|-------|-------|
| **Fund Name** | [Full legal name of the fund entity] |
| **Fund Type** | [PE Buyout / Venture Capital / Real Estate / Credit / Hedge / Fund of Funds] |
| **GP Entity** | [General Partner legal name and jurisdiction of formation] |
| **Fund Size** | Target: $[X] / Hard Cap: $[Y] |
| **Vintage** | [Year of final closing or first investment] |
| **Management Fee** | [X]% on [committed capital / invested capital / NAV] during [investment period / post-investment period] |
| **Carried Interest** | [X]% [whole-fund / deal-by-deal] |
| **Preferred Return / Hurdle** | [X]% [simple / compounded annually / compounded quarterly] |
| **Fund Term** | [X] years + [Y] x [Z]-year extensions [with/without LP consent] |
| **Commitment Period** | [X] years [with extension provisions description] |
| **LPAC** | [Composition summary — e.g., "5 members, elected by majority in interest"] |
| **Governing Law** | [State / jurisdiction] |
| **AUM (if stated)** | [$X or "Not stated"] |

---

## Risk Dashboard

<!-- Each score is the mean of the unrounded fund-risks composites tagged with that category (a provision with several tags counts in each row), with its item count. Write "not assessed" where no item carries the tag. Conditional regulatory items with UNKNOWN applicability are excluded and listed, not scored. -->

| Risk Category | Mean composite (n items) | Assessment |
|---------------|--------------------------|------------|
| Fee Risk | [mean (n) or not assessed] | [One-line summary — e.g., "2.5% on committed capital with no step-down (s. 6.1)"] |
| Liquidity Risk | [mean (n) or not assessed] | [e.g., "10-year term with two 1-year extensions at GP discretion, no LP vote required"] |
| Governance Risk | [mean (n) or not assessed] | [e.g., "LPAC advisory only on conflicts; no LP consent for investment period extension"] |
| Regulatory Risk | [mean (n) or not assessed; excluded: n] | [e.g., "No tax distribution provision; ERISA items excluded, investor mix UNKNOWN"] |
| Operational Risk | [mean (n) or not assessed] | [e.g., "Broad delegation authority to affiliates"] |
| GP-LP Asymmetry | [mean (n) or not assessed] | [e.g., "GP can modify waterfall for future investors without existing LP consent"] |
| Concentration Risk | [mean (n) or not assessed] | [e.g., "NAV-based facility permitted without a cap or permitted-use list"] |
| Valuation Risk | [mean (n) or not assessed] | [e.g., "Valuation at GP discretion with no independent review"] |
| Key Person Risk | [mean (n) or not assessed] | [e.g., "No named key persons; no suspension of investment period on key person departure"] |
| Clawback Risk | [mean (n) or not assessed] | [e.g., "Clawback net of taxes at the rate stated in s. 12.1, with no escrow requirement"] |

**Summary:**
| Risk Level | Count | Provisions |
|------------|-------|---------|
| HIGH Risk | [number] | [Comma-separated list of provision names] |
| MEDIUM Risk | [number] | [Comma-separated list of provision names] |
| LOW Risk | [number] | [Comma-separated list of provision names] |

---

## Provision-by-Provision Analysis

### HIGH RISK PROVISIONS

<!-- Repeat this block for EACH high-risk provision found in the LPA. -->

#### [Finding ID] [Provision Name] — [Source ID], Section [X.X]

- **What it says:** [Plain English summary of what this provision means. No legal jargon. Write as if explaining to an institutional LP operations team. Example: "The GP can extend the investment period by one year without any LP vote or LPAC consent, as long as the GP provides 30 days' notice."]

- **Why it is risky:** [Specific explanation of the danger in GP-LP dynamics context. Example: "This lets the GP continue deploying capital (and charging full management fees on committed capital) for an additional year without LP approval. In a poor-performing fund, this extends LP exposure and delays the fee step-down the LPA provides after the investment period."]

- **Financial exposure:** [Effect computed with the packaged helper from source figures, with formula and inputs; otherwise "Not quantified — [missing input]". Example: "Fund-level fee during a one-year extension = 2% x $500M total commitments stated in s. 1.4 as the fee base = $10M (fund_calculations.py arithmetic); LP share not quantified — commitment not supplied."]

- **Comparison:** [Identified, dated comparable source with citation, or ILPA published position [date] as a discussion point; otherwise "No comparable source assessed".]

- **Proposed change:** [Specific alternative language to propose. Example: "Replace with: 'The General Partner may extend the Investment Period for one (1) additional year only with the prior written approval of a majority in interest of the Limited Partners. During any such extension, the Management Fee shall be calculated on Invested Capital (at cost) rather than Committed Capital.'"]

---

<!-- Add more high-risk provisions using the same format above. -->

### MEDIUM RISK PROVISIONS

<!-- Repeat this block for EACH medium-risk provision. Same format as high risk. -->

#### [Finding ID] [Provision Name] — [Source ID], Section [X.X]

- **What it says:** [Plain English summary]

- **Why it is risky:** [Specific explanation]

- **Financial exposure:** [Computed from source figures, or "Not quantified — [missing input]"]

- **Comparison:** [Identified, dated source, otherwise "No comparable source assessed"]

- **Proposed change:** [Specific alternative language for counsel review]

---

### LOW RISK PROVISIONS

<!-- Brief summary of lower-risk provisions, with finding and source IDs. No need for the full 5-field format. -->

- **[Provision Name] (Section [X.X]):** [One-sentence summary of what the clause provides. Example: "Indemnification excludes bad faith, gross negligence and willful misconduct (s. 9.3)."]

- **[Provision Name] (Section [X.X]):** [One-sentence summary]

- **[Provision Name] (Section [X.X]):** [One-sentence summary]

---

## Protections not found in the supplied text (scope searched)

<!-- List each protection the terms agent searched for and did not find, with the scope searched (full document / excerpt). Report absence within the supplied scope only; do not say a protection should be present. -->

Scope searched: [full document as supplied / excerpt: sections searched]

| # | Protection not found | Direct effect of its absence | Risk Level |
|---|-------------------|----------------|------------|
| 1 | [e.g., "Key Person Provision"] | [e.g., "Without named key persons and a suspension trigger, the GP can lose its most experienced investment professionals without any impact on fund operations or LP recourse."] | HIGH |
| 2 | [e.g., "GP Removal (No-Fault Divorce)"] | [e.g., "LPs have no ability to remove the GP, for cause or otherwise, whatever the vote."] | HIGH |
| 3 | [e.g., "LPAC Consent for Conflicts"] | [e.g., "No LPAC consent required for conflict transactions. GP can engage in self-dealing without independent oversight."] | HIGH |
| 4 | [e.g., "Fee Offset Provisions"] | [e.g., "No offset of transaction, monitoring, or consulting fees against management fees. GP retains 100% of portfolio company fees."] | MEDIUM |
| 5 | [e.g., "Carry Escrow"] | [e.g., "No escrow holdback on carried interest distributions. Clawback is the only protection, which requires GP to return cash already spent."] | MEDIUM |

---

## Obligations & Deadlines

<!-- Map out every time-bound obligation in the LPA. Include who is responsible, what triggers it, and what the consequence is for non-compliance. -->

| Obligation | Responsible Party | Trigger / Deadline | Consequence of Non-Compliance |
|------------|-------------------|-------------------|-------------------------------|
| [e.g., "Fund capital calls"] | [e.g., "GP"] | [e.g., "10 business days' notice per Section 3.2"] | [e.g., "LP default provisions trigger per Section 3.5 — forfeiture of up to 50% of capital account"] |
| [e.g., "Quarterly financial reports"] | [e.g., "GP"] | [e.g., "Within 60 days of quarter end per Section 8.1"] | [e.g., "No stated consequence"] |
| [e.g., "Annual audited financials"] | [e.g., "GP"] | [e.g., "Within 120 days of fiscal year end per Section 8.2"] | [e.g., "No stated consequence"] |
| [e.g., "LPAC meeting"] | [e.g., "GP"] | [e.g., "At least annually, or upon request of majority of LPAC"] | [e.g., "No stated consequence"] |
| [e.g., "Capital call funding"] | [e.g., "LPs"] | [e.g., "Within 10 business days of capital call notice"] | [e.g., "Default interest at prime + 5%, forfeiture of up to 50% of capital account, forced sale of interest at discount"] |

---

## Compliance Flags

<!-- Use the compliance agent's states: SUPPORTED DOCUMENT PROVISION / IDENTIFIED DOCUMENT GAP / PARTIALLY ADDRESSED / UNAVAILABLE. Each flag cites its authority and checked date, or names the missing authority or intake fact. Include the compliance agent's readiness (HOLD / ESCALATE / PRELIMINARY READY FOR HUMAN REVIEW); it does not set the report status. -->

- **[Flag Title]:** [Description. Example: "ERISA — UNAVAILABLE: investor mix UNKNOWN in the Regulatory Intake, so plan-asset applicability cannot be assessed. The LPA contains no plan-asset provisions (full document searched)."]

- **[Flag Title]:** [Description. Example: "Advisers Act custody (Rule 206(4)-2) — UNAVAILABLE: no source-register entry for the rule; adviser status supplied as SEC-registered."]

- **[Flag Title]:** [Description. Example: "Governing Law — Fund is governed by Delaware law but GP is a Cayman entity. Enforcement of clawback and fiduciary duty provisions across jurisdictions may be complex."]

---

## Waterfall & Economics Summary

<!-- Summarize the distribution waterfall structure, management fee economics, and key economic terms. -->

### Distribution Waterfall

| Tier | Description | Split |
|------|-------------|-------|
| 1 | Return of Capital | [100% to LPs / description] |
| 2 | Preferred Return | [Rate]% [compounding] to LPs |
| 3 | GP Catch-Up | [X]% GP / [Y]% LP until [target] |
| 4 | Carried Interest | [X]% LP / [Y]% GP |

### Key Economic Terms

| Term | Value (source locator) | Comparison | Direct effect |
|------|------------------------|------------|---------------|
| Management Fee (IP) | [X]% on [basis] ([s. X]) | [identified, dated source, otherwise "No comparable source assessed"] | [effect from the clause] |
| Management Fee (Post-IP) | [X]% on [basis] ([s. X]) | [comparison] | [effect] |
| Carry | [X]% of [stated base] ([s. X]) | [comparison] | [effect] |
| Hurdle | [X]% [method] ([s. X]) | [comparison] | [effect] |
| Clawback | [description] ([s. X]) | [comparison] | [effect] |
| Fee Offsets | [X]% ([s. X]) | [comparison] | [effect] |
| NAV-based facility | [defined? cap and basis; permitted uses; LPAC consent] ([s. X]) | [ILPA published position, 25 Jul 2024, discussion point] | [effect] |
| Continuation vehicles | [conflicts pre-cleared or LPAC review; election period] ([s. X]) | [ILPA draft guidance, June 2026 — draft, discussion point] | [effect] |
| Organizational expenses | [cap and basis; overage sharing; side-letter/MFN cost treatment] ([s. X]) | [ILPA published position, 13 May 2026, discussion point] | [effect] |

---

## Negotiation Priorities

<!-- Ranked list of the most important changes to negotiate, from most critical to least. Each gives the specific change, its direct effect and any cited source; likelihood of acceptance is "Unknown (no negotiation records)" unless records are supplied. -->

1. **[Most Important Change]** — [What to ask for with specific proposed language. Example: "Add key person provision naming [Senior Partner 1] and [Senior Partner 2]. If either ceases to devote substantially all of their business time to the fund, the investment period shall be automatically suspended until the LPAC approves a successor or votes to resume. Proposed language: 'Upon the occurrence of a Key Person Event, the Investment Period shall be immediately suspended and no new investments shall be made until the earlier of (a) the LPAC, by majority vote, resolving that the Investment Period shall resume, or (b) 180 days following such event, at which time the Investment Period shall permanently terminate.'"]

2. **[Second Most Important]** — [What to ask for. Example: "Require LPAC consent for investment period extensions. Current provision allows GP unilateral extension. Proposed: 'The General Partner may extend the Investment Period for one (1) additional year only with the affirmative vote of a majority in interest of the Limited Partners.'"]

3. **[Third Most Important]** — [What to ask for. Example: "Add carried interest escrow of 25% held until fund liquidation or third-party clawback guaranty. Proposed: 'Twenty-five percent (25%) of all Carried Interest distributions shall be deposited in an escrow account and held until the final liquidation of the Partnership, at which time such amounts shall be released or returned in accordance with the clawback provisions of Section [X].'"]

4. **[Fourth Change]** — [What to ask for]

5. **[Fifth Change]** — [What to ask for]

<!-- Continue as needed. Most LPA reviews will have 5-10 negotiation priorities. -->

---

## Recommended Next Steps

<!-- Actionable checklist. Include specific actions, not vague advice. -->

1. [ ] [e.g., "Send negotiation term sheet addressing the 5 priorities listed above to GP counsel"]
2. [ ] [e.g., "Request a revised LPA draft addressing high-risk provisions in Sections 4.1, 6.3, and 9.2"]
3. [ ] [e.g., "Add key person provision with named individuals and suspension trigger"]
4. [ ] [e.g., "Request fee calculation examples from GP to verify management fee step-down mechanics"]
5. [ ] [e.g., "Request the LP investor schedule with benefit plan status so ERISA applicability can be assessed"]
6. [ ] [e.g., "Request waterfall model from GP to verify catch-up and carry calculations"]
7. [ ] [e.g., "Compare terms to GP's prior fund LPA (Fund III vs. Fund IV)"]
8. [ ] Engage qualified fund formation counsel before executing subscription documents

---

## Status, limitations and data handling
- Report status: [PARTIAL / READY_FOR_REVIEW] — the same value as the evidence sidecar.
- Assumptions: [list, including each user-supplied intake fact]
- Limitations and checks not performed: [source-scope determination (full document / excerpt / uncertain); unavailable dimensions or agents; checks UNAVAILABLE for a missing authority, naming it; UNKNOWN / NOT PERFORMED items]
- Data handling: the packaged helpers ran locally and made no network calls; the AI host and its model provider processed the document content; connectors used: [none / list]. Confirm the source documents' confidentiality terms permit this processing.

Not financial, legal or tax advice. Qualified human review is required.

---

<!--
TEMPLATE USAGE NOTES:

1. Replace all [bracketed placeholders] with actual values from the analysis.
2. Remove any sections that are not applicable to the fund type.
3. Add additional provisions to the Provision-by-Provision Analysis as needed.
4. The Risk Dashboard counts should match the actual provisions listed.
5. Negotiation Priorities should reference specific section numbers from the LPA.
6. Protections searched for should be tailored to the fund type:
   - PE Buyout: key person, no-fault divorce, LPAC powers, carry escrow, fee offsets
   - Venture Capital: follow-on reserves, recycling limits, information rights
   - Real Estate: leverage caps, co-investment allocation, environmental liability
   - Credit: concentration limits, NAV triggers, leverage covenants
   - All fund types: NAV-based facilities, continuation-vehicle conflicts, organizational expense cap basis and side-letter/MFN cost treatment
   - Hedge Fund: gate protections, side pocket restrictions, HWM reset limitations
   - Fund of Funds: look-through reporting, underlying fund selection criteria
7. All risk levels (HIGH/MEDIUM/LOW) should be assigned consistently:
   - HIGH: Could cause significant financial loss, governance impairment, or loss of LP rights
   - MEDIUM: Could cause moderate disadvantage or create ambiguity
   - LOW: Minor issue with small improvement possible
8. Financial exposure is computed only from source figures with the packaged helper; otherwise write "Not quantified".
9. Comparisons cite an identified, dated source or an ILPA published position (discussion point); otherwise "No comparable source assessed". Comparisons never set a risk level or score.
-->
