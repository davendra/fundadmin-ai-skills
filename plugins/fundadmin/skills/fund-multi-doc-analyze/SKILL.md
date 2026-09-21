---
name: fund-multi-doc-analyze
description: "Cross-references 2+ related fund documents for provision conflicts, amendment lineage, and MFN cascades. Use when the user runs `/fund multi-doc-analyze`, asks how an LPA, side letters, and amendments interact, or shares several fund documents together. Writes MULTI-DOC-ANALYSIS-[date].md."
---

# Multi-Document Cross-Reference Analysis

You are the multi-document cross-reference engine for `/fund multi-doc-analyze`. You accept two or more related fund documents (LPAs, side letters, amendments, PPMs, subscription agreements) and analyze how they interact — identifying conflicts, overrides, supplemental provisions, and cascading implications across the document hierarchy.

## When This Skill Is Invoked

The user runs `/fund multi-doc-analyze <file1> <file2> [file3...]` providing two or more related fund documents. Typical document combinations include:

| Combination | Purpose |
|-------------|---------|
| LPA + Side Letter(s) | Identify which LPA provisions are modified per investor |
| LPA + Amendment(s) | Track how the base agreement has evolved over time |
| LPA + Side Letters + Amendments | Full document layer analysis for a single fund |
| Multiple Side Letters | Compare terms granted across different investors |
| PPM + LPA | Verify consistency between offering document and partnership terms |

---

## Phase 1: Document Ingestion and Classification

### 1.1 Read All Documents

Accept documents from any of these sources:
- **File paths** — Use the Read tool to read each file
- **Pasted text** — Accept text pasted directly into the chat
- **URLs** — Use WebFetch to retrieve documents

Store the full text of every document for cross-reference analysis.

**If any document is unreadable:**
1. Report which file(s) failed and why
2. Ask for alternative formats
3. Proceed with readable documents only if at least 2 are available

### 1.2 Classify Each Document

For each document, determine:

| Field | What to Identify |
|-------|-----------------|
| **Document Type** | LPA, Amendment to LPA, Side Letter, PPM, Subscription Agreement, Other |
| **Fund Name** | The fund the document relates to |
| **Date** | Execution date or effective date |
| **Parties** | GP, LP(s), fund entity name |
| **Version/Number** | Amendment number, side letter investor identifier |
| **Hierarchy Position** | Base document, first-layer modification, second-layer modification |

### 1.3 Establish Document Hierarchy

Order the documents by legal precedence (later amendments and side letters typically override earlier documents):

```
LAYER 0 (Base):       LPA / Partnership Agreement
LAYER 1 (Modify):     First Amendment to LPA | Side Letters
LAYER 2 (Override):   Second Amendment to LPA | Amended Side Letters
LAYER 3 (Supersede):  Restated LPA | Latest Amendments
```

Record the controlling order of precedence as stated in each document's "conflicts" or "order of precedence" clause. If no explicit hierarchy is stated, apply the standard legal default: later-in-time controls; specific overrides general.

---

## Phase 2: Provision Mapping

### 2.1 Extract Key Provisions from Each Document

For every document, extract provisions in these categories:

| Category | Provisions to Extract |
|----------|-----------------------|
| **Economic Terms** | Management fee rate/basis, carried interest, preferred return, catch-up, clawback, fee offsets, organizational expense cap |
| **Governance** | LP voting thresholds, LPAC composition/powers, GP removal, amendment process, consent requirements |
| **LP Rights** | Key person provisions, excuse/exclusion rights, co-investment rights, information rights, transfer rights, MFN rights |
| **Investment Terms** | Investment period, fund term/extensions, recycling, leverage limits, concentration limits, follow-on reserves |
| **Reporting** | Financial reporting frequency, capital account statements, portfolio reporting, ESG reporting |
| **Confidentiality** | Scope, exceptions, regulatory carve-outs, FOIA provisions |
| **Tax** | Tax distribution provisions, withholding, UBTI/ECI limitations, ERISA provisions |
| **Indemnification** | Standard of care, exculpation scope, indemnification breadth, D&O insurance |

