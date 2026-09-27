# Changelog — fundadmin plugin

All notable changes to the published plugin. The private source repository
(`davendra/fundadmin-ai`, maintainers only) keeps the full project changelog.

## 1.3.2 — 2026-09-27

- **Host-evaluation evidence:** see `docs/production/verification.md` for this
  release's status. Evidence is recorded there, not here, because this file is
  part of the candidate the evidence is bound to.
- Capital-call and distribution reviews no longer fail a notice for a rounding
  difference its own stated method explains. When the notice states how an
  amount was derived (for example an expense true-up as each investor's share
  of the cumulative total less the amount already called), that method
  reproduces every amount exactly, and each investor differs from a direct
  pro-rata split by at most one currency unit, netting to zero, the review
  records a method note instead of a FAIL: no High Risk flag, no score cap.
  Any other difference still fails, with no blanket allowance. The fee audit
  and the draft capital call follow the same rule.
- `fund_screening.py` treats placeholder scope metadata as missing. A list
  scope, jurisdiction or subject such as `UNKNOWN`, `N/A` or
  `list-scope-not-supplied`, a placeholder identity link, or a freshness limit
  set to the 3660-day ceiling makes the check INCOMPLETE (identity linkage or
  freshness NOT ASSESSED), never NO MATCH REPORTED. The KYC skills say not to
  invent scope values to get a file past validation.
- Shipped samples: reference prefixes left over from the old fund names are
  gone (Obrelund documents use `OBRL-`, the Kirrowyn wire-change email
  `KRWN-`); Fund III documents are signed by Jonathan R. Whitmore, the LPA
  signatory, rather than a GP principal who shares a surname with an investor;
  notices no longer carry an agreement's "IN WITNESS WHEREOF" line; and the
  capital-call email now matches the USD 575M fund, its call sequence and the
  account on file.
- Eval suite fixes. The review-lpa issue check no longer accepts a bare
  "exclusion" for the key-person and excuse theme, and the wire-readiness
  check accepts a plain "No." to the override question while still rejecting
  approval language.

## 1.3.1 — 2026-09-26

- **Host-evaluation evidence** was recorded in
  `docs/production/verification.md` at publication (27 September 2026): all 18
  saved installed-plugin cases passed on the pinned Claude Code 2.1.278
  against the published candidate, two after a disclosed retry.
- Shipped sample documents fixed. Answer keys no longer appear inside the
  documents (no `[ISSUE: ...]` notes, red-flag comments or fraud-indicator
  banners); each planted issue is visible in its own document instead: the
  ERISA subscription states its 24.9% benefit-plan participation, and capital
  call 1 shows the account on file next to the new bank details. Clean controls
  are genuinely clean: their fee lines, uses of funds and per-investor columns
  now add up.
- PDF reports render wide tables as labelled records with thin separators
  instead of a run of column names joined by `|`, and Markdown horizontal rules
  (`---`, `***`) are drawn as rules instead of printed as text.
- The KYC tracker workbook is bound to its report: `fund_kyc.py xlsx-spec
  --report` records the report's hash and copies its tables, documents the grid
  does not decide show INCOMPLETE rather than a bare N/A, report-listed open
  items reach the workbook, and `fund_report.py companion` refuses a KYC spec
  that is not bound to that exact report revision.
- `fund_report.py validate` and `write-report` now say which field broke which
  rule, for example `findings[0].id (finding id) contains uppercase letters; it
  must match ^[a-z0-9][a-z0-9-]{0,79}$`, instead of a bare "invalid input". The
  message names the field and never repeats a value from the report.
- Eval suite fixes. The capital-rounding allocation check no longer reads a
  percentage column (`33.3333%`) as an investor's amount. Evidence runs now
  grant each case only the gated tools its `allowed_tools` lists (one
  invocation per case) instead of Bash, Write and Edit for every case.

## 1.3.0 — 2026-09-23

- **Host-evaluation evidence** was recorded in
  `docs/production/verification.md` after publication (24 September 2026):
  all 18 saved installed-plugin cases passed on the pinned Claude Code 2.1.278
  against the published candidate, one after a disclosed retry. When this
  entry was written the evidence was still pending.
- Obsidian support is retired. The `vault-init` and `vault-sync` skills are
  removed (60 skills now), and the menu, `ingest`, `search-precedent` and
  `counsel-handoff` no longer offer vault steps: every review is saved in its
  local run folder, and precedent search reads the local `reviews/` tree. The
  source repository keeps the retired code under `archive/`.
