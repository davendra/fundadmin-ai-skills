---
name: fund-report-pdf
description: "Renders the latest fund review as a branded PDF with score gauge, risk dashboard and priorities; needs Python and ReportLab. Use for `/fund report-pdf`. Writes FUND-REVIEW-REPORT.pdf."
---

# Professional PDF Report Generator — Fund Administration

You are the PDF report generator for `/fund report-pdf`. You collect data from the most recent fund document review analysis and generate a professional, branded PDF document using Python and ReportLab.

## When This Skill Is Invoked

The user runs `/fund report-pdf` after having completed a fund document review (via `/fund review-lpa`, `/fund waterfall-review`, `/fund review-ppm`, `/fund review-subscription`, `/fund review-side-letter`, or other analysis commands). You find the most recent analysis data, then generate a polished PDF report.

---

## Phase 1: Locate Analysis Data

### 1.1 Find the Most Recent Review

Search for the most recent fund review output file in the working directory. Look for files matching these patterns (in order of preference):

1. `LPA-REVIEW-*.md`
2. `PPM-REVIEW-*.md`
3. `SUBSCRIPTION-REVIEW-*.md`
4. `SIDE-LETTER-REVIEW-*.md`
5. `WATERFALL-REVIEW-*.md`
6. `AUDIT-SUPPORT-*.md`
7. `COMPLIANCE-REVIEW-*.md`
8. `KYC-REVIEW-*.md`
9. Any `.md` file containing "Safety Score" or "Completeness Score" or "Waterfall" in the context of fund analysis

Use the Glob tool to find matching files. If multiple matches exist, use the most recently modified file.

**If no analysis file is found:**
- Tell the user: "No fund review data found in the current directory. Please run `/fund review-lpa <file>` or another review command first, then run `/fund report-pdf` to generate the PDF."
- Do NOT proceed.

### 1.2 Parse the Analysis Data

Read the analysis file and extract:

| Data Point | Where to Find It |
|-----------|-----------------|
| **Score** | "LPA Safety Score: X/100" or "Completeness Score: X/100" or "Safety Score: X/100" |
| **Grade** | "Grade: [letter]" |
| **Fund name** | "Fund Name" row in details table |
| **Fund type** | "Fund Type" row in details table |
| **Parties / GP Entity** | "GP Entity" row or "Parties" row |
| **Vintage** | "Vintage" row in details table |
| **AUM / Fund Size** | "Fund Size" or "AUM" row |
| **Governing law** | "Governing Law" row |
| **Date** | From filename or "Date of Review" row |
| **Risk dashboard** | Risk category scores and assessments, or High/Medium/Low risk counts |
| **Provision analysis** | Each provision with risk level, description, and recommendation |
| **Missing protections** | "Missing LP Protections" or "Missing Protections" section |
| **Obligations** | "Obligations & Deadlines" table |
| **Compliance flags** | "Compliance Flags" section |
| **Waterfall summary** | "Waterfall & Economics Summary" or waterfall tier breakdown |
| **Negotiation priorities** | "Negotiation Priorities" numbered list |
| **Next steps** | "Recommended Next Steps" checklist |
| **Executive summary** | "Executive Summary" section |

---

## Phase 2: Prepare Input Data and Locate the PDF Script

### 2.1 Accept Markdown Review Output or Normalized JSON

The bundled Python helper accepts either:

1. the review Markdown file itself, or
2. a normalized JSON payload if you already have structured review data available.

If you need to pre-assemble the report data before calling the helper, write a temporary JSON file containing structured keys such as:

```json
{
  "score": 72,
  "grade": "B",
  "grade_label": "Acceptable",
  "details": {
    "fund_name": "Example Fund",
    "fund_type": "Private Equity",
    "gp_entity": "Example GP LLC",
    "aum": "$500M",
    "management_fee": "2.0% on commitments",
    "carry": "20%",
    "hurdle_rate": "8%",
    "fund_term": "10 years + 2 x 1 year extensions",
    "governing_law": "Delaware"
  },
  "executive_summary": "...",
  "risks": {
    "high": 2,
    "medium": 4,
    "low": 6,
    "high_provisions": "...",
    "medium_provisions": "...",
    "low_provisions": "..."
  },
  "provisions": [],
  "compliance_flags": [],
  "obligations": [],
  "negotiation_priorities": [],
  "next_steps": []
}
```

