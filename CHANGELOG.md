# Changelog — fundadmin plugin

All notable changes to the published plugin. The source repository
(`davendra/fundadmin-ai`) keeps the full project changelog.

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
