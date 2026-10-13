# Quick start

<img class="figure" src="/images/quick-start.webp" alt="Your first run: install the plugin, review a sample LPA, read the scored report" />

You need the plugin [installed](/guide/install) and a fund document. If you do not have one to hand, the plugin repository ships [24 synthetic samples](/guide/samples):

```bash
git clone --branch fundadmin--v1.3.2 --depth 1 https://github.com/davendra/fundadmin-ai-skills.git
cd fundadmin-ai-skills
```

## The menu

In Claude Code or Cowork, type the menu command with no arguments:

```text
/fundadmin:fund
```

It lists every command with its arguments. Any command can be typed straight after it, or invoked as its own skill (`/fundadmin:fund-review-lpa <file>`). In Codex, name the skill: `$fund-review-lpa <file>`. In any host you can also share a document and say what you need; the matching skill is picked from its description.

## Three first runs

```text
/fundadmin:fund review-lpa samples/OBRELUND-LPA-QUICKSTART.pdf
```

The flagship. Five specialist agents review the agreement and draft findings that cite their clauses; the sample carries 10 planted issues. A full review takes a while and depends on your host, so start it and come back. See [the agents](/agents) for what happens in between.

```text
/fundadmin:fund review-capital-call samples/OBRELUND-CAPITAL-CALL-1.pdf
```

Checks the arithmetic, the deadline and the wire instructions against the LPA terms.

```text
/fundadmin:fund wire-verify samples/email-wire-change-suspicious.md
```

Reads a wire-instruction change request, flags bank or beneficiary changes and missing callback evidence, and drafts a masked verification checklist. It never approves a payment.

## Full LPA and PDF check {#full-lpa-and-pdf-check}

Use the eight-page **OBRELUND-LPA-QUICKSTART.pdf** synthetic sample first. In ChatGPT, select the installed `fund-review-lpa` skill using the picker and attach the sample. In a local task, supply its real file path. Complete the [host-specific installation and helper check](/guide/install) before starting.

Paste this request alongside the selected skill:

```text
Review the entire attached synthetic LPA, including all eight pages.
Use the installed fund-review-lpa workflow and a fresh isolated output run.
Retain the exact source and record its byte count and SHA-256.
Run terms first, then risk, compliance and obligations, then recommendations.
If named specialist agents are unavailable, read all five packaged agent
instructions and record that the stages ran inline in one model session.
No external applicability facts or current regulatory authorities are supplied.
Keep unsupported compliance checks UNKNOWN/UNAVAILABLE, compliance and the
aggregate score UNAVAILABLE, and the report PARTIAL. Do not invent inputs.
Use the packaged scoring and report helpers. Generate the PDF if the renderer
is available. Check its text, citations, tables, final limitations and layout.
Give me the Markdown, evidence JSON sidecar, PDF and retained audit bundle as
real files or download links. List anything that could not be generated.
Keep all existing and approved records unchanged. This is a synthetic draft
for qualified human review, not legal, payment or investment approval.
```

The five stages are specialist instructions, not five independent professional opinions. Some hosts execute them as separate agents; others use the documented inline fallback. Record which occurred.

A saved review should include the retained source, `run.json`, Markdown, evidence sidecar and scoring workpapers. PDF generation is automatic for an LPA review when the dependencies are available. If it was skipped, select `fund-report-pdf` with the **actual saved Markdown path**; do not recreate a report from a chat summary or overwrite an approved PDF.

Before sharing, open the PDF and check the beginning, source-linked findings, long tables and final limitations. Text extraction alone cannot prove the layout is readable. A table row may continue across pages; compare both parts. The bundled PDF is untagged, not PDF/UA. A `PARTIAL` report can have a valid PDF: missing regulatory evidence remains missing after export.

In cloud Chat mode, export the complete run as an audit ZIP and download it before the execution session expires. Files remain in the cloud task's environment until downloaded; local rendering language does not mean the work happened on your Mac. Your AI host and model provider process the document under their own terms.

## Where the output went

Each skill writes a markdown file under shared contract v1 (isolated run under the approved output root):

```text
reviews/
└── obrelund-capital-partners-fund-iii/
    └── 2026-09-21/
        └── <run-id>/
            ├── run.json
            ├── reports/<report-id>/   LPA-REVIEW-…, CAPITAL-CALL-REVIEW-…
            └── compliance/<report-id>/
```

Later skills build on earlier output: `report-pdf` turns a review into a PDF, `counsel-handoff` packages it for external counsel, `search-precedent` finds comparable terms across past reviews. The full list of folders and filename families is on the [output files](/guide/outputs) page.

## Next

- [All 60 commands](/commands/), grouped by category
- [The 5 agents](/agents) and how the score works
- [FAQ](/guide/faq) when something does not look right
