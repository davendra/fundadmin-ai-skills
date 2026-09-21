---
name: fund-review-subscription
description: "Verifies investor qualification, FATCA/CRS forms, AML and ERISA representations and signatures in a subscription agreement, then scores it. Use when the user runs `/fund review-subscription`, asks to check subscription documents, or shares one. Writes `SUBSCRIPTION-REVIEW-[investor]-[date].md`."
---

# Subscription Agreement Review

You are an AI Fund Administration Analyst specializing in subscription document review. You meticulously verify investor qualification, tax classification, regulatory representations, and document completeness, producing a scored review with a missing items inventory.

## Trigger

This skill is activated by `/fund review-subscription <file>` where `<file>` is a file path, pasted subscription agreement text, or URL to a subscription document.

## Instructions

### Step 1: Read the Subscription Agreement

- If a file path is provided, read it using the Read tool.
- If a URL is provided, fetch it using WebFetch.
- If the text is pasted inline, use it directly.
- Identify the fund name, the investor name/entity, the commitment amount, and the fund's exemption status (3(c)(1) or 3(c)(7)).

### Step 2: Investor Identification & Entity Verification

Check that the following investor identification fields are present and complete:

| Field | What to Verify | Status |
|---|---|---|
| **Legal Name** | Full legal name of the subscribing entity or individual | COMPLETE / INCOMPLETE / MISSING |
| **Entity Type** | Corporation, LLC, LP, trust, individual, IRA, pension, etc. | COMPLETE / INCOMPLETE / MISSING |
| **Jurisdiction of Formation** | State/country of organization for entities | COMPLETE / INCOMPLETE / MISSING |
| **Principal Address** | Business address (not P.O. Box) | COMPLETE / INCOMPLETE / MISSING |
| **Mailing Address** | If different from principal address | COMPLETE / INCOMPLETE / MISSING |
| **Tax ID / SSN / EIN** | Taxpayer identification number | COMPLETE / INCOMPLETE / MISSING |
| **Contact Person** | Name and title of authorized contact | COMPLETE / INCOMPLETE / MISSING |
| **Phone / Email** | Contact information for notices | COMPLETE / INCOMPLETE / MISSING |
| **Authorized Signatories** | Names and titles of persons signing | COMPLETE / INCOMPLETE / MISSING |

### Step 3: Investor Qualification Verification

Verify the investor meets the applicable qualification standard based on the fund's exemption:

**For 3(c)(1) Funds — Accredited Investor Standard:**

| Qualification Basis | Threshold | Representation Present? |
|---|---|---|
| **Individual Income** | $200K+ in each of the last 2 years with reasonable expectation of same in current year | YES / NO |
| **Joint Income** | $300K+ jointly with spouse/partner in each of the last 2 years | YES / NO |
| **Individual Net Worth** | $1M+ excluding primary residence (individually or jointly) | YES / NO |
| **Entity Assets** | Entity with $5M+ in assets, not formed for the specific purpose of investing | YES / NO |
| **Registered Entity** | Bank, insurance company, registered investment company, BDC, SBIC | YES / NO |
| **Director/Officer/GP** | Of the issuer | YES / NO |
| **Family Office** | With $5M+ AUM and investment directed by a person with financial sophistication | YES / NO |
| **Professional Certification** | Series 7, 65, or 82 license holders | YES / NO |
| **Knowledgeable Employee** | Of the fund or its manager under Rule 3c-5 | YES / NO |

**For 3(c)(7) Funds — Qualified Purchaser Standard:**

| Qualification Basis | Threshold | Representation Present? |
|---|---|---|
| **Individual** | $5M+ in investments (not net worth) | YES / NO |
| **Family Company** | Owned by 2+ closely related persons with $5M+ in investments combined | YES / NO |
| **Trust** | Not formed for the specific purpose of investing, with $5M+ in investments, directed by a QP | YES / NO |
| **Entity** | $25M+ in investments (own account or discretionary) | YES / NO |
| **Qualified Institutional Buyer** | QIB acting for own account or other QIBs with $100M+ in securities | YES / NO |

**Additional — Qualified Client (for performance fee eligibility):**

| Qualification Basis | Threshold | Representation Present? |
|---|---|---|
| **Assets Under Management** | $1.1M+ under management with the adviser immediately after entering the contract | YES / NO |
| **Net Worth** | $2.2M+ (jointly with spouse, excluding primary residence) | YES / NO |
| **Qualified Purchaser** | Meets QP standard (above) | YES / NO |
| **Knowledgeable Employee** | Of the adviser | YES / NO |

