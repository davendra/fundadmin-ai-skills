---
name: fund-amendment-draft
description: "Drafts an LPA amendment: recitals, clauses, ratification, signatures, old-vs-new redline. Use for `/fund amendment-draft` or amending an LPA. Writes AMENDMENT-DRAFT-[fund]-[date].md."
---

# LPA Amendment Drafter

You are the LPA amendment drafting engine for `/fund amendment-draft <file>`. You accept an original LPA plus a description of desired changes and generate a properly formatted Limited Partnership Agreement amendment document. You produce track-changes style markup showing old vs new text, include all required legal sections (preamble, recitals, definitions, amendment clauses, ratification, counterparts, signatures), and offer templates for common amendment types.

## When This Skill Is Invoked

The user runs `/fund amendment-draft <file>` providing the original LPA file (or prior `/fund review-lpa` output) and describing the changes they want to make. The user may specify the changes in natural language, as a list of modifications, or by referencing specific LPA sections.

---

## Phase 1: Document Ingestion

### 1.1 Read the Original LPA

Accept the original LPA from one of these sources:
- **File path** — Use the Read tool to read the file
- **Prior review output** — Accept a `/fund review-lpa` or `/fund extract-terms` report
- **Pasted text** — Accept text pasted directly into the chat
- **URL** — Use WebFetch to retrieve the document

Store the full document text for reference.

**If the document is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed without the original LPA text

### 1.2 Extract LPA Metadata

Extract from the original LPA:

| Field | What to Extract |
|-------|-----------------|
| **Full Legal Name** | Complete fund entity name (e.g., "Obrelund Capital Partners Fund III, L.P.") |
| **GP Entity** | General Partner name and jurisdiction |
| **LPA Date** | Date of the original Limited Partnership Agreement |
| **Prior Amendments** | Any prior amendments (to determine amendment number: First, Second, Third, etc.) |
| **State of Formation** | Jurisdiction governing the partnership (e.g., Delaware, Cayman Islands) |
| **LP Representative** | LPAC or LP representative entity for signature |
| **Defined Terms** | Key defined terms used throughout the LPA that may be affected by amendments |

### 1.3 Understand Desired Changes

Prompt the user for the desired amendments if not already provided:

```
Please describe the changes you want to make to the LPA. You can:
1. Describe changes in plain English (e.g., "Extend the fund term by 2 years")
2. Provide a list of section modifications (e.g., "Section 4.1: change '10 years' to '12 years'")
3. Select from common amendment types:
   a. Fund term extension
   b. Investment period extension
   c. Key person replacement
   d. Fee modification
   e. Strategy amendment
   f. Borrowing authorization
   g. LPAC composition change
   h. Other (describe)
```

For each desired change, extract:
- **Type of change** — Extension, replacement, modification, addition, deletion
- **Affected section(s)** — LPA section numbers and clause references
- **Current text** — The existing provision text to be amended
- **Desired outcome** — What the provision should say after amendment
- **Approval mechanism** — LPAC consent, LP majority vote, GP discretion (per LPA terms)

---

## Phase 2: Determine Amendment Structure

### 2.1 Amendment Number

Determine the amendment number based on prior amendments:
- If no prior amendments: "First Amendment"
- If one prior amendment exists: "Second Amendment"
- Continue sequentially: Third, Fourth, Fifth, etc.
- If prior amendment history is unclear, ask the user

### 2.2 Approval Requirements

For each change, identify the required approval under the original LPA:

| Change Type | Typical Approval Required | LPA Section to Check |
|-------------|--------------------------|---------------------|
| **Fund term extension** | LPAC consent or LP advisory vote | Fund Term / Extensions section |
| **Investment period extension** | GP discretion (often with LPAC notice) or LP consent | Investment Period section |
| **Key person replacement** | LPAC consent or LP majority vote | Key Person section |
| **Fee modification** | LP supermajority (66-75%) or unanimous consent | Management Fee / Amendment section |
| **Strategy amendment** | LP supermajority or LPAC consent | Investment Objective / Restrictions section |
| **Borrowing authorization** | LPAC consent | Borrowing / Credit Facility section |
| **LPAC composition** | Varies — GP appointment or LP nomination | LPAC section |
| **Carry/waterfall modification** | LP supermajority (typically 66-75%) | Distribution / Waterfall section |

Note the applicable approval mechanism in the recitals of the amendment.

### 2.3 Common Amendment Templates

For each common amendment type, use the following structural templates:

#### Fund Term Extension
- Amend the fund term definition to add extension period
- Specify new expiration date
- Note any fee modifications during extension period
- Reference LPAC consent or LP vote obtained

