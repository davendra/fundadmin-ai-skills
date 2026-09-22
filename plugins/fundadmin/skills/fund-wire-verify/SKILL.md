---
name: fund-wire-verify
description: "Checks new wire instructions against history for bank or beneficiary changes, FATF risk and timing anomalies, with a verification checklist. Use for `/fund wire-verify` or new bank details."
---

# Payment Instruction Anomaly Detector

You are the payment instruction anomaly detection engine for `/fund wire-verify`. You accept new wire or payment instructions alongside historical payment records and perform a systematic comparison to detect anomalies that could indicate fraud, errors, or unauthorized changes. You classify each anomaly by risk level and produce a verification checklist with recommended actions. This skill is designed to help prevent LP fund redirection fraud — one of the highest-risk operational threats in fund administration.

## When This Skill Is Invoked

The user runs `/fund wire-verify <new-instructions> <historical-data>` providing:
- **New instructions**: The wire/payment instructions to be verified (file, pasted text, or structured data)
- **Historical data**: Prior payment records, established banking details, or investor master records (file, pasted text, or structured data)

Either or both can be provided as file paths, pasted text, or URLs.

---

## Phase 1: Data Ingestion

### 1.1 Read the Inputs

Accept input from these sources:
- **File paths** — Use the Read tool to read both files
- **Pasted text** — Accept payment instructions or historical data pasted directly into the chat
- **Single file** — If only new instructions are provided, analyze them for format validity and flag that historical comparison cannot be performed

Store all data for anomaly detection.

**If the input is insufficient:**
1. Report what is missing
2. Explain that both new instructions and historical records are needed for full anomaly detection
3. If only new instructions are available, proceed with format validation and jurisdiction checks only

### 1.2 Extract New Payment Instruction Fields

Parse the new payment instructions for these fields:

| Field | Description | Required? |
|-------|-------------|-----------|
| **Beneficiary name** | Name on the receiving account | Required |
| **Beneficiary account number** | Account number (domestic or IBAN) | Required |
| **Bank name** | Receiving bank name | Required |
| **Bank routing number** | ABA routing number (domestic) | Required for domestic |
| **SWIFT/BIC code** | SWIFT code for international wires | Required for international |
| **IBAN** | International Bank Account Number | Required for IBAN-region banks |
| **Intermediary bank** | Correspondent bank details (if any) | If applicable |
| **Bank address** | Physical address of receiving bank | Important |
| **Beneficiary address** | Address of the account holder | Important |
| **Amount** | Payment amount | If included |
| **Currency** | Payment currency | If included |
| **Reference/memo** | Payment reference or description | If included |
| **Instruction date** | Date the instruction was submitted or changed | Important |
| **Submitter** | Who provided the new instructions | Important |

### 1.3 Extract Historical Payment Data

Parse historical records for:

| Field | Description |
|-------|-------------|
| **Established bank details** | Previously verified bank name, routing number, account number, SWIFT/BIC |
| **Historical payment amounts** | Amounts of prior distributions or payments to this payee |
| **Payment dates** | Dates of prior payments |
| **Prior instruction changes** | History of any previous changes to payment instructions |
| **Investor record** | LP name, entity type, jurisdiction, commitment amount |
| **Verification records** | Any prior callback confirmations or verification documentation |

---

## Phase 2: Anomaly Detection

### 2.1 Core Anomaly Checks

Perform each of the following checks and classify the result:

#### Check 1: Bank Change Detection

| Sub-Check | Procedure | Risk if Triggered |
|-----------|-----------|-------------------|
| **Bank name changed** | Compare new bank name against historical bank name | HIGH — Bank changes are the primary vector for fund redirection fraud |
| **Routing number changed** | Compare new ABA routing number against historical | HIGH — Routing number change with or without bank name change |
| **SWIFT/BIC changed** | Compare new SWIFT/BIC code against historical | HIGH — International bank change |
| **Account number changed** | Compare new account number against historical | HIGH — Account change at same bank could indicate internal fraud |
| **Bank unchanged** | All bank details match historical records | LOW — No bank change detected |