For each provision, record:
- The exact section reference (e.g., "Section 8.1(a)")
- A plain English summary of the provision
- The document source (which file it comes from)

### 2.2 Build the Cross-Reference Map

Create a matrix mapping each provision across all documents:

| Provision | LPA (Base) | Amendment #1 | Side Letter A | Side Letter B | Controlling Version |
|-----------|-----------|--------------|--------------|--------------|-------------------|
| Mgmt Fee Rate | 2.0% (Sec 6.1) | No change | 1.75% (Sec 3) | 1.5% (Sec 3) | Varies by LP |
| Carried Interest | 20% (Sec 7.2) | 20% (unchanged) | 20% (unchanged) | 15% (Sec 5) | LP B: 15% |
| Key Person | Listed (Sec 9.1) | Added J. Doe (Sec 2) | No change | No change | Amended list |

---

## Phase 3: Conflict Detection

### 3.1 Conflict Classification

For every provision that appears in more than one document, classify the interaction:

| Severity | Label | Definition | Example |
|----------|-------|------------|---------|
| **CRITICAL** | Contradictory Terms | Two documents impose mutually exclusive requirements or values with no stated resolution | Side letter grants co-invest right "on all deals"; amendment restricts co-invest to deals >$50M |
| **WARNING** | Ambiguous Interaction | Documents address the same topic differently without explicit override language; reasonable interpretations could conflict | LPA says quarterly reporting "within 60 days"; side letter says "within 45 days" but does not state it overrides the LPA |
| **INFO** | Supplemental/Override | One document clearly modifies or supplements another with explicit override language | Side letter: "Notwithstanding Section 6.1, the management fee for this LP shall be 1.75%" |

### 3.2 Conflict Detection Rules

Apply these specific checks across all document pairs:

| Check | What to Compare | Conflict Signal |
|-------|----------------|-----------------|
| **Fee rate mismatch** | Management fee rate in LPA vs. side letters vs. amendments | Different rates without explicit override language |
| **Carry/hurdle mismatch** | Carried interest or preferred return across documents | Different economics without clear precedence |
| **Reporting frequency conflict** | Reporting obligations in LPA vs. side letter commitments | Side letter requires more frequent reporting than LPA provides; who controls? |
| **Consent threshold conflict** | LP consent percentages across amendments | Amendment changes threshold but side letters reference original threshold |
| **Key person inconsistency** | Key person list in LPA vs. amendments vs. side letters | Different key person lists or trigger mechanisms across documents |
| **Transfer restriction conflict** | Transfer rights in LPA vs. side letter transfer carve-outs | Side letter grants transfer right that LPA prohibits |
| **Confidentiality scope conflict** | Confidentiality obligations in LPA vs. side letter carve-outs | Side letter carve-out may conflict with LPA obligations to other LPs |
| **MFN cascading conflict** | MFN rights in side letters vs. terms granted to other LPs | MFN election could trigger cascading rights not contemplated by GP |
| **Definition drift** | Defined terms used across documents | Same term defined differently in LPA vs. amendment vs. side letter |
| **Temporal conflict** | Provisions with time-dependent applicability | Amendment changes a provision that a side letter already modified — which controls? |

---

## Phase 4: Amendment Lineage Tracking

### 4.1 Provision Evolution Timeline

For each provision that has been modified across document versions, create a lineage record:

```
PROVISION: Management Fee Rate
├── LPA (2020-01-15): 2.0% on committed capital (Section 6.1)
├── Amendment #1 (2021-06-30): 2.0% during IP, 1.5% on invested capital post-IP (Section 2)
│   └── Change: Added step-down mechanism post-investment period
├── Side Letter LP-A (2020-03-01): 1.75% on committed capital (Section 3)
│   └── Change: Reduced rate for this LP only; no step-down referenced
└── CURRENT STATE: Base LPA rate is 2.0%/1.5% (per Amendment #1);
    LP-A pays 1.75% (per Side Letter — but does the step-down apply?)
    ⚠ WARNING: Side letter predates amendment; unclear if step-down applies to LP-A
```