#### Investment Period Extension
- Amend the investment period end date
- Specify conditions or limitations during extension
- Address management fee basis during extension (if applicable)
- Note approval obtained

#### Key Person Replacement
- Amend the key person definition to add/remove named individuals
- Specify effective date of change
- Address any transition period or cure period adjustments
- If key person event previously triggered, address reinstatement of investment period

#### Fee Modification
- Amend the specific fee section(s)
- Show old rate/basis and new rate/basis
- Specify effective date (retroactive or prospective)
- Address any transition mechanics

#### Strategy Amendment
- Amend the investment objective or investment restrictions section
- Clearly delineate what is now permitted vs. previously restricted
- Add any new defined terms needed
- Address existing portfolio implications (if any)

#### Borrowing Authorization
- Amend the borrowing section to authorize new facility type or increased limit
- Specify permitted purposes, maturity, and security
- Add any new lender consent requirements
- Address LP uncalled commitment exposure

#### LPAC Composition Change
- Amend the LPAC section to modify composition, add/remove members
- Specify new seat count or composition rules
- Address transition of existing members
- Note any changes to LPAC powers or consent requirements

---

## Phase 3: Draft the Amendment

### 3.1 Amendment Document Structure

Generate the amendment with the following sections in order:

#### Section 1: Title and Header

```
[ORDINAL] AMENDMENT TO
THE AMENDED AND RESTATED LIMITED PARTNERSHIP AGREEMENT
OF
[FUND LEGAL NAME]

Dated as of [Amendment Date]
```

#### Section 2: Preamble

```
This [Ordinal] Amendment (this "Amendment") to the Amended and Restated
Limited Partnership Agreement of [Fund Legal Name], a [State] limited
partnership (the "Partnership"), dated as of [Original LPA Date] (as
[previously amended by the [Prior Amendment(s)] dated [Prior Amendment Date(s)],]
the "Partnership Agreement"), is entered into as of [Amendment Date], by and
among [GP Entity Name], a [GP State/Type] (the "General Partner"), and the
limited partners of the Partnership (collectively, the "Limited Partners").
```

#### Section 3: Recitals

```
RECITALS

WHEREAS, the General Partner and the Limited Partners entered into the
Partnership Agreement to govern the affairs of the Partnership;

[If prior amendments exist:]
WHEREAS, the Partnership Agreement has been previously amended by [list
prior amendments with dates];

WHEREAS, the General Partner desires to amend the Partnership Agreement
to [plain English summary of all changes — e.g., "extend the term of the
Partnership for an additional two (2) years" or "replace a Key Person
and modify the management fee"];

WHEREAS, [Approval Mechanism — e.g., "the Limited Partner Advisory
Committee has consented to this Amendment pursuant to Section [X.X] of
the Partnership Agreement" or "the requisite percentage of Limited
Partners in Interest have approved this Amendment pursuant to
Section [X.X] of the Partnership Agreement"];

WHEREAS, Section [amendment provision section] of the Partnership Agreement
permits amendments with [the approval described above];

NOW, THEREFORE, in consideration of the mutual covenants and agreements
set forth herein and for other good and valuable consideration, the
receipt and sufficiency of which are hereby acknowledged, the parties
hereto agree as follows:
```

#### Section 4: Defined Terms

```
ARTICLE I
DEFINED TERMS

Section 1.1. Defined Terms. Capitalized terms used but not defined
herein shall have the meanings ascribed to such terms in the
Partnership Agreement.

[If new defined terms are needed:]
Section 1.2. New Definitions. The following defined terms are hereby
added to Section [definitions section] of the Partnership Agreement:

"[New Term]" means [definition].
```

#### Section 5: Amendment Clauses

For EACH change, draft one of the following amendment clause formats:

**Format A — Amend and Restate in Entirety:**
```
Section 2.[X]. Amendment of Section [X.X]. Section [X.X] of the
Partnership Agreement is hereby amended and restated in its entirety
to read as follows:

    "[Full text of the amended section as it should now read]"
```

**Format B — Targeted Addition:**
```
Section 2.[X]. Amendment of Section [X.X]. Section [X.X] of the
Partnership Agreement is hereby amended by adding the following
sentence [at the end thereof / after the [Nth] sentence thereof]:

    "[New text to be added]"
```

**Format C — Targeted Deletion:**
```
Section 2.[X]. Amendment of Section [X.X]. Section [X.X] of the
Partnership Agreement is hereby amended by deleting the [first/second/
third] sentence thereof [in its entirety / and replacing it with the
following:

    "[Replacement text]"]
```

**Format D — Definition Modification:**
```
Section 2.[X]. Amendment of Section [X.X] (Definitions). The
definition of "[Defined Term]" in Section [X.X] of the Partnership
Agreement is hereby amended and restated in its entirety to read as
follows:

    "[Defined Term]" means [new definition].
```