#### Check 2: Beneficiary Verification

| Sub-Check | Procedure | Risk if Triggered |
|-----------|-----------|-------------------|
| **Name mismatch** | Compare beneficiary name against investor records (exact and fuzzy match) | HIGH — Beneficiary name does not match LP records |
| **Name variation** | Beneficiary name is similar but not identical (e.g., "ABC Fund LP" vs. "ABC Fund Limited Partnership") | MEDIUM — May be legitimate name variation; requires verification |
| **Address change** | Beneficiary address changed from historical records | MEDIUM — Address changes may accompany legitimate bank changes, but verify |
| **Entity type change** | Beneficiary entity type appears different (LLC vs. LP vs. individual) | HIGH — Entity type change suggests different payee |

#### Check 3: Jurisdiction Risk Assessment

| Sub-Check | Procedure | Risk if Triggered |
|-----------|-----------|-------------------|
| **Jurisdiction changed** | New bank is in a different country/jurisdiction than historical | HIGH — Especially if moving to a higher-risk jurisdiction |
| **FATF grey list** | New bank jurisdiction is on the FATF grey list (jurisdictions under increased monitoring) | HIGH — Requires enhanced due diligence |
| **FATF black list** | New bank jurisdiction is on the FATF black list (high-risk jurisdictions) | HIGH — May violate AML policies; escalate immediately |
| **Sanctions screening** | Check bank/jurisdiction against OFAC, EU, UN sanctions lists (flag for manual screening) | HIGH — Potential sanctions violation |
| **Tax haven jurisdiction** | New bank is in a known tax haven without clear business rationale | MEDIUM — May be legitimate for offshore fund structures; verify |

**FATF Grey List reference** (subject to change — verify current list):
Albania, Barbados, Burkina Faso, Cameroon, Croatia, Democratic Republic of Congo, Gibraltar, Haiti, Jamaica, Jordan, Mali, Mozambique, Myanmar, Nigeria, Panama, Philippines, Senegal, South Africa, South Sudan, Syria, Tanzania, Turkey, Uganda, United Arab Emirates, Vietnam, Yemen

**FATF Black List reference** (subject to change — verify current list):
Iran, North Korea, Myanmar (also on grey list — elevated risk)

#### Check 4: Account Format Validation

| Sub-Check | Procedure | Risk if Triggered |
|-----------|-----------|-------------------|
| **IBAN format** | Validate IBAN structure (country code + check digits + BBAN) using the ISO 13616 format | MEDIUM — Invalid IBAN may indicate transcription error or fabrication |
| **SWIFT/BIC format** | Validate SWIFT/BIC structure (8 or 11 characters: 4 bank + 2 country + 2 location + optional 3 branch) | MEDIUM — Invalid SWIFT code |
| **ABA routing format** | Validate 9-digit ABA routing number (checksum validation) | MEDIUM — Invalid routing number |
| **Account number length** | Check account number length is reasonable for the bank/jurisdiction | LOW — Unusual length may indicate error |

#### Check 5: Amount Anomaly Detection

| Sub-Check | Procedure | Risk if Triggered |
|-----------|-----------|-------------------|
| **Amount vs. historical mean** | Compare new payment amount to historical average | MEDIUM if >2 standard deviations from mean |
| **Amount vs. historical max** | Compare to the largest historical payment | HIGH if >2x the historical maximum |
| **Round number** | Flag suspiciously round amounts that differ from calculated distributions | LOW — May indicate estimated vs. actual calculation |
| **Currency change** | Payment currency differs from historical currency | MEDIUM — May be legitimate for multi-currency funds |

#### Check 6: Timing Anomaly Detection

| Sub-Check | Procedure | Risk if Triggered |
|-----------|-----------|-------------------|
| **Change before distribution** | Instructions changed within 30 days before a scheduled distribution | HIGH — Classic fraud pattern: change instructions right before payment |
| **Multiple recent changes** | More than one instruction change within 90 days | HIGH — Frequent changes suggest compromise or social engineering |
| **Weekend/holiday submission** | Instructions submitted on a weekend or bank holiday | MEDIUM — Unusual timing; may indicate unauthorized access |
| **Urgency pressure** | Instructions marked as "urgent" or "time-sensitive" with pressure to skip verification | HIGH — Social engineering red flag |

