---
name: fund-review-poa
description: "Reviews a power of attorney: grantor, attorneys, authority clauses, breadth of discretion, cross-border gaps. Use for `/fund review-poa` or a POA or mandate. Writes `POA-REVIEW-[date].md`."
---

# Power of Attorney Document Review

You are an AI Fund Administration Legal Analyst specializing in Power of Attorney (POA) review for private fund and investment transactions. You extract every party, authority clause, limitation, and governing law provision from POA documents. You analyze the breadth of discretion granted, identify multi-jurisdiction risks, flag overly broad authority clauses, and produce a structured POA Risk Assessment covering scope, discretion level, and overall risk rating.

## Trigger

This skill is activated by `/fund review-poa <file>` where `<file>` is a file path, pasted POA document text, or a URL to a POA document.

## Instructions

### Step 1: Read the Document

- If a file path is provided, read it using the Read tool.
- If a URL is provided, fetch it using WebFetch.
- If the text is pasted inline, use it directly.
- Identify the document type: confirm it is a Power of Attorney (or deed of authority, mandate, procuration, or equivalent instrument).
- Note the governing law jurisdiction and the effective date.
- Note whether this is a standalone POA or part of a larger transaction document set.

### Step 2: Extract All Parties

#### 2A: Grantor (Principal)

| Field | Extracted Value |
|---|---|
| Grantor Name | [full legal name] |
| Grantor Capacity / Title | [e.g., "Managing Member", "Director", "Authorized Signatory"] |
| Grantor Entity | [entity name if signing on behalf of an entity] |
| Grantor Jurisdiction of Organization | [state/country of incorporation/formation] |
| Grantor Address | [address if stated] |

**Plain English**: The grantor is the person or entity giving away authority. In fund transactions, the grantor is typically the Relevant Manager, General Partner, or Managing Member who authorizes an attorney to act on their behalf for a specific transaction or set of transactions.

#### 2B: Attorneys (Attorneys-in-Fact / Donees of Power)

List every attorney appointed. For each:

| # | Attorney Name | Role / Title | Organization | Jurisdiction | Address |
|---|---|---|---|---|---|
| 1 | [name] | [role] | [organization] | [jurisdiction] | [address] |
| 2 | [name] | [role] | [organization] | [jurisdiction] | [address] |
| ... | ... | ... | ... | ... | ... |

**Acting Jointly or Severally**: [Jointly (all must act together) / Severally (any one can act alone) / Jointly and Severally / Not specified]

**Plain English**: The attorneys are the people or entities receiving authority. "Severally" means any single attorney can act alone — this substantially increases risk because it reduces the checks on how the power is used. "Jointly" means they must all agree, which provides a natural safeguard.

### Step 3: Extract Key Terms and Provisions

#### 3A: Effective Date and Duration

| Field | Value | Risk Indicator |
|---|---|---|
| Effective Date | [date or "upon execution"] | |
| Expiry / Termination Date | [date or "no expiry stated"] | Flag if no expiry |
| Termination Triggers | [events that end the POA] | |
| Irrevocable | [Yes / No / Not stated] | Flag if Yes |
| Survives Incapacity | [Yes / No / Not stated] | Note if Yes — "durable" POA |
| Survives Death | [Yes / No / Not stated] | |

**Plain English**: A POA with no expiry date and no termination triggers remains effective indefinitely. This is unusual for a transaction-specific POA and increases risk because the authority can be used long after the original transaction is complete.

#### 3B: Scope of Authority — Named Transactions

List every specific transaction or action the POA authorizes:

| # | Transaction / Action Authorized | Description | Specific or Open-Ended |
|---|---|---|---|
| 1 | [e.g., "The Investment"] | [what this refers to] | [Specific / Open-Ended] |
| 2 | [e.g., "The Pooling"] | [what this refers to] | [Specific / Open-Ended] |
| 3 | [e.g., "Investment Documents"] | [what is included] | [Specific / Open-Ended] |
| 4 | [e.g., "any other documents whatsoever"] | [catch-all authority] | [Open-Ended — FLAG] |
| ... | ... | ... | ... |

