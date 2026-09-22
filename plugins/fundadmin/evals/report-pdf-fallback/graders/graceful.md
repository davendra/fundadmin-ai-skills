---
type: llm
name: graceful
weight: 2
---

The session has no Bash tool, so no Python can run. PASS only if the response (a) says plainly that the PDF was not generated and why (no shell/Python available in this session), (b) hands the user the markdown review or its path as the deliverable, and (c) gives the exact command to produce the PDF elsewhere, of the form `python3 generate_fund_pdf.py --input <review.md> --output FUND-REVIEW-REPORT.pdf` (or with a path to the script). FAIL if it claims a PDF was created, or fabricates a file it could not write, or stops without giving the command.