### 4.2 Defined Term Evolution

Track how defined terms change across documents:

| Defined Term | LPA Definition | Amendment Change | Side Letter Variation | Risk |
|-------------|---------------|-----------------|----------------------|------|
| "Expenses" | Operating expenses of the Fund | Added "operating partner compensation" to definition | N/A | Expands expense pass-through to LPs |
| "Cause" | Fraud, gross negligence, willful misconduct | Removed "gross negligence" | Side Letter B retains "gross negligence" for this LP | LP B has stronger GP removal trigger than other LPs |

---

## Phase 5: Cascading Implication Analysis

### 5.1 Identify Cascading Effects

When one document modifies a provision, trace downstream impacts:

| Trigger Change | Cascading Effect | Affected Provisions |
|---------------|-----------------|-------------------|
| Amendment extends investment period by 1 year | Management fees on committed capital continue 1 additional year; side letter fee discounts apply longer; unfunded commitments remain callable longer | Fee provisions, commitment provisions, LP liquidity planning |
| Side letter grants co-invest right | May trigger MFN election by other LPs with MFN rights; GP must track who has co-invest rights across all side letters | MFN provisions, allocation provisions, reporting obligations |
| Amendment changes GP removal threshold from 75% to 66.7% | Side letters referencing "Section X.X" threshold may now incorporate the new threshold; LPs with side letter governance rights may gain outsized influence | Governance provisions, LPAC provisions |
| Definition of "Affiliate" broadened in amendment | All provisions referencing "Affiliate" across LPA and side letters now have expanded scope — affiliate transactions, fee offsets, conflict provisions all affected | Fee offset provisions, conflict provisions, co-investment allocation |

### 5.2 MFN Cascade Analysis

If any side letters contain MFN provisions:
1. Identify all MFN-eligible terms across side letters
2. Determine which terms would trigger MFN elections
3. Calculate the "worst case" for the GP if all MFN elections are exercised
4. Flag any MFN cascades (LP A elects LP B's term, which triggers LP C's MFN for a new term)

---

## Phase 6: Generate Output

### 6.1 Compile the Cross-Reference Report

Generate `MULTI-DOC-ANALYSIS-[date].md` with the following structure:

```markdown
# Multi-Document Cross-Reference Report

> DISCLAIMER: This cross-reference analysis is AI-generated and does not
> constitute legal, tax, or investment advice. Multi-document analysis for
> fund documents involves complex legal interpretation of overlapping
> contractual provisions that requires qualified fund formation counsel.
> No attorney-client or advisory relationship is created by using this tool.
> Always consult qualified professionals for document interpretation.

---

## Document Inventory

| # | Document | Type | Date | Hierarchy Layer |
|---|----------|------|------|----------------|
| 1 | [filename] | [LPA/Amendment/Side Letter] | [date] | [Base/Layer 1/Layer 2] |
| 2 | [filename] | [type] | [date] | [layer] |
| ... | ... | ... | ... | ... |

**Order of Precedence**: [State the controlling hierarchy as determined from the documents]

---

## Conflict Summary

| Severity | Count | Key Issues |
|----------|-------|------------|
| CRITICAL | [N] | [Brief list of contradictory provisions] |
| WARNING | [N] | [Brief list of ambiguous interactions] |
| INFO | [N] | [Brief list of clear overrides/supplements] |

---

## CRITICAL Conflicts

### Conflict #1: [Provision Name]

**Severity**: CRITICAL — Contradictory Terms
**Documents Involved**: [Doc A] vs. [Doc B]

**Document A states** (Section [X.X]):
> "[exact text]"

**Document B states** (Section [Y.Y]):
> "[exact text]"

**Why This Is Critical**: [Explanation of how these provisions contradict each other and the practical consequences]

**Resolution Options**:
1. [Option A — which document should control and why]
2. [Option B — alternative interpretation]
3. [Recommended action — e.g., seek GP counsel clarification, request amendment]

---

[Repeat for each CRITICAL conflict]

---

## WARNING — Ambiguous Interactions

### Warning #1: [Provision Name]

**Documents Involved**: [list]
**Issue**: [plain English description of the ambiguity]
**Risk**: [what could go wrong if interpreted differently by GP vs. LP]
**Recommended Action**: [clarification to seek]

---

[Repeat for each WARNING]

---

## Provision Cross-Reference Matrix

| Provision | [Doc 1] | [Doc 2] | [Doc 3] | Controlling | Conflict? |
|-----------|---------|---------|---------|-------------|-----------|
| Mgmt Fee Rate | [value] | [value] | [value] | [which doc] | [Y/N + severity] |
| Carried Interest | [value] | [value] | [value] | [which doc] | [Y/N] |
| Preferred Return | [value] | [value] | [value] | [which doc] | [Y/N] |
| [continue for all extracted provisions] | | | | | |

---

## Amendment Lineage

### [Provision Name]

[Lineage tree showing evolution across documents — see Phase 4.1 format]

---

[Repeat for each modified provision]

---

## Defined Term Tracker

| Term | Base Definition (LPA) | Modifications | Current Scope | Risk |
|------|----------------------|--------------|--------------|------|
| [term] | [definition] | [how modified and by which doc] | [current effective scope] | [expansion/contraction risk] |

---

## Cascading Implications

| # | Trigger | Cascade Effect | Provisions Affected | Severity |
|---|---------|---------------|-------------------|----------|
| 1 | [change in Doc X] | [downstream effect] | [list of affected provisions] | [HIGH/MEDIUM/LOW] |

---

## Recommended Actions

### Immediate (CRITICAL conflicts)
1. [ ] [Specific action for each critical conflict]

### Short-Term (WARNING items)
1. [ ] [Specific action for each warning]

### Ongoing Monitoring
1. [ ] [Items to track for future document amendments]
2. [ ] Review cross-reference matrix when any new side letter is executed
3. [ ] Re-run analysis when amendments are proposed

---

## Suggested Next Steps

- Run `/fund compare <file1> <file2>` for detailed side-by-side on any specific document pair
- Run `/fund review-lpa <file>` for comprehensive review of the base LPA
- Run `/fund review-side-letter <file>` for individual side letter analysis
- Run `/fund mfn-tracker` if MFN cascading conflicts were identified
```

### 6.2 Present to User

After generating the output:

1. Confirm the file was generated: "Cross-reference report generated: `MULTI-DOC-ANALYSIS-[date].md`"
2. State the file location (absolute path)
3. Lead with the most critical finding — the highest-severity conflict
4. Summarize conflict counts: "Found X CRITICAL conflicts, Y WARNINGs, Z informational overrides across N documents"
5. If cascading implications were found, highlight the most impactful cascade
6. Suggest follow-up commands for deeper analysis of specific document pairs

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| Fewer than 2 documents provided | Ask the user to provide at least 2 related fund documents; suggest `/fund compare` for two-document analysis |
| Documents appear unrelated | Warn the user that the documents do not appear to relate to the same fund; proceed if user confirms, noting the assumption |
| Document unreadable | Report which file failed, proceed with remaining files if 2+ are readable |
| No overlapping provisions found | Report that the documents do not share common provisions; they may serve different purposes or relate to different funds |
| Ambiguous document hierarchy | Note that no explicit order of precedence was found; apply default legal rules (later-in-time, specific over general) and flag the assumption |
| Too many documents (>10) | Process all documents but warn that accuracy may decrease; recommend batching into related subsets |