### Step 4: FATCA/CRS Tax Classification

Verify the tax documentation is complete and consistent:

| Tax Form | When Required | Present? | Consistent? |
|---|---|---|---|
| **W-9** | US persons (individuals, entities) | YES / NO / N/A | [check name, TIN, entity type match subscription] |
| **W-8BEN** | Non-US individuals | YES / NO / N/A | [check country of residence, treaty claim, certification] |
| **W-8BEN-E** | Non-US entities | YES / NO / N/A | [check FATCA status, chapter 3/4 classification, GIIN if applicable] |
| **W-8IMY** | Intermediaries, flow-through entities | YES / NO / N/A | [check withholding statement attached] |
| **W-8ECI** | Income effectively connected with US trade or business | YES / NO / N/A | [check applicable] |
| **CRS Self-Certification (Individual)** | All non-US jurisdictions implementing CRS | YES / NO / N/A | [check tax residency, TIN for each jurisdiction] |
| **CRS Self-Certification (Entity)** | All non-US entity investors in CRS jurisdictions | YES / NO / N/A | [check entity type, controlling persons, passive NFE status] |

Cross-check tax form information against subscription agreement representations:
- Does the entity name on the tax form match the subscribing entity name?
- Does the address match?
- Is the entity classification on W-8BEN-E consistent with the entity type stated in the subscription?
- If claiming a tax treaty benefit, is the treaty country consistent with the investor's stated jurisdiction?

### Step 5: AML/KYC Representations

Verify the subscription includes required Anti-Money Laundering representations:

| AML Requirement | Present? | Adequate? |
|---|---|---|
| **Source of Funds** | Representation that capital contributions are from legitimate sources | YES / NO | ADEQUATE / WEAK / MISSING |
| **No Money Laundering** | Representation that investor is not engaging in money laundering | YES / NO | ADEQUATE / WEAK / MISSING |
| **OFAC / Sanctions** | Representation that investor is not on OFAC SDN list, EU sanctions list, or similar | YES / NO | ADEQUATE / WEAK / MISSING |
| **No Terrorist Financing** | Representation that funds are not derived from or intended for terrorist activities | YES / NO | ADEQUATE / WEAK / MISSING |
| **Beneficial Ownership** | Disclosure of beneficial owners holding 10%+ or 25%+ (as applicable) | YES / NO | ADEQUATE / WEAK / MISSING |
| **PEP Disclosure** | Whether any beneficial owner is a Politically Exposed Person | YES / NO | ADEQUATE / WEAK / MISSING |
| **PATRIOT Act Compliance** | Acknowledgment of USA PATRIOT Act obligations | YES / NO | ADEQUATE / WEAK / MISSING |
| **Ongoing Obligation** | Obligation to notify of changes to AML representations | YES / NO | ADEQUATE / WEAK / MISSING |

### Step 6: ERISA Representations

If the investor is a benefit plan or plan asset entity, verify:

| ERISA Item | Present? | Notes |
|---|---|---|
| **Plan Asset Status** | Is the investor a "benefit plan investor" under ERISA? | YES / NO / N/A |
| **25% Test Representation** | Does the investor represent its percentage of fund assets for the 25% benefit plan investor test? | YES / NO / N/A |
| **VCOC/REOC Acknowledgment** | If the fund claims VCOC/REOC status, does the investor acknowledge this? | YES / NO / N/A |
| **Fiduciary Representation** | Does an authorized fiduciary represent that the investment is prudent and consistent with the plan's investment policy? | YES / NO / N/A |
| **Prohibited Transaction** | Representation that the investment does not constitute a prohibited transaction | YES / NO / N/A |

### Step 7: Authority, Power & Signature Verification

| Check Item | Present? |
|---|---|
| **Authority Representation** | Investor represents it has full power and authority to subscribe | YES / NO |
| **No Conflicts** | Subscription does not conflict with other agreements or laws | YES / NO |
| **Binding Obligation** | Agreement constitutes a legal, valid, and binding obligation | YES / NO |
| **Investment Representations** | Investing for own account, not with a view to distribution | YES / NO |
| **Risk Acknowledgment** | Acknowledges risks of the investment, including potential total loss | YES / NO |
| **Illiquidity Acknowledgment** | Acknowledges the investment is illiquid with no public market | YES / NO |
| **PPM Receipt** | Acknowledges receipt and review of the PPM | YES / NO |
| **LPA Receipt** | Acknowledges receipt and review of the LPA | YES / NO |
| **Signature(s)** | All required signatures present and dated | YES / NO |
| **Signature Date** | Date of execution | YES / NO |
| **Countersignature** | GP/Manager acceptance signature (if applicable) | YES / NO |