- Report PDFs are readable. Headings, lists, block quotes and bold, italic and
  inline code are typeset; severity and checkbox symbols print as `HIGH`,
  `MEDIUM`, `LOW` and `[ ]` instead of `[U+1F534]`-style markers. Source HTML
  and unmapped glyphs still stay visible.
- `review-lpa` asks once, without blocking, for the four facts that decide
  regulatory applicability: adviser status, offering route and fund exclusion,
  investor mix, and marketing jurisdictions. Answers are passed to every agent
  as user-supplied facts. Without them, or in an unattended run, the compliance
  dimension stays unavailable and no aggregate score is issued. With them, a
  compliance point can be assessed only when the facts and a registered authority
  are available; points with no authority on file stay UNKNOWN.
- Every review report (each `*-REVIEW` family) opens with a ranked **Key Issues
  and Asks** table: each issue with its source locator, direct effect and a
  proposed stance (push, trade or accept). A stance is a negotiation or
  remediation position, never an investment, admission, payment or compliance
  verdict.
- Readiness (HOLD, ESCALATE, PRELIMINARY READY FOR HUMAN REVIEW) now maps to one
  report status, so the report body and its evidence sidecar agree.
- Every saved report, PDF and Excel companion notes how the content was handled
  and reminds the reader to check the source documents' confidentiality terms
  before using an AI tool on them. The manual's privacy page covers this too.
- Release-blocker fix pass after a pre-release review: unsourced "market"
  comparisons, percentiles, grades and verdict fields (commit/decline, clean or
  qualified opinions, "compliant") were removed from skills, agents and
  templates in favour of cited sources or neutral evidence states; figures go
  through the packaged calculation helper or are marked uncalculated;
  recommendation slots in board memos are left for the GP; drafting skills
  separate a review cover from the sendable text; intake routes every wire
  instruction to `wire-verify`, checks email authentication headers when present
  and decodes attachments locally; the filename catalogue now lists every family
  the helper produces; and new guard tests keep these from coming back.
- KYC routing is stricter. `fund_kyc.py` now checks that screening evidence
  covers the record's own subject, every required owner and controller, and is
  not older than the record, so evidence for another investor or a stale search
  can no longer lead to PRELIMINARY READY. It also checks identity flags and
  W-8/W-9 validity (a W-8 runs to 31 December of the third year after signing),
  and reports document completeness. `aml-screen` can no longer report NO MATCH
  without the helper.
- Rules brought up to date with 2025–2026 sources, each cited and dated in the
  skill: the Rule 506(c) minimum-investment verification route and the qualified
  purchaser (C) exclusion; 2025 K-1 Box 19 codes and K-3 requests; Rev. Proc.
  2025-32 199A values; amended CRS and CARF; OFAC sham-transfer red flags; ILPA
  NAV-facility, org-expense and (draft) continuation-vehicle positions as
  discussion points; ILPA Reporting Template v2 fee lines; returns labelled with
  and without the subscription line; Form PF, Reg S-P, AIFMD II, SFDR 2.0 and UK
  SDR dates in the regulatory calendar, with 17 new source-register entries.
  MFN eligibility now follows each clause's tier test; investor powers of
  attorney are reviewed against their own profile.
- `monitor-email` moves into Document Intake (13 categories), and its menu line
  now says what it does: a read-only mailbox check that stages attachments in an
  isolated run, with no automatic processing. Public counts are corrected to 60
  commands, 61 skills including the `fund` menu, and 7 packaged scripts.
- An unlabelled numeric score in a PDF request is now labelled "LPA document
  favourability (heuristic, methodology v2)" rather than "LPA Safety Score".

## 1.2.0 — 2026-09-22

- **Published without host-evaluation evidence.** The installed-plugin eval
  cases were not run against this candidate; the offline contract, helper and
  validation suites were. Host behaviour is unverified for this release. See
  `docs/production/verification.md`.

1.1.1 was never published. Its changes ship in this release and are listed
after the new work.

- KYC routing. `kyc-review`, `aml-screen` and `kyc-tracker` now read the
  onboarding documents into a structured record first (in a separate Explore
  subagent where Claude Code has one, inline otherwise, and the report says
  which), then `fund_kyc.py` applies the firm's own rules grid and any supplied
  screening evidence. The result is a risk rating, a document matrix, one outcome
  per rule and a disposition for a person to act on: ESCALATE FOR EDD, REQUEST
  DOCUMENTS, HOLD or PRELIMINARY READY FOR HUMAN REVIEW. Nothing admits, rejects
  or clears an investor. Without a firm grid nothing is scored and the result is
  HOLD; the shipped example grid shows the structure and caps every result at
  HOLD. `investor-onboard` takes its document checklist from the grid,
  `fatca-crs-classify` starts from the record's tax forms, and
  `subscription-process` reads the disposition as returned.