Use normalized JSON only when you need to override or pre-assemble the review data yourself. Otherwise, prefer passing the review Markdown file directly and let the helper normalize it internally.

### 2.2 Look for Existing Script

Search for the PDF generation Python script in these locations (in order); stop at the first one that exists:

1. `${CLAUDE_PLUGIN_ROOT}/skills/fund/scripts/generate_fund_pdf.py` — the copy that ships with the `fundadmin` plugin. If that variable appears unexpanded in this text, the host does not substitute it; move on.
2. `../fund/scripts/generate_fund_pdf.py` relative to this skill's own base directory (the plugin layout and the `install.sh` layout both place the `fund` skill next to this one)
3. `~/.claude/skills/fund/scripts/generate_fund_pdf.py` (where `install.sh` puts it)
4. `[working directory]/fundadmin-ai/scripts/generate_fund_pdf.py`
5. `[working directory]/scripts/generate_fund_pdf.py`
6. `../scripts/generate_fund_pdf.py` (one level up from working directory)

If none exist, use the Glob tool to search for `**/generate_fund_pdf.py` within the project.

**If `python3` is not available in this host** (for example a Cowork session without a Python runtime), or ReportLab cannot be installed, do not attempt Phase 4 either: deliver the review Markdown file you located in Phase 1, tell the user plainly that the PDF was not generated and why, and give them the exact `python3 generate_fund_pdf.py --input <review.md> --output FUND-REVIEW-REPORT.pdf` command to run on a machine that has Python.

### 2.3 If Script Found

Run the script, passing it either the review Markdown file or the normalized JSON file:

```bash
python3 [script_path] --input [analysis_input_path] --output FUND-REVIEW-REPORT.pdf
```

The script also preserves the legacy positional interface for backwards compatibility:

```bash
python3 [script_path] [analysis_input_path] [output.pdf]
```

### 2.4 If Script Not Found — Generate Inline

If no script is found, generate the PDF directly using inline Python with ReportLab. Write and execute a Python script that produces the PDF.

**First, check that ReportLab is installed:**

```bash
pip3 install reportlab 2>/dev/null || pip install reportlab 2>/dev/null
```

Then generate and execute the following Python script. The script MUST produce a professional PDF with all elements described in Phase 3.

---

## Phase 3: PDF Content and Layout Specification

The generated PDF MUST include all of the following sections with professional styling.

### 3.1 Page Setup

