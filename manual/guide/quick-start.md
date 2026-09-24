# Quick start

<img class="figure" src="/images/quick-start.webp" alt="Your first run: install the plugin, review a sample LPA, read the scored report" />

You need the plugin [installed](/guide/install) and a fund document. If you do not have one to hand, the plugin repository ships [24 synthetic samples](/guide/samples):

```bash
git clone https://github.com/davendra/fundadmin-ai-skills.git && cd fundadmin-ai-skills
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