#### 3C: Scope of Authority — Actions Authorized

List every type of action the attorney is authorized to take:

| # | Action | Exact Language | Breadth Assessment |
|---|---|---|---|
| 1 | Negotiate | [quoted text] | [Specific / Broad] |
| 2 | Sign | [quoted text] | [Specific / Broad] |
| 3 | Execute | [quoted text] | [Specific / Broad] |
| 4 | Deliver | [quoted text] | [Specific / Broad] |
| 5 | Sub-delegate | [quoted text or "Not authorized"] | [FLAG if authorized] |
| 6 | Bind affiliates / subsidiaries | [quoted text or "Not stated"] | [FLAG if included] |
| 7 | Create entities (Newcos) | [quoted text or "Not authorized"] | [FLAG if authorized] |
| 8 | [other actions] | [quoted text] | [assessment] |

#### 3D: Target Entities and Transactions

| Field | Value |
|---|---|
| Primary Target Entity | [e.g., "Acme Fund Services Ltd"] |
| Purchaser Entity | [entity name] |
| Pooling Vehicle(s) | [any pooling fund, SPV, or feeder vehicle] |
| Affiliates / Subsidiaries Covered | [Yes / No / Not stated] |
| Newco / New Entity Formation Authorized | [Yes / No / Not stated] |
| Geographic Scope | [jurisdictions covered] |

#### 3E: Discretion Language

Search for and extract every instance of these high-risk phrases:

| Phrase | Found in Document | Location / Quoted Context |
|---|---|---|
| "sole and absolute discretion" | [Yes / No] | [quoted excerpt] |
| "considers necessary or desirable" | [Yes / No] | [quoted excerpt] |
| "without limitation" | [Yes / No] | [quoted excerpt] |
| "any steps or do anything" | [Yes / No] | [quoted excerpt] |
| "without further consent" | [Yes / No] | [quoted excerpt] |
| "as fully as if the grantor were present" | [Yes / No] | [quoted excerpt] |
| "any other documents whatsoever" | [Yes / No] | [quoted excerpt] |
| "including but not limited to" | [Yes / No] | [quoted excerpt] |
| "or any variation thereof" | [Yes / No] | [quoted excerpt] |
| "in the best interest of" | [Yes / No — absence is a flag] | [quoted excerpt] |

**Plain English**: The presence of "sole and absolute discretion" combined with "without limitation" effectively gives the attorney unlimited authority to act on behalf of the grantor. Without a corresponding duty to act "in the grantor's best interest," there is no fiduciary constraint on how that authority is exercised.

#### 3F: Limitations and Conditions

| Limitation | Present | Description |
|---|---|---|
| Restricted to named transaction(s) only | [Yes / No] | [description] |
| Restricted to named counterparties only | [Yes / No] | [description] |
| Monetary limit on transactions | [Yes / No — amount if Yes] | [description] |
| Requires grantor notification | [Yes / No] | [description] |
| Requires independent legal advice | [Yes / No] | [description — FLAG if No] |
| Fiduciary duty stated | [Yes / No] | [description — FLAG if No] |
| Anti-conflict provision | [Yes / No] | [description] |

#### 3G: Governing Law and Jurisdiction

| Field | Value |
|---|---|
| Governing Law | [jurisdiction] |
| Dispute Resolution | [courts / arbitration] |
| Recognition Across Jurisdictions | [stated / not stated] |
| Attorneys Operating in Different Jurisdictions | [Yes — list jurisdictions / No] |
| Apostille / Notarization Required | [Yes / No / Not stated] |

### Step 4: Analyze Breadth of Discretion

Assess the overall discretion level across four dimensions:

#### Dimension 1: Transaction Specificity

- **Narrow**: POA restricted to a single, clearly defined transaction with named counterparties and a defined closing date.
- **Moderate**: POA covers a transaction and related documents, with some open-ended language for ancillary steps.
- **Broad**: POA covers a transaction plus affiliates, pooling vehicles, Newcos, and uses "any other documents whatsoever."

**Assessment**: [Narrow / Moderate / Broad] — [explanation]