| Property | Value |
|----------|-------|
| Page size | Letter (8.5" x 11") |
| Margins | 0.75" all sides |
| Font family | Helvetica (built into ReportLab) |
| Primary color | #1a365d (dark navy) |
| Accent color | #2d5f8a (medium blue) |
| High risk color / Danger | #e53e3e (red) |
| Medium risk color / Warning | #d69e2e (amber) |
| Low risk color / Success | #38a169 (green) |
| Background | White (#ffffff) |
| Table header bg | #1a365d (dark navy) |
| Table header text | White (#ffffff) |
| Table alt row | #f0f4f8 (light blue-gray) |
| Section header underline | #2d5f8a (accent color) |

### 3.2 Cover Page

The cover page MUST include:

```
[Top: Thin colored bar across full width in primary color #1a365d]

FUND DOCUMENT REVIEW REPORT
[Large, bold, primary color, centered]

[Subtitle: Fund type or "Comprehensive Fund Document Analysis"]

[Large circular score gauge graphic — see 3.3]

Fund Safety Score: [SCORE]/100
Grade: [LETTER] — [LABEL]
[Color-coded based on score: red for F/D, amber for C, green for B/A/A+]

Fund: [Fund Name]
Prepared: [today's date]

[Bottom of page:]
DISCLAIMER: This analysis is AI-generated and does not constitute
legal, tax, or investment advice. Always consult qualified professionals.

[Thin colored bar at bottom in primary color]
```

### 3.3 Score Gauge Graphic

Draw a semi-circular gauge (speedometer style) using ReportLab drawing primitives:

- Semi-circle arc from 0 to 180 degrees
- Color gradient: red (left) to yellow (center) to green (right)
- Needle pointing to the score position
- Score number displayed large and centered below the gauge
- Grade letter displayed below the score

Implementation approach using ReportLab:
```python
from reportlab.graphics.shapes import Drawing, Wedge, String, Line
from reportlab.graphics import renderPDF
from reportlab.lib.colors import Color
import math

# Create a drawing for the gauge
# Use Wedge shapes for the colored arc segments
# Use Line for the needle
# Use String for the score text
```

If the gauge is too complex to render reliably, fall back to a large color-coded score box:
```
+----------------------------------+
|     FUND SAFETY SCORE            |
|                                  |
|           72 / 100               |
|          Grade: B                |
|        (Acceptable)              |
+----------------------------------+
```
Color the box border and score text based on the grade.

### 3.4 Fund Details Page

```
FUND DETAILS
[Section header with colored underline in #2d5f8a]

[Executive Summary — 3-4 sentence overview]

FUND INFORMATION
[Table with alternating row colors:]
| Field             | Value                 |
| Fund Name         | [name]                |
| Fund Type         | [PE/VC/RE/etc.]       |
| GP Entity         | [GP name]             |
| Fund Size         | [target / hard cap]   |
| Vintage           | [year]                |
| Management Fee    | [rate on basis]       |
| Carried Interest  | [rate]                |
| Preferred Return  | [rate, compounding]   |
| Fund Term         | [years + extensions]  |
| Commitment Period | [years]               |
| Governing Law     | [jurisdiction]        |
```

### 3.5 Risk Dashboard Page

```
RISK DASHBOARD
[Section header with colored underline]

[Color-coded risk summary boxes in a row:]
+------------+  +------------+  +------------+
| HIGH RISK  |  | MED RISK   |  | LOW RISK   |
| #e53e3e bg |  | #d69e2e bg |  | #38a169 bg |
|    [n]     |  |    [n]     |  |    [n]     |
+------------+  +------------+  +------------+

[Risk category table (if available from LPA review):]
| Risk Category    | Score (1-10) | Assessment            |
|------------------|-------------|------------------------|
| Fee Risk         | [X]         | [summary]              |
| Liquidity Risk   | [X]         | [summary]              |
| Governance Risk  | [X]         | [summary]              |
| Regulatory Risk  | [X]         | [summary]              |
| Operational Risk | [X]         | [summary]              |
| GP-LP Asymmetry  | [X]         | [summary]              |
| Key Person Risk  | [X]         | [summary]              |
| Clawback Risk    | [X]         | [summary]              |

OR (if from other review types):

[Risk matrix table:]
| Risk Level | Count | Provisions Affected         |
|------------|-------|-----------------------------|
| High       | [n]   | [provision1], [provision2]   |
| Medium     | [n]   | [provision1], [provision2]   |
| Low        | [n]   | [provision1], [provision2]   |
```

Use colored squares or rectangles with the specified colors for risk level indicators.

### 3.6 Provision-by-Provision Analysis Pages

For EACH provision analyzed, create a structured entry:

```
[Risk level color bar on left margin]

PROVISION: [Provision Name] — Section [X.X]
Risk Level: [HIGH / MEDIUM / LOW]

What it says:
[plain English summary]

Why it matters:
[risk explanation with GP-LP dynamics context]

Financial exposure:
[quantified impact — bps, dollars, or percentage]

Market standard:
[what comparable funds typically provide]

Recommended change:
[specific alternative language]

[Separator line]
```

Group provisions by risk level: all High Risk first, then Medium, then Low.

### 3.7 Compliance Flags Section

```
COMPLIANCE FLAGS
[Section header]

[List of regulatory or jurisdictional concerns identified]
- SEC / Investment Advisers Act issues
- ERISA plan asset concerns
- FATCA/CRS classification issues
- AML/KYC gaps
- Jurisdictional enforceability concerns
```

### 3.8 Obligations Timeline

```
OBLIGATIONS & DEADLINES
[Section header]

[Table:]
| Obligation | Responsible Party | Trigger / Deadline | Consequence |
|------------|-------------------|-------------------|-------------|
| [obligation] | [GP/LP]        | [when]            | [what happens] |
```

### 3.9 Negotiation Priorities

```
NEGOTIATION PRIORITIES
[Section header]

1. [HIGHEST PRIORITY]
   Current: [what the provision says now]
   Proposed: [specific language to propose]
   Market justification: [why this is reasonable]

2. [SECOND PRIORITY]
   ...

3. [THIRD PRIORITY]
   ...
```

Number and rank all priorities. Use bold for the priority title.

### 3.10 Next Steps Checklist

```
RECOMMENDED NEXT STEPS
[Section header]

[ ] [First action]
[ ] [Second action]
[ ] [Third action]
[ ] Engage qualified fund formation counsel before executing subscription documents
```

### 3.11 Legal Disclaimer (Final Page)

```
DISCLAIMER

This document was generated by an AI-powered fund document analysis tool.
It does NOT constitute legal, tax, financial, or investment advice and
should not be relied upon as such. The analysis is based on automated
text interpretation and may not capture all nuances of the fund documents,
applicable law, or market context.

ALWAYS consult qualified professionals before:
- Making capital commitments to any investment fund
- Negotiating fund document terms
- Making decisions based on this analysis
- Taking any action that could have legal or financial consequences

This report is provided for informational and educational purposes only.
The creators of this tool accept no liability for actions taken based
on this analysis.

Generated: [date and time]
Tool: AI Fund Administration Assistant — Claude Code
```

### 3.12 Page Footer (All Pages Except Cover)

Every page after the cover should have:

```
[Left: "AI Fund Administration Assistant — Fund Review Report"]
[Center: "CONFIDENTIAL"]
[Right: "Page X of Y"]
```

Use a thin line above the footer to separate it from content.

---

## Phase 4: Generate the PDF

### 4.1 Write the Python Script

Write a complete Python script that:

1. Reads the review Markdown file or normalized JSON file
2. Parses markdown sections using string matching / regex, or uses normalized JSON fields directly
3. Builds the PDF page by page using ReportLab
4. Includes all sections from Phase 3
5. Uses professional styling with the fund admin color palette (#1a365d, #2d5f8a, #e53e3e, #d69e2e, #38a169)
6. Handles missing sections gracefully (skip if data not found)

### 4.2 Execute the Script

Run the script using Bash:

```bash
cd [working directory] && python3 /tmp/generate_fund_pdf.py --input "[analysis_input_path]" --output "FUND-REVIEW-REPORT.pdf"
```

### 4.3 Verify Output

After execution:
1. Check that the PDF was created successfully
2. Verify the file size is reasonable (should be >10KB for a real report)
3. Report any errors to the user

---

## Phase 5: Present to User

After generating the PDF:

1. Confirm the PDF was generated: "PDF report generated: `FUND-REVIEW-REPORT.pdf`"
2. State the file location (absolute path)
3. Summarize what is in the report (sections included, page count if known)
4. Note: "Open the PDF to review the full formatted report with the score gauge, risk dashboard, and provision-by-provision analysis."
5. If any sections were missing from the source data, note which sections were skipped and why.

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| ReportLab not installed | Run `pip3 install reportlab` and retry |
| No analysis file found | Tell user to run `/fund review-lpa` or another review command first |
| Analysis file unreadable | Report the error, ask user to verify the file |
| PDF generation fails | Show the error, attempt to fix, retry once |
| Script not found and inline generation fails | Provide the markdown analysis as fallback and explain the PDF could not be generated |
| Python not available | Report that Python 3 is required for PDF generation |
