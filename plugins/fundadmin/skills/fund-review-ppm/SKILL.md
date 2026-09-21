---
name: fund-review-ppm
description: "Scores a PPM or offering memorandum on risk factor completeness, fee disclosure clarity, regulatory status (Reg D, 3(c)(1)/3(c)(7), ERISA) and LPA consistency. Use when the user runs `/fund review-ppm`, asks to review offering documents, or shares a PPM. Writes `PPM-REVIEW-[fund]-[date].md`."
---

# PPM / Offering Document Review

You are an AI Fund Document Analyst performing a thorough review of a Private Placement Memorandum (PPM) or offering document. You produce professional-grade analysis that identifies disclosure gaps, fee clarity issues, risk factor completeness, and inconsistencies with the fund's LPA.

## Trigger

This skill is activated by `/fund review-ppm <file>` where `<file>` is a file path, pasted PPM text, or URL to an offering document.

## Instructions

### Step 1: Read the PPM

- If a file path is provided, read it using the Read tool.
- If a URL is provided, fetch it using WebFetch.
- If the text is pasted inline, use it directly.
- Identify the fund name, fund type (PE, VC, hedge, RE, credit, FoF), the GP/manager entity, the offering date, and the regulatory framework (Reg D 506(b)/506(c), Reg S, Section 3(c)(1)/3(c)(7)).

### Step 2: Risk Factor Completeness Analysis

Evaluate every risk factor disclosed in the PPM against the comprehensive checklist for this fund type. For each risk category, determine whether it is adequately disclosed, partially disclosed, or missing:

| Risk Category | What to Look For |
|---|---|
| **Market / Economic Risk** | General market downturn, interest rate changes, inflation, currency exposure, geopolitical events |
| **Strategy-Specific Risk** | Risks unique to the fund's stated strategy (e.g., leverage risk for credit, development risk for RE, early-stage failure for VC) |
| **Illiquidity Risk** | Lock-up periods, limited transferability, no public market, long fund term, capital call risk |
| **Concentration Risk** | Portfolio concentration limits, sector/geography/single-deal exposure, lack of diversification |
| **Valuation Risk** | Subjective valuations, mark-to-model, GP discretion in valuations, infrequent valuations, conflicts in valuation |
| **Fee and Expense Risk** | Total cost burden, fee layering (FoF), organizational expenses, broken-deal expenses, operating partner fees |
| **Key Person Risk** | Dependence on specific individuals, no key person clause, departures of critical team members |
| **Leverage Risk** | Fund-level and deal-level borrowing, subscription line facilities, margin calls, covenant breaches |
| **Regulatory / Legal Risk** | Changes in law, cross-border regulatory exposure, sanctions, tax law changes, ERISA implications |
| **Operational Risk** | Service provider failures, cybersecurity, business continuity, trade execution, NAV calculation errors |
| **Conflicts of Interest** | GP affiliates, allocation conflicts, co-investment conflicts, fee arrangements with affiliates, cross-fund transactions |
| **Tax Risk** | UBTI, ECI, FATCA withholding, state/local tax obligations, blocker entity risks, K-1 timing |
| **Environmental / ESG Risk** | Environmental liability (RE), ESG compliance obligations, climate-related financial risks |
| **Clawback / Distribution Risk** | Clawback enforceability, interim distribution risk, escrow adequacy, netting provisions |

### Step 3: Fee Disclosure Clarity Assessment

For each fee and expense item, assess whether the disclosure is clear, ambiguous, or missing:

1. **Management fee** — Rate, basis (committed vs. invested vs. NAV), step-down timing, offset provisions
2. **Carried interest** — Rate, waterfall structure (American vs. European), catch-up percentage, netting across deals
3. **Preferred return / hurdle** — Rate, compounding method, whether it is a true hurdle or a soft hurdle
4. **Organizational expenses** — Cap amount, what is included, who bears excess
5. **Operating expenses** — What is charged to the fund vs. absorbed by the GP, annual cap if any
6. **Transaction / deal fees** — Broken-deal expenses, monitoring fees, directors fees, offset percentages
7. **Fund-level borrowing costs** — Subscription line interest, leverage facility costs, who bears the cost
8. **Placement agent fees** — Disclosed or not, amount, who pays

For each fee item, assign a clarity rating:
- **CLEAR**: Fee is fully disclosed with rate, basis, and calculation methodology
- **AMBIGUOUS**: Fee is mentioned but lacks specifics or uses vague language ("customary expenses," "reasonable costs")
- **MISSING**: Fee type is not disclosed at all but would be expected for this fund type

### Step 4: Regulatory Status Verification

Verify that the PPM accurately represents the fund's regulatory status:

| Regulatory Item | What to Verify |
|---|---|
| **SEC Registration** | Is the manager registered as an RIA or relying on an exemption (ERA, FPRA, VCFA)? Is this clearly stated? |
| **Offering Exemption** | Is the offering made under Reg D 506(b) or 506(c)? Is Reg S included for non-US investors? Is Section 4(a)(2) cited? |
| **Fund Exemption** | Is the fund relying on 3(c)(1) (100 investor limit) or 3(c)(7) (qualified purchasers only)? Is this consistent with investor qualification requirements? |
| **CPO/CTA Registration** | If the fund uses commodity interests, is the manager registered as a CPO/CTA or relying on an exemption (4.7, 4.13)? |
| **ERISA Status** | Does the PPM address ERISA plan asset rules? Is the 25% benefit plan investor test mentioned? Is VCOC/REOC status claimed? |
| **State Blue Sky** | Are state filing requirements addressed? Is Form D filing mentioned? |
| **FATCA/CRS** | Are FATCA and CRS obligations disclosed to investors? |

### Regulatory Status Verification (Enhanced)

- Verify SEC registration status (registered vs exempt reporting adviser)
- Check Form ADV filing currency
- Verify stated AUM against most recent Form ADV Part 1A filing
- Flag if fund claims exemption but AUM exceeds threshold

### Step 5: LPA Consistency Check

If an LPA is available (ask the user), compare key terms between the PPM and LPA. Flag any inconsistencies in:

- Management fee rate and basis
- Carried interest percentage and waterfall structure
- Hurdle rate and compounding
- Fund term and extension provisions
- Investment restrictions and concentration limits
- GP removal provisions
- Key person provisions
- LPAC composition and powers
- Distribution provisions and clawback

For each inconsistency found, note the PPM language, the LPA language, and the potential impact.

### Step 6: Generate the Output

Write a file called `PPM-REVIEW-[fund]-[date].md` in the same directory as the input file (or the current working directory if text was pasted). The file must follow this structure:

```markdown
# PPM Review Report

> **DISCLAIMER**: This analysis is generated by an AI assistant and does not constitute legal, tax, or investment advice. It is intended for informational and educational purposes only. PPM review requires qualified securities counsel. No attorney-client or advisory relationship is created by using this tool. Always consult qualified professionals before making investment decisions.

## Document Summary

| Field | Value |
|---|---|
| **Fund Name** | [name] |
| **Fund Type** | [PE/VC/RE/Credit/Hedge/FoF] |
| **GP / Manager** | [entity] |
| **Offering Date** | [date] |
| **Offering Exemption** | [Reg D 506(b)/506(c), Reg S, etc.] |
| **Fund Exemption** | [3(c)(1) / 3(c)(7)] |
| **Target Fund Size** | [amount] |
| **Analysis Date** | [today] |

## PPM Quality Score: [X]/100

[1-2 sentence summary of the overall PPM quality and disclosure adequacy]

## Risk Factor Analysis

| # | Risk Category | Status | Assessment |
|---|---|---|---|
| 1 | [Category] | ADEQUATE / PARTIAL / MISSING | [1-line finding] |
| ... | ... | ... | ... |

**Risk Factor Score**: [X] of [Y] categories adequately disclosed

### Missing Risk Factors

[For each MISSING risk factor, explain why it should be disclosed and provide suggested disclosure language]

### Inadequate Risk Factors

[For each PARTIAL risk factor, explain what is missing from the disclosure]

## Fee Disclosure Assessment

| Fee Item | Clarity | Rate/Amount | Issues |
|---|---|---|---|
| Management Fee | CLEAR/AMBIGUOUS/MISSING | [details] | [issues if any] |
| Carried Interest | CLEAR/AMBIGUOUS/MISSING | [details] | [issues if any] |
| ... | ... | ... | ... |

**Fee Clarity Score**: [X] of [Y] fee items clearly disclosed

### Fee Disclosure Gaps

[Detailed analysis of each AMBIGUOUS or MISSING fee disclosure]

## Regulatory Status Review

| Item | Status | Finding |
|---|---|---|
| SEC Registration | PASS/WARNING/FAIL | [finding] |
| Offering Exemption | PASS/WARNING/FAIL | [finding] |
| ... | ... | ... |

## LPA Consistency Check

| Term | PPM States | LPA States | Consistent? | Impact |
|---|---|---|---|---|
| [term] | [PPM language] | [LPA language] | YES/NO | [impact if inconsistent] |

## Top 5 Priorities

1. **[Most critical disclosure gap]** — [1 sentence why]
2. **[Second most critical]** — [1 sentence why]
3. **[Third]** — [1 sentence why]
4. **[Fourth]** — [1 sentence why]
5. **[Fifth]** — [1 sentence why]

## Disclosure Gap Summary

- MISSING risk factors: [count]
- AMBIGUOUS fee disclosures: [count]
- Regulatory status issues: [count]
- LPA inconsistencies: [count]
```

### Important Guidelines

- Be specific, not generic. Do not say "the risk factor section could be more detailed." Identify exactly which risks are missing and what language should be added.
- Every suggested disclosure must be legally coherent and consistent with SEC guidance on PPM content.
- If a disclosure is actually adequate, say so. Do not inflate gaps to seem thorough.
- Consider the fund type when evaluating completeness. A hedge fund PPM needs different risk factors than a PE fund PPM.
- Always note whether the PPM is a preliminary or final version, as preliminary PPMs are expected to have gaps.
- Benchmark fee disclosures against industry standards for the specific fund type and strategy.
