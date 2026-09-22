# Changelog — fundadmin plugin

## Unpublished 1.1.0 candidate — second-review corrections

- Validate installer path components consistently before update checks and writes; reject unsafe aliases and hard-linked targets. Resolve selected release executables before directory changes.
- Separate capital-call risk blockers from descriptive scores; align eligible-pool allocation review with deterministic currency-unit rounding.
- Add bounded NAV-inclusive KS-PME, signed YTD reconciliation and capital-call status workpapers; remove contradictory financial interpretations.
- Share safe slug/filename generation between direct and routed skills; distinguish local candidates from the older public baseline and qualify host support.
- Exercise synthetic source-to-sidecar-to-Markdown-to-PDF workflows; require preserved, candidate-bound host evidence before actual publication. Offline test success is not host or professional approval.

All notable changes to the published plugin. The source repository
(`davendra/fundadmin-ai`) keeps the full project changelog.

## 1.1.0 — 2026-09-21 — Supervised-pilot release candidate

Local source candidate only; this entry does not establish publication.

- Nine deterministic Decimal calculation operations with reproducible workpapers,
  explicit rounding, conservative IRR ambiguity handling and bounded waterfall support.
- Supplied-screening-evidence validator with freshness, coverage, identity and
  conflict checks; it never performs live screening or grants clearance.
- Dated 30-entry regulatory source register, including failed retrievals; stale
  blanket rules replaced by source- and jurisdiction-dependent checks.
- PDF exporter preserves non-LPA content and unknown score states, renders real
  tested tables, creates private files exclusively and refuses output collisions.
- Revision-aware intake/matching instructions, shared masking rules, safer installer,
  transactional generated builds, source fingerprints and expanded test/eval gates.

- Review and draft support requiring human review, not certified production operation.
  Live host, connector and external operational qualification is not tested by the
  local report/helper contracts. See `docs/production/README.md` for release limits.
- Shared contract v1 applies to all 63 skills, whether invoked directly or routed.
  Python 3.9+ standard-library helpers create isolated runs, validate evidence
  sidecars and record source/output SHA-256 hashes. Reports live under
  `reviews/<fund>/<date>/<run-id>/<subfolder>/<report-id>/<filename>`; no output
  beside inputs or in the working-directory root, and no report overwrite.
- LPA methodology v2 runs terms first, then risk/compliance/obligations in parallel,
  then recommendations. Raw weights 20/25/20/15 over 80 normalise to
  25/31.25/25/18.75%; recommendations carry zero weight. Unknown dimensions make
  the aggregate unavailable. Coverage confidence is separate from heuristic
  document favourability; the legacy Safety Score name is not a safety verdict.
- Generated docs remove investment/admission verdicts and obsolete LPA/onboarding
  image embeds, describe specific connector dependencies and host/provider data
  flows, and expose capability/maturity fields for every catalogue entry.
- Optional PDF dependencies are pinned in `requirements-plugin.txt`. Plain-skill
  installation uses a reviewed local source checkout of `plugin-release`; no
  remote shell script is piped into a shell. Existing host commands are retained.

The entries below describe historical releases, not current runtime guarantees.

## 1.0.2 — 2026-09-21

- New logo, "Quorum": a ring split in the LPA Safety Score weights
  (20/25/20/15/20) with the 25% risk arc in teal. Ships as the app icon
  (`assets/icon.svg`, `assets/logo.png`), a bare mark, and light and dark
  lockups used in the README header.
- The earlier `review-lpa` sequencing and duration claims are superseded by
  methodology v2 in 1.1.0; terms is a dependency and no duration is guaranteed.

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
- No bundled hooks or MCP servers; host/provider traffic and optional connector
  traffic still apply. This was not an offline-processing guarantee.
