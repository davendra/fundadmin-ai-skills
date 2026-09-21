# Changelog — fundadmin plugin

All notable changes to the published plugin. The source repository
(`davendra/fundadmin-ai`) keeps the full project changelog.

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