- `aml-screen` can run checks through a screening provider connector the firm has
  approved, when the user authorises sending the subjects' details to it; without
  one, checks stay NOT PERFORMED.
- KYC reviews and the KYC tracker save an Excel workbook beside the report (a CSV
  when openpyxl is not installed). So do `review-capital-account`, `reconcile`,
  `fee-audit`, `waterfall-review` and `obligation-tracker`: their workbook is the
  report's own tables, one sheet each, copied as written and never recalculated.
- Four new host eval cases: `kyc-disposition`, `kyc-reader-injection`,
  `kyc-no-grid` and `kyc-tracker-xlsx` (18 in all).
- `fund_xlsx.py`, a spreadsheet companion helper: a review's tables as an
  `.xlsx` workbook (openpyxl) or a CSV file, written beside the Markdown report
  with its own sidecar. It never writes formulas, and without openpyxl it says so
  instead of writing a workbook.
- The user manual (https://help.fundadmin.dev) is generated from the plugin
  source again and ships in `manual/`, so a release can no longer drop it.
  Its agents and output-files pages describe methodology v2 and the shared
  contract v1 run layout; the letter-grade scale and the 1.0 LPA-pipeline and
  onboarding figures are gone. README graphics live in
  `manual/public/images/` (not `docs/images/`), and the README links the
  manual's privacy page.
- Brings in the fixes made directly on this repository after 1.1.0 (#1, #2,
  #5–#8): skill write paths aligned with shared contract v1; `report-pdf`
  recognises capital-call, distribution and K-1 reports; corrected filename
  labels for `wire-verify`, `ingest` and `report-pdf`; firmer trigger wording
  so the bare `/fundadmin:fund` menu and `wire-verify` load their skills; the
  eval-fixture workflow (`.github/workflows/evals.yml`) and its structural
  tests. They now come from the source repository, so the next release keeps them.
- Gate-3 eval graders: deterministic regex prechecks for the capital-rounding,
  privacy-mask and review-lpa cases, JavaScript-compatible regex flags, and
  the menu case counts a `/fundadmin:fund` slash invocation as the skill firing.
- The contract suite caps skill descriptions at 320 characters (the menu
  skill's at 1,024) instead of 1.0.3's 200, and keeps the manual, licence and
  Codex-link checks.
- Installation guidance is now one hierarchy, in the README, the manual and
  `catalog.json`: the plugin marketplace for Claude Code and Cowork
  (recommended), a workspace marketplace import pinned to the reviewed release
  tag for Codex and ChatGPT teams, and third-party skill installers described
  accurately as developer compatibility that copies selected raw skill files
  and neither the agents, the metadata nor the report helper. The manual no
  longer tells anyone to pipe a remote script into a shell, and the README no
  longer claims the marketplace serves an older baseline than the release it
  ships in. New page: `docs/production/installation-and-release-channels.md`
  (what `main` is, immutable `fundadmin--vX.Y.Z` tags, what a pilot pins and
  records, one installation method per environment).
- Descriptions and the `/fund` menu state the real boundary. Wording that
  claimed screening, clearance, certification, eligibility determination,
  admission, filing submission, payment approval or a market-standard verdict
  is replaced by what the skills do: review supplied evidence, recompute
  arithmetic, draft documents, record checks as incomplete or not performed.
  The doc-only overrides that used to patch this downstream are gone, so the
  menu a user sees and the published catalogue now say the same thing, and a
  contract test fails if a claim comes back.

## 1.1.0 — 2026-09-21 — Supervised-pilot release candidate

Published as `fundadmin--v1.1.0` on 2026-09-22. Second-review corrections included in it:

- Validate installer path components consistently before update checks and writes; reject unsafe aliases and hard-linked targets. Resolve selected release executables before directory changes.
- Separate capital-call risk blockers from descriptive scores; align eligible-pool allocation review with deterministic currency-unit rounding.
- Add bounded NAV-inclusive KS-PME, signed YTD reconciliation and capital-call status workpapers; remove contradictory financial interpretations.
- Share safe slug/filename generation between direct and routed skills; distinguish local candidates from the older public baseline and qualify host support.
- Exercise synthetic source-to-sidecar-to-Markdown-to-PDF workflows; require preserved, candidate-bound host evidence before actual publication. Offline test success is not host or professional approval.

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