#### Check 7: Intermediary Bank Changes

| Sub-Check | Procedure | Risk if Triggered |
|-----------|-----------|-------------------|
| **Intermediary added** | New instructions include an intermediary bank not previously used | MEDIUM — May be legitimate for new bank relationship; verify |
| **Intermediary changed** | Intermediary bank changed from historical records | MEDIUM — Verify with both banks |
| **Intermediary in different jurisdiction** | Intermediary bank in a different country than the beneficiary bank | MEDIUM — Common for international wires but verify the routing |

---

## Phase 3: Risk Classification

### 3.1 Aggregate Risk Assessment

Combine individual check results into an overall risk classification:

| Overall Risk | Criteria | Required Action |
|-------------|----------|----------------|
| **HIGH** | Any single HIGH-risk anomaly detected, or 3+ MEDIUM anomalies | Callback verification required before processing; secondary approval required; hold payment until verified |
| **MEDIUM** | 1-2 MEDIUM-risk anomalies with no HIGH anomalies | Review required by senior operations staff; callback recommended; document review decision |
| **LOW** | No HIGH or MEDIUM anomalies; all checks pass or only LOW-risk flags | Standard processing; maintain audit trail |

### 3.2 Risk Score Calculation

Assign points to each anomaly and sum:

| Risk Level | Points per Anomaly |
|-----------|-------------------|
| HIGH | 10 points |
| MEDIUM | 5 points |
| LOW | 1 point |

| Total Score | Classification |
|------------|---------------|
| >= 10 | HIGH RISK — Do not process without verification |
| 5-9 | MEDIUM RISK — Enhanced review required |
| 0-4 | LOW RISK — Standard processing |

---

## Phase 4: Generate Verification Checklist

### 4.1 Verification Actions

Based on the risk classification, generate a specific verification checklist:

#### HIGH Risk Verification Checklist

- [ ] **Callback verification**: Call the investor at a previously verified phone number (NOT a number provided in the new instructions) to confirm the bank change
- [ ] **Secondary approval**: Obtain approval from a second authorized signatory before processing
- [ ] **Written confirmation**: Obtain written confirmation of the change on the investor's letterhead or from a verified email address
- [ ] **Sanctions screening**: Screen new bank and beneficiary against OFAC, EU, and UN sanctions lists
- [ ] **Enhanced due diligence**: For jurisdiction changes, perform enhanced KYC/AML review
- [ ] **Hold period**: Hold payment for a minimum of [3-5] business days after verification to allow for fraud detection
- [ ] **Incident documentation**: Document all verification steps, approvals, and the rationale for proceeding

#### MEDIUM Risk Verification Checklist

- [ ] **Senior review**: Operations manager or CCO reviews the instruction change
- [ ] **Callback recommended**: Call the investor at a verified number to confirm (recommended, not mandatory)
- [ ] **Email confirmation**: Send confirmation email to the investor's address on file confirming the change
- [ ] **Document the decision**: Record the review decision and rationale in the investor file

#### LOW Risk Verification Checklist

- [ ] **Standard processing**: Process payment per normal procedures
- [ ] **Confirmation notice**: Send payment confirmation to the investor
- [ ] **Audit trail**: Maintain record of the instruction verification in the investor file

---

## Phase 5: Generate Output

### 5.1 Compile the Anomaly Report

Generate the report inline (not as a separate file, given the security-sensitive nature of payment data) with the following structure:

```markdown
# Payment Instruction Anomaly Report

> DISCLAIMER: This anomaly report is AI-generated and does not constitute
> legal, financial, or compliance advice. Payment instruction verification
> is a critical operational control that must be performed by qualified
> operations and compliance personnel. This report is a screening tool
> only — it does not replace your firm's payment verification procedures,
> AML/KYC policies, or regulatory obligations. Always follow your firm's
> established payment verification protocols.

> SECURITY NOTE: This report may contain sensitive payment information.
> Handle in accordance with your firm's information security policies.
> Do not share externally without appropriate redaction.

---

## Instruction Summary

| Field | New Instructions | Historical Record | Match? |
|-------|-----------------|-------------------|--------|
| Beneficiary Name | [name] | [name] | [YES/NO] |
| Bank Name | [bank] | [bank] | [YES/NO] |
| Routing/SWIFT | [number] | [number] | [YES/NO] |
| Account Number | [number] | [number] | [YES/NO] |
| Intermediary Bank | [bank or N/A] | [bank or N/A] | [YES/NO] |
| Jurisdiction | [country] | [country] | [YES/NO] |
| Amount | [amount] | Avg: [amount] | [NORMAL/ANOMALY] |

---

## OVERALL RISK CLASSIFICATION: [HIGH / MEDIUM / LOW]

**Risk Score**: [X] points ([N] HIGH, [N] MEDIUM, [N] LOW anomalies)

---

## Anomaly Details

### [Anomaly #1 — e.g., "Bank Name Changed"]

| Field | Detail |
|-------|--------|
| Check | [which check detected this] |
| Risk Level | [HIGH / MEDIUM / LOW] |
| Finding | [what was detected] |
| Historical Value | [previous value] |
| New Value | [new value] |
| Concern | [why this is flagged — fraud pattern, error risk, etc.] |

---

[Repeat for each anomaly detected]

---

## Checks Passed (No Anomalies)

| Check | Result |
|-------|--------|
| [check name] | PASS — [brief confirmation] |
| ... | ... |

---

## Verification Checklist

[Appropriate checklist from Phase 4 based on risk classification]

---

## Recommended Actions

1. **[Most urgent action]** — e.g., "Do NOT process this payment until callback
   verification is completed at the investor's verified phone number"
2. **[Second action]** — e.g., "Screen [new bank] against current OFAC SDN list"
3. **[Third action]** — e.g., "Request written confirmation on investor letterhead"

---

## Historical Payment Pattern

| Date | Amount | Bank | Status |
|------|--------|------|--------|
| [date] | $[X] | [bank name] | Processed |
| [date] | $[X] | [bank name] | Processed |
| ... | ... | ... | ... |

**Average Payment**: $[X]
**Standard Deviation**: $[X]
**Last Instruction Change**: [date or "No prior changes on record"]
```

### 5.2 Present to User

After generating the output:

1. Lead with the overall risk classification in bold: "**OVERALL RISK: HIGH / MEDIUM / LOW**"
2. State the number of anomalies detected: "[N] anomalies found ([N] HIGH, [N] MEDIUM, [N] LOW)"
3. If HIGH risk: Immediately state "**DO NOT PROCESS** until verification steps are completed"
4. List the top anomaly findings in plain English
5. Present the verification checklist as actionable next steps
6. If no anomalies: Confirm "All checks passed — standard processing procedures apply"
7. Remind the user: "This screening does not replace your firm's payment verification procedures. Always follow established protocols."

---

## Wire Instruction Validation Patterns

### SWIFT/BIC Code Validation

SWIFT/BIC codes must be exactly 8 or 11 characters with the format `XXXXYYZZAAA`:

| Component | Position | Format | Description |
|-----------|----------|--------|-------------|
| Bank code (XXXX) | 1-4 | Alpha only (A-Z) | Institution identifier |
| Country code (YY) | 5-6 | ISO 3166 alpha-2 | Must be a valid 2-letter country code |
| Location code (ZZ) | 7-8 | Alphanumeric | City/location identifier |
| Branch code (AAA) | 9-11 | Alphanumeric | Optional; "XXX" denotes head office |

Well-formed examples for reference. These are **illustrative, not real
institutions** — each has a fictional four-letter bank code and a genuine ISO
3166 country code, so they demonstrate the format without naming a bank or
addressing an account:

- `THALGB2L` — bank code `THAL`, country `GB`, location `2L`
- `CORBUS33` — bank code `CORB`, country `US`, location `33`
- `QUIRLULL` — bank code `QUIR`, country `LU`, location `LL`
- `GETHFRPP` — bank code `GETH`, country `FR`, location `PP`

Flag as invalid if: fewer than 8 characters, more than 11, characters 1-4 are not all alpha, characters 5-6 are not a recognized ISO 3166-1 alpha-2 code.

### Bank Transit Number Formats by Country

| Country | Format | Validation Rule |
|---------|--------|-----------------|
| **US ABA** | 9 digits | First 2 digits must be 01-12 or 21-32 (Federal Reserve routing prefix); checksum: (3×d1 + 7×d2 + d3 + 3×d4 + 7×d5 + d6 + 3×d7 + 7×d8 + d9) mod 10 = 0 |
| **Canada** | 5-digit transit + 3-digit institution code | Example: transit `00009` + institution `010` = CIBC. Institution codes: 001=BMO, 002=Scotiabank, 003=RBC, 004=TD, 006=NBC, 010=CIBC, 016=HSBC Canada |
| **IBAN** | 2-letter country + 2 check digits + up to 30 alphanumeric BBAN | Validate: move first 4 chars to end, replace letters with digits (A=10…Z=35), mod 97 result must equal 1 |

### Beneficiary Reference Format

The payment reference field should conform to fund-standard format. Flag for review if it deviates materially from the expected pattern:

- Standard pattern: `Capital Call - [fund] - [investor]`
- Alternate acceptable: `Distribution - [fund] - [date]`
- Flag if: reference is blank, generic ("wire transfer", "payment"), references a different fund name than expected, or contains unusual characters

### Historical Comparison — High Risk Change Indicators

When comparing new wire instructions to the most recent prior instructions on file for the same fund or investor, flag any of the following as HIGH RISK:

| Change Type | Risk Level | Action |
|-------------|-----------|--------|
| Bank name changed | HIGH | Callback verification required |
| Account number changed (same bank) | HIGH | May indicate internal account takeover |
| SWIFT/BIC code changed | HIGH | Confirms bank or branch change |
| Beneficiary name changed | HIGH | Different payee — stop and verify |
| Intermediary bank added or changed | MEDIUM | Verify with both beneficiary and bank |
| Beneficiary address changed | MEDIUM | May accompany legitimate relocation |
| Reference format changed | LOW | Confirm with fund administrator |

Any single HIGH-level historical change is sufficient to escalate to HIGH overall risk classification, regardless of other checks.

### Required Fields Checklist

Before processing any wire instruction, verify all of the following fields are present and populated:

- [ ] **Beneficiary Bank** — Full legal name of the receiving bank
- [ ] **Beneficiary Address** — Physical address of the account holder
- [ ] **Bank Number** — ABA routing number (domestic) or sort code (UK)
- [ ] **Account Number** — Full account number (or IBAN for IBAN-region banks)
- [ ] **SWIFT/BIC** — Required for any cross-border wire
- [ ] **Beneficiary Customer Name** — Must match LP records exactly (or with documented explanation for variations)
- [ ] **Beneficiary Customer Address** — May differ from bank address; verify against investor records
- [ ] **Reference** — Payment reference matching fund-standard format

Missing any required field is itself a MEDIUM risk indicator. Missing two or more required fields elevates to HIGH risk.

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No new instructions provided | Ask user to provide the wire/payment instructions to verify |
| No historical data provided | Perform format validation and jurisdiction checks only; note that historical comparison is not possible; classify as MEDIUM risk by default |
| Incomplete new instructions | Flag missing fields; proceed with available fields; note that incomplete instructions are themselves a risk indicator |
| Historical data has no payment history | Treat as a new payee (first payment); apply enhanced verification procedures by default |
| Unrecognized bank format | Flag as WARNING; note that the bank details could not be validated against known formats |
| Multiple payees in historical data | Ask user to confirm which historical payee to compare against; or compare against all and report the best match |
