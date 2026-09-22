# Changelog — fundadmin plugin

All notable changes to the published plugin. The source repository
(`davendra/fundadmin-ai`) keeps the full project changelog.

## 1.0.8 — 2026-09-22

- The manual now points to the new contact form on fundadmin.dev from its
  navbar, footer, FAQ and privacy page, replacing links to GitHub issues
  that visitors could not open while the repositories are private. The
  privacy page covers fundadmin.dev and what the form collects.

## 1.0.7 — 2026-09-22

- `LICENSE` is now the plain MIT text. It used to carry the source
  repository's scope paragraph, which named folders and a second license
  that are not in this repository. The README's License section says what
  the license covers: everything here.
- The Codex manifest's privacy link pointed at a README anchor that did not
  exist. It now points at a new privacy page in the manual, which says what
  the plugin and the manual site do and do not send anywhere, including
  that a skill given a URL asks the host to fetch it.

## 1.0.6 — 2026-09-22

- Manual: figures for the quick start, output files and sample documents
  pages, and a new social preview card in the same style (the old card was
  from the previous site and quoted a 60-second review).

## 1.0.5 — 2026-09-22

- Manual: every command category now opens with an illustration in the
  README style, eleven new ones drawn for the categories that had none
  (drafting, compliance, reporting, negotiation, tracking, analytics,
  investor operations, portfolio, knowledge base, cross-document analysis,
  ESG and tax).

## 1.0.4 — 2026-09-22

- Manual redesign: a navy and teal theme with IBM Plex type and a navy dark
  mode, the Quorum ring as the home mark, category icons on the home page and
  command index, the LPA pipeline, batch intake and onboarding graphics on
  their category pages, and on the agents page a weights ring and grade scale
  drawn from the same numbers as `catalog.json`.

## 1.0.3 — 2026-09-21

- A user manual, published at https://help.fundadmin.dev and shipped in this
  repository under `manual/`. The command reference (one page per category,
  every command with its arguments, hosts and output file), the agents page
  and the output-files page are generated from the same data as
  `catalog.json`. The README graphics moved from `docs/images/` to
  `manual/public/images/`.
- Shorter skill and agent descriptions. Every session loads all 63 skill
  descriptions and the 5 agent descriptions, so they were trimmed to 200
  characters or fewer (about 18,000 characters down to under 12,000) while keeping
  what matters for choosing a skill: what it does, its `/fund` command, and the
  file it writes. The contract suite now enforces the limit.

## 1.0.2 — 2026-09-21

- New logo, "Quorum": a ring split in the LPA Safety Score weights
  (20/25/20/15/20) with the 25% risk arc in teal. Ships as the app icon
  (`assets/icon.svg`, `assets/logo.png`), a bare mark, and light and dark
  lockups used in the README header.
- `review-lpa` runs the four independent agents in parallel, waits, then runs
  the recommendations agent on their results, and writes the report once with
  the final score. A headless run had previously saved a draft with score
  placeholders while the last agent was still working. It also tells the user
  up front that a full review takes 15–40 minutes.

## 1.0.1 — 2026-09-21

- Adds `samples/`: 24 synthetic documents for one fictional fund family, each mapped
  in `samples/README.md` to the command to run and the issues planted in it (two
  clean controls included), so the skills can be tried right after installing.
- Orchestrator output list names the `PRECEDENT-SEARCH-*` and `COUNSEL-HANDOFF-*`
  families; eval cases tuned.

## 1.0.0 — 2026-09-21

First public release as a plugin for Claude Code, Claude Cowork and Codex.

- 62 `/fund` skills plus the `fund` orchestrator, packaged with the 5 LPA-review
  agents, the ReportLab PDF script and 6 output templates.
- Every skill now carries trigger-style frontmatter so hosts auto-invoke the
  right one when a fund document is shared; nine skills that previously had no
  frontmatter at all gained it.
- Skill names match their directories in every host (`fund-review-lpa`, not
  the old internal aliases).
- `review-lpa` uses the packaged agents by name and falls back to running the
  five prompts inline on hosts without subagents.
- `report-pdf` finds the packaged script first and degrades to the markdown
  report when Python is unavailable.
- `search-precedent` works from local review files when no vault MCP is present;
  `counsel-handoff` gained a full phase structure and output package.
- No hooks, no MCP servers, no network calls.