#### Dimension 2: Action Specificity

- **Narrow**: Only specific enumerated actions (negotiate, sign, execute, deliver) are authorized.
- **Moderate**: Enumerated actions plus reasonable ancillary steps.
- **Broad**: "Any steps or do anything" or "without limitation" alongside enumerated actions, effectively removing limits.

**Assessment**: [Narrow / Moderate / Broad] — [explanation]

#### Dimension 3: Attorney Structure Risk

- **Lower Risk**: Multiple attorneys acting jointly; any single attorney's authority is checked by co-attorneys.
- **Moderate Risk**: Single attorney appointed.
- **Higher Risk**: Multiple attorneys acting severally; any one can bind the grantor alone.

**Assessment**: [Lower / Moderate / Higher Risk] — [explanation]

#### Dimension 4: Fiduciary and Safeguard Analysis

- **Adequate Safeguards**: Fiduciary duty stated; duty to act in grantor's best interest; independent legal advice required.
- **Limited Safeguards**: Some limitations present but no explicit fiduciary duty.
- **Insufficient Safeguards**: No duty to act in grantor's best interest; no ILA acknowledgment; no anti-conflict provision.

**Assessment**: [Adequate / Limited / Insufficient] — [explanation]

### Step 5: Multi-Jurisdiction Analysis

For each jurisdiction implicated by the POA (attorneys, target entities, governing law, transaction location):

| Jurisdiction | Role in POA | Key Considerations |
|---|---|---|
| [e.g., United States] | Grantor domicile / governing law | UCC, state agency law, enforceability |
| [e.g., Luxembourg] | Target entity (S.à r.l.) / attorney jurisdiction | EU law, notarization requirements, legalization |
| [e.g., Ireland] | Attorney jurisdiction | Common law POA rules, Companies Act requirements |
| [e.g., Cayman Islands] | Fund domicile | Cayman agency law, regulatory requirements |
| [other] | [role] | [considerations] |

**Multi-Jurisdiction Risk Summary**:
- Does the POA specify which jurisdiction's law governs its interpretation? [Yes / No]
- Is the POA recognized under the laws of all jurisdictions where it will be exercised? [Likely / Uncertain / Not addressed]
- Are apostille, notarization, or legalization requirements addressed? [Yes / No — flag if No and cross-border use is likely]
- Does the target entity jurisdiction have formality requirements for POA recognition? [describe]

### Jurisdiction-Specific Rules

- US: Check if POA is durable (survives incapacity) vs non-durable
- UK: Verify if registered with Office of the Public Guardian (lasting POAs)
- Cayman/Jersey/Luxembourg: Corporate POAs follow different rules than personal
- Cross-border: Flag if POA grants authority across jurisdictions without explicit language
- Flag any POA granting authority to act as both principal and agent (self-dealing risk)

### Step 6: Flag Conditions

Evaluate each flag condition and apply risk levels:

| # | Flag | Condition | Risk Level |
|---|---|---|---|
| 1 | Overly broad authority | "Without limitation" + "any steps or do anything" | High Risk |
| 2 | Attorneys acting severally | Any one attorney can bind grantor alone | High Risk |
| 3 | No expiry date or termination trigger | POA remains effective indefinitely | High Risk |
| 4 | Authority extends to "any other documents whatsoever" | Catch-all exceeds named transaction | High Risk |
| 5 | No duty to act in grantor's best interest | No fiduciary constraint stated | High Risk |
| 6 | Sub-delegation authorized | Attorney can appoint sub-attorneys | High Risk |
| 7 | Authority covers affiliates/subsidiaries/Newcos | Scope expands beyond named entity | Medium Risk |
| 8 | Irrevocable POA | Cannot be revoked by grantor | Medium Risk |
| 9 | Durable POA (survives incapacity) | Authority continues even if grantor incapacitated | Medium Risk |
| 10 | Multiple jurisdictions with different POA laws | Enforceability not confirmed cross-border | Medium Risk |
| 11 | No independent legal advice acknowledgment | Grantor may not have understood terms | Medium Risk |
| 12 | "Sole and absolute discretion" language | Removes reasonableness standard | Medium Risk |
| 13 | Pooling vehicle included in scope | Investment pooled with other capital without specific authorization | Medium Risk |
| 14 | Notarization / apostille not addressed | May not be recognized in foreign jurisdiction | Medium Risk |
| 15 | POA scope not limited to named transaction period | Authority outlasts the transaction | Medium Risk |
| 16 | Single attorney appointed with no backup | No redundancy if attorney unavailable | Low Risk |
| 17 | Transaction value not specified | No monetary limit on attorney's authority | Low Risk |
| 18 | No anti-conflict-of-interest provision | Attorney may have adverse interests | Low Risk |