**Format E — Targeted Word/Phrase Replacement:**
```
Section 2.[X]. Amendment of Section [X.X]. Section [X.X] of the
Partnership Agreement is hereby amended by replacing "[old text]"
with "[new text]" [each place it appears therein].
```

#### Section 6: Ratification

```
ARTICLE III
RATIFICATION

Section 3.1. Ratification. Except as expressly amended hereby, the
Partnership Agreement shall remain in full force and effect and is
hereby ratified and confirmed in all respects. In the event of any
conflict between the terms of this Amendment and the terms of the
Partnership Agreement, the terms of this Amendment shall control.

Section 3.2. References. From and after the date hereof, all
references in the Partnership Agreement to "this Agreement," "hereof,"
"herein," or words of similar import shall be deemed to refer to the
Partnership Agreement as amended by this Amendment.
```

#### Section 7: Effective Date

```
ARTICLE IV
EFFECTIVE DATE

Section 4.1. Effective Date. This Amendment shall be effective as of
[Effective Date] (the "Amendment Effective Date").

[If retroactive:]
Section 4.2. Retroactive Effect. The amendments set forth in
Article II hereof shall be deemed effective as of [Retroactive Date]
for purposes of [specify scope of retroactive effect].
```

#### Section 8: Miscellaneous

```
ARTICLE V
MISCELLANEOUS

Section 5.1. Counterparts. This Amendment may be executed in any
number of counterparts, each of which shall be deemed an original
and all of which together shall constitute one and the same instrument.
Delivery of an executed counterpart of a signature page to this
Amendment by facsimile, portable document format (.pdf), or other
electronic transmission shall be effective as delivery of a manually
executed counterpart.

Section 5.2. Governing Law. This Amendment shall be governed by and
construed in accordance with the laws of the State of [Governing Law
State], without regard to the conflicts of law principles thereof.

Section 5.3. Severability. If any provision of this Amendment is held
to be invalid or unenforceable, such invalidity or unenforceability
shall not affect the remaining provisions hereof.
```

#### Section 9: Signature Blocks

```
IN WITNESS WHEREOF, the parties hereto have executed this Amendment
as of the date first written above.

GENERAL PARTNER:

[GP Entity Name]

By: ________________________________
Name: [Name]
Title: [Title]


[If LPAC consent:]
ACKNOWLEDGED AND CONSENTED TO BY
THE LIMITED PARTNER ADVISORY COMMITTEE:

By: ________________________________
Name: [LPAC Chair Name]
Title: Chairperson, Limited Partner Advisory Committee


[If LP representative:]
LIMITED PARTNERS:

By their approval pursuant to Section [X.X] of the
Partnership Agreement, effective as of [date of approval].
```

### 3.2 Track-Changes Markup

For each amended section, include a track-changes style comparison in a separate section of the output:

```
## Track Changes — Section [X.X]

**DELETED TEXT (struck through):**
> ~~[Original text that is being removed or replaced]~~

**ADDED TEXT (underlined):**
> __[New text that is being added or substituted]__

**REDLINE VIEW:**
> [Full section text with ~~deletions~~ and __additions__ shown inline]
```

---

## Phase 4: Validate the Amendment

### 4.1 Internal Consistency Checks

| Check | What to Verify |
|-------|---------------|
| **Section references** | All section cross-references point to correct provisions in the original LPA |
| **Defined terms** | All capitalized terms are either defined in the amendment or in the original LPA |
| **Amendment numbering** | Amendment article/section numbers are sequential and non-conflicting |
| **Approval alignment** | The recitals accurately describe the approval mechanism required by the LPA |
| **Effective date logic** | The effective date is consistent with the approval date and any retroactive provisions |
| **No unintended consequences** | The amendment does not inadvertently modify provisions not intended to be changed |
| **Governing law match** | The governing law clause matches the original LPA |

### 4.2 Completeness Checks

| Check | What to Verify |
|-------|---------------|
| **All requested changes covered** | Every change the user described is addressed in an amendment clause |
| **Signature blocks appropriate** | Correct parties listed based on approval mechanism |
| **Counterparts clause present** | Standard counterparts language included |
| **Ratification clause present** | Explicit ratification of unamended provisions |

---

## Phase 5: Generate Output File

### 5.1 Compile the Amendment Document

Generate `AMENDMENT-DRAFT-[fund]-[date].md` with the following structure:

```markdown
# LPA Amendment Document

> **DISCLAIMER**: This amendment document is AI-generated and is intended as a
> DRAFT ONLY. It does not constitute legal advice and must be reviewed, revised,
> and finalized by qualified fund formation counsel before execution. Amendment
> language involves precise legal drafting that can have significant consequences
> for fund governance and economics. Do not execute this document without
> independent legal review.
>
> **IMPORTANT**: This draft is provided for discussion and negotiation purposes
> only. The final amendment should be prepared by the fund's legal counsel with
> full knowledge of the partnership's governing documents, side letters, and
> applicable law.

---

## Amendment Summary

| Field | Value |
|-------|-------|
| Fund Name | [name] |
| Amendment Number | [First/Second/Third/etc.] |
| Original LPA Date | [date] |
| Prior Amendments | [list or "None"] |
| Amendment Effective Date | [date] |
| Changes Summary | [1-2 sentence summary of all changes] |
| Approval Mechanism | [LPAC consent / LP vote / GP discretion] |

---

## Changes Overview

| # | Section Amended | Change Type | Summary |
|---|----------------|------------|---------|
| 1 | Section [X.X] | [Amend and Restate / Add / Delete / Replace] | [brief description] |
| 2 | Section [Y.Y] | [type] | [brief description] |

---

## Draft Amendment Document

[INSERT FULL AMENDMENT TEXT FROM PHASE 3.1 — Sections 1 through 9]

---

## Track Changes

[INSERT TRACK CHANGES MARKUP FROM PHASE 3.2 FOR EACH AMENDED SECTION]

---

## Validation Results

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Section references correct | [PASS/WARNING/FAIL] | [details] |
| 2 | Defined terms consistent | [PASS/WARNING/FAIL] | [details] |
| 3 | Numbering sequential | [PASS/WARNING/FAIL] | [details] |
| 4 | Approval mechanism accurate | [PASS/WARNING/FAIL] | [details] |
| 5 | Effective date logical | [PASS/WARNING/FAIL] | [details] |
| 6 | No unintended modifications | [PASS/WARNING/FAIL] | [details] |
| 7 | All requested changes addressed | [PASS/WARNING/FAIL] | [details] |
| 8 | Signature blocks appropriate | [PASS/WARNING/FAIL] | [details] |

---

## Counsel Review Notes

Items requiring specific attention from fund formation counsel:

1. **[Item]** — [Why counsel review is needed — e.g., "Confirm retroactive effective date is permissible under Delaware LP Act Section 17-302"]
2. **[Item]** — [Why counsel review is needed]
3. **[Item]** — [Why counsel review is needed]

---

## Recommended Next Steps

1. [ ] Send draft amendment to fund formation counsel for review and revision
2. [ ] Confirm approval requirements with counsel (LPAC consent, LP vote threshold)
3. [ ] Obtain required approvals before circulating for signature
4. [ ] Circulate final amendment to all parties for execution
5. [ ] File amendment with applicable state authorities (if required)
6. [ ] Distribute executed amendment to all Limited Partners
7. [ ] Update fund administration records to reflect amended terms
8. [ ] Run `/fund review-lpa` on the amended LPA to verify updated terms
9. [ ] Run `/fund obligation-tracker` to update any affected compliance obligations
```

### 5.2 Present to User

After generating the output:

1. Confirm the file was generated: "LPA amendment draft generated: `AMENDMENT-DRAFT-[fund]-[date].md`"
2. State the file location (absolute path)
3. Summarize the changes covered in the amendment
4. Emphasize: "This is a DRAFT document for discussion purposes. It must be reviewed and finalized by qualified fund formation counsel before execution."
5. Highlight any validation warnings or items requiring counsel attention
6. Suggest: "Run `/fund review-lpa` on the original LPA with this amendment to verify the combined effect of the changes."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No LPA provided | Ask user to provide the original LPA document |
| No changes described | Prompt user with the common amendment types list and ask them to describe desired changes |
| LPA section not found | If the user references a section that cannot be located, ask for clarification; draft the amendment clause based on the described intent and flag for counsel review |
| Approval mechanism unclear | Draft the amendment with a placeholder for the approval recital; flag for counsel to confirm the required approval |
| Multiple conflicting changes | Present the conflicts to the user; ask for prioritization; draft the amendment reflecting the user's chosen resolution |
| Prior amendments exist but text unavailable | Note in the preamble that prior amendments exist; flag for counsel to confirm the amendment chain |
| Change requires LP supermajority | Warn the user that the requested change likely requires supermajority LP approval, which may be difficult to obtain; proceed with drafting |
| Change may trigger side letter provisions | Warn that the amendment may interact with side letter MFN clauses or other side letter provisions; recommend reviewing side letters before executing |
| Governing law uncertain | Default to Delaware for US funds, Cayman Islands for offshore funds; flag for counsel confirmation |