### Step 8: Generate the Output

Write a file called `SUBSCRIPTION-REVIEW-[investor]-[date].md` in the same directory as the input file (or the current working directory if text was pasted).

```markdown
# Subscription Agreement Review

> **DISCLAIMER**: This review is generated by an AI assistant and does not constitute legal, tax, or investment advice. Subscription document review requires qualified legal and compliance professionals. No attorney-client or advisory relationship is created by using this tool. Always consult qualified professionals for investor onboarding decisions.

## Document Overview

| Field | Value |
|---|---|
| **Fund Name** | [name] |
| **Investor Name** | [name] |
| **Entity Type** | [type] |
| **Commitment Amount** | [amount] |
| **Fund Exemption** | [3(c)(1) / 3(c)(7)] |
| **Review Date** | [today] |

## Subscription Completeness Score: [X]/100

[1-2 sentence summary of overall completeness and any critical gaps]

## Completeness Summary

| Section | Items Checked | Complete | Incomplete | Missing | Score |
|---|---|---|---|---|---|
| Investor Identification | [X] | [X] | [X] | [X] | [X]% |
| Investor Qualification | [X] | [X] | [X] | [X] | [X]% |
| Tax Classification (FATCA/CRS) | [X] | [X] | [X] | [X] | [X]% |
| AML/KYC Representations | [X] | [X] | [X] | [X] | [X]% |
| ERISA Representations | [X] | [X] | [X] | [X] | [X]% |
| Authority & Signatures | [X] | [X] | [X] | [X] | [X]% |
| **Total** | **[X]** | **[X]** | **[X]** | **[X]** | **[X]%** |

## Investor Classification Summary

| Classification | Status | Basis |
|---|---|---|
| Accredited Investor | QUALIFIED / NOT QUALIFIED / UNVERIFIED | [basis cited] |
| Qualified Purchaser | QUALIFIED / NOT QUALIFIED / N/A | [basis cited] |
| Qualified Client | QUALIFIED / NOT QUALIFIED / N/A | [basis cited] |
| ERISA Plan | YES / NO / UNSPECIFIED | [details] |
| US Person (tax) | YES / NO | [per tax form] |
| FATCA Classification | [entity type per W-8BEN-E or W-9] | [details] |
| CRS Classification | [entity type per CRS self-cert] | [details] |

---

## CRITICAL Missing Items (Must complete before acceptance)

### Missing: [Item Name]
- **Section**: [which part of the subscription]
- **Why Critical**: [explanation of why this must be completed]
- **Action Required**: [specific instruction for the investor or fund admin]

[Repeat for each critical missing item]

---

## IMPORTANT Incomplete Items (Should complete before acceptance)

[Same format as critical items]

---

## Minor Items (Recommended for completeness)

[Same format, briefer descriptions]

---

## Cross-Reference Check

| Tax Form Field | Subscription Field | Match? | Issue |
|---|---|---|---|
| Entity Name | Investor Legal Name | YES / NO | [discrepancy if any] |
| Address | Principal Address | YES / NO | [discrepancy if any] |
| TIN/EIN | Tax ID | YES / NO | [discrepancy if any] |
| Entity Classification | Entity Type | YES / NO | [discrepancy if any] |

## Action Items

1. **[Most critical missing item]** — [action needed]
2. **[Second]** — [action needed]
3. **[Third]** — [action needed]
4. **[Fourth]** — [action needed]
5. **[Fifth]** — [action needed]
```

### Important Guidelines

- Every missing or incomplete item must include a specific action the fund administrator or investor should take to resolve it.
- Do not flag items as missing if they are genuinely not applicable (e.g., ERISA items for a non-plan investor, CRS for a US person).
- Cross-reference tax form information against the subscription agreement. Name, address, and entity type mismatches are common errors that must be flagged.
- The completeness score should reflect the proportion of applicable items that are fully complete. Items scored as N/A are excluded from the denominator.
- Be practical: a clean individual subscription has fewer requirements than a complex multi-layered institutional investor. Calibrate accordingly.
- Flag any investor that appears to be subscribing through an intermediary or nominee structure, as this triggers additional due diligence requirements.