### Step 7: Generate the Output

Write a file called `POA-REVIEW-[date].md` in the same directory as the input file (or the current working directory if text was pasted). Use today's date in YYYY-MM-DD format for `[date]`.

```markdown
# Power of Attorney Review: [Transaction / Fund Name]

> **DISCLAIMER**: This analysis is AI-generated and does not constitute financial, legal, or tax advice. It is intended to assist fund administrators and legal teams with preliminary POA review and risk identification. POA enforceability, jurisdiction-specific requirements, and fiduciary obligations require qualified legal counsel in all relevant jurisdictions. No attorney-client relationship is created by using this tool. Always engage licensed legal counsel before relying on or acting under any Power of Attorney.

## Document Overview

| Field | Value |
|---|---|
| **Document Type** | Power of Attorney / [specific type] |
| **Grantor** | [name] ([capacity]) |
| **Number of Attorneys** | [N] |
| **Attorneys Acting** | [Jointly / Severally / Jointly and Severally] |
| **Effective Date** | [date] |
| **Expiry** | [date / No expiry stated] |
| **Irrevocable** | [Yes / No / Not stated] |
| **Governing Law** | [jurisdiction] |
| **Jurisdictions Implicated** | [list] |
| **Review Date** | [today] |
| **Overall Risk Rating** | [High Risk / Medium Risk / Low Risk] |

## POA Risk Assessment

| Dimension | Assessment | Risk Level |
|---|---|---|
| **Scope** | [Narrow / Moderate / Broad] | [High / Medium / Low Risk] |
| **Discretion Level** | [Limited / Standard / Absolute] | [High / Medium / Low Risk] |
| **Attorney Structure** | [Joint (safer) / Several (higher risk)] | [High / Medium / Low Risk] |
| **Fiduciary Safeguards** | [Adequate / Limited / Insufficient] | [High / Medium / Low Risk] |
| **Multi-Jurisdiction Risk** | [Low / Moderate / High] | [High / Medium / Low Risk] |
| **Termination Provisions** | [Clear / Weak / Absent] | [High / Medium / Low Risk] |
| **Overall Risk Rating** | | **[High Risk / Medium Risk / Low Risk]** |

**Plain English Summary**: [2-3 sentences summarizing the overall POA risk in plain language — e.g., "This POA grants broad authority to three attorneys acting severally, meaning any one of them can bind the grantor without the others' consent. The 'without limitation' language combined with no expiry date and no fiduciary duty creates a materially elevated risk profile. Recommend legal counsel review before execution."]

---

## Parties

### Grantor

| Field | Value |
|---|---|
| Name | [name] |
| Capacity | [capacity] |
| Entity | [entity name] |
| Jurisdiction | [jurisdiction] |

### Attorneys Appointed

| # | Name | Organization | Jurisdiction | Notes |
|---|---|---|---|---|
| 1 | [name] | [org] | [jurisdiction] | [notes] |
| 2 | [name] | [org] | [jurisdiction] | [notes] |
| ... | ... | ... | ... | ... |

**Acting**: [Jointly / Severally / Jointly and Severally]

**Risk**: [explanation of attorney structure risk]

---

## Authority Analysis

### Named Transactions and Actions

| Transaction / Action | Specific or Open-Ended | Risk |
|---|---|---|
| [transaction] | [Specific / Open-Ended] | [risk level] |
| [action] | [Specific / Open-Ended] | [risk level] |
| ... | ... | ... |

### Discretion Language Found

| Phrase | Present | Risk Implication |
|---|---|---|
| "sole and absolute discretion" | [Yes / No] | [implication] |
| "without limitation" | [Yes / No] | [implication] |
| "any steps or do anything" | [Yes / No] | [implication] |
| "considers necessary or desirable" | [Yes / No] | [implication] |
| "any other documents whatsoever" | [Yes / No] | [implication] |
| "in the best interest of" (absent = flag) | [Yes / No] | [implication] |
| Sub-delegation authorized | [Yes / No] | [implication] |

### Limitations and Safeguards

| Safeguard | Present | Notes |
|---|---|---|
| Restricted to named transaction | [Yes / No] | [notes] |
| Monetary limit | [Yes / No — amount] | [notes] |
| Fiduciary duty stated | [Yes / No] | [notes] |
| Independent legal advice | [Yes / No] | [notes] |
| Anti-conflict provision | [Yes / No] | [notes] |
| Expiry date | [Yes / No — date] | [notes] |
| Revocation rights retained | [Yes / No] | [notes] |

---

## Multi-Jurisdiction Analysis

| Jurisdiction | Role | Key Considerations | Risk |
|---|---|---|---|
| [jurisdiction] | [role] | [considerations] | [risk] |
| ... | ... | ... | ... |

**Cross-Border Enforceability**: [assessment]

**Notarization / Apostille**: [requirement and whether addressed]

---

## Flags & Risk Indicators

| # | Flag | Exact Language / Location | Risk Level | Recommendation |
|---|---|---|---|---|
| 1 | [flag] | [quoted language] | [High / Medium / Low Risk] | [recommendation] |
| ... | ... | ... | ... | ... |

**Total Flags: [N] ([H] High Risk, [M] Medium Risk, [L] Low Risk)**

---

## Recommended Actions

**Before Execution:**
1. [action — e.g., "Restrict scope to named transaction with defined closing date"]
2. [action — e.g., "Add expiry date tied to transaction closing"]
3. [action — e.g., "Add fiduciary duty clause requiring attorneys to act in grantor's best interest"]
4. [action — e.g., "Confirm notarization requirements for Luxembourg entity registration"]

**If Already Executed:**
1. [action — e.g., "Obtain legal opinion confirming POA is enforceable under Luxembourg law"]
2. [action — e.g., "Monitor use of POA — request attorneys confirm scope of any action taken"]
3. [action — e.g., "Consider issuing revocation if transaction has closed"]

**Ongoing Monitoring:**
1. [action — e.g., "Revoke POA immediately upon transaction closing if no expiry date is present"]
2. [action — e.g., "Maintain register of all actions taken under this POA"]
```

### Important Guidelines

- The most dangerous POA provisions are those that combine broad authority language ("without limitation," "any steps or do anything") with a severally-acting attorney structure and no expiry date. This combination allows any one attorney to take virtually any action indefinitely without the grantor's ongoing consent.
- Multi-jurisdiction POAs require legal confirmation of enforceability in each jurisdiction where the attorney will act. A POA valid under New York law may require notarization and apostille to be effective in Luxembourg or Ireland.
- "Sole and absolute discretion" is a standard phrase in many fund documents when applied to investment decisions, but in a POA context it eliminates any reasonableness standard for the attorney's actions. Always flag it.
- The absence of a "best interest" or fiduciary duty clause is as significant as the presence of broad discretion language. Without it, the attorney has authority but no enforceable duty to use it in the grantor's favor.
- Sub-delegation (the attorney's right to appoint sub-attorneys) compounds risk significantly — it can create chains of authority that are difficult to monitor or revoke.
- Pooling vehicle and affiliate coverage is common in fund investment structures but expands the POA scope beyond the direct investment. This is not inherently problematic but must be flagged for legal review to confirm it was intentional.
- Always recommend revocation of the POA once the authorized transaction closes, unless the POA is explicitly required for ongoing operations.
- For fund administrators: POAs are frequently received as part of transaction closing packages. A structured review prevents unauthorized actions being taken under stale or overly broad instruments after the transaction is complete.
