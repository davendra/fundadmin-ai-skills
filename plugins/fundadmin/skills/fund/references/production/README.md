# Production readiness and operator guide

## Release status

Version 1.3.3 is a **supervised release candidate**, not approval for unattended fund administration. The plugin supplies instructions and bounded local helpers; the host controls model execution, access and tools. Automated tests do not certify legal accuracy, investor eligibility, sanctions clearance, tax classification or payment safety.

The scope of this hardening is the skills/plugin distribution. The source repository's commercial web applications, MCP server and deployment infrastructure require their own security, tenancy, authentication, backup and operational reviews before production use.

## Known limitations in 1.3.3

The reviewer of the 1.3.2 release runs recorded three notes on cases that passed (see [verification.md](verification.md)). 1.3.3 does not change those skills, so until a later release fixes them, treat them as limits:

- **`review-capital-account`:** a side remark on a year-to-date return can be wrong in the third decimal place. In the release run it stated −4.003% where −3.997% is correct. Check every derived return against the source figures before relying on it.
- **`kyc-review`:** with no KYC rules grid supplied, it suggested moving the review date to fit the evidence. Do not change a review date to fit the evidence; record the gap for the reviewer instead.
- **`performance-calc`:** the output was correct. The release check required the word "missing" or "absent" and rejected "not supplied", so the case passed on a disclosed retry. This needs a test fix, not a change in behaviour.

The sample pack covers two funds, not one; [`samples/README.md`](https://github.com/davendra/fundadmin-ai-skills/blob/main/samples/README.md) lists which document belongs to which.

## Supported modes and dependencies

| Capability | Support boundary | Requirement |
|---|---|---|
| Document review and drafting | Evidence-grounded draft; human review always required | Approved AI host and readable source documents |
| Audited report saving | Private run folders, source hashes, validated sidecars, no overwrite | Python 3.9+, `fund_report.py`, operator-controlled workspace |
| Numeric workpapers | Only documented supported operations; not arbitrary LPA interpretation | `fund_calculations.py`, explicit inputs and assumptions |
| LPA scoring | Heuristic methodology v2; unknown dimensions suppress aggregate | `fund_lpa_score.py`; no investment verdict |
| AML/KYC screening | Validation of supplied provider evidence; not a screening service | Approved current provider evidence and compliance review |
| Email workflows | Host connector-dependent; no implicit send/delete/write permission | Approved connectors and narrowly scoped access |
| PDF reports | Rendering of supplied report, not independent verification | Pinned ReportLab environment; source report retained |
| KYC routing | Rules-grid evaluation of an extracted record; routes to a person, never admits or clears | `fund_kyc.py`, the firm's own rules grid, supplied screening evidence ([kyc.md](kyc.md)) |
| Spreadsheet companions | The report's tables as `.xlsx` or CSV beside the report; no formulas, no new figures | `fund_xlsx.py`; openpyxl for `.xlsx`, CSV without it |

Detailed boundaries: [calculations](calculations.md), [LPA scoring](lpa-scoring.md), [regulatory](regulatory.md), [intake](intake.md), [PDF](pdf.md), [installation and release channels](installation-and-release-channels.md). Packaged `skills/fund/references/` contains the shared production and evidence contracts.

## Data handling

The helpers do not call network services. The AI host can transmit document content to model providers. Browsing, email and screening connectors can introduce additional destinations, permissions, logs and retention. Before using real data, the operator must approve providers, processing locations, contractual terms and access policies. Plugin instructions are not a technical data-loss-prevention system.

Use synthetic documents in CI and demonstrations. Mask bank and tax identifiers in reports, use investor reference IDs, and keep original identity evidence in approved restricted storage. The report helper creates new directories with mode 0700 and files with mode 0600; existing directory permissions and backups remain the operator's responsibility. Content hashes reveal neither authenticity nor ownership. Git ignore rules reduce accidental commits, but do not remove files already tracked and are not an access control.

Select a retention period with the business/data owner. Record the run ID, reason, approver and affected systems before deletion; include provider logs, backups and exported copies. Test recoverability and any legal hold requirements. No automatic destruction of originals or previous reports is provided.

## Installation and upgrade

User installation routes, release channels and what a supervised deployment pins and records are in [installation and release channels](installation-and-release-channels.md). This section covers the maintainer build and the plain-skills route.

Maintainers only: use a reviewed checkout of `main` in the private source repository (the release lineage since the 1.1.0 line was merged into it on 22 September 2026); do not execute an unreviewed remote shell script. Build the plugin with `python3 tools/build_plugin.py`. The generated `.fundadmin-generated.json` records a fixed source baseline commit plus SHA-256 hashes of actual working-tree inputs, so uncommitted changes are distinguishable without making the generated tree stale every time it is committed. The publishing commit separately records the exact source revision.

Create a virtual environment and install `requirements-plugin.txt` for build/PDF checks. Core evidence, calculation, score and screening helpers use the Python standard library; the spreadsheet companion needs `openpyxl` for `.xlsx` and falls back to CSV without it ([xlsx.md](xlsx.md)). For a plain skills installation, run the reviewed local `install.sh`; `FUNDADMIN_CLAUDE_DIR` can point to a dedicated test directory. An existing installation requires explicit `FUNDADMIN_ALLOW_UPDATE=1` and is backed up first. No real host installation is required to run the test suite.

## Verification and launch gates

1. Run `python3 tools/sync_production_policy.py --check` and `python3 tools/verify_production.py` from source.
2. Run `python3 tools/build_plugin.py --check`, then strict plugin/marketplace validation with the pinned CI CLI version. Confirm generated runtime tests pass too.
3. Run behavioural host evaluations, including missing screening evidence, injection, contradictory sources, numeric errors and missing PDF execution capability. Preserve model/host versions and traces privately. A prompt fixture or regex match alone is not behavioural evidence; inspect the response and tool trace.
4. A qualified fund administrator independently checks numeric golden cases and representative real-world structures. Compliance/legal/tax owners approve jurisdictional applicability and source freshness; assign an update owner.
5. Confirm provider coverage, credentials, outages, audit logs, access, privacy/retention, recovery and incident escalation with the intended deployment environment. Run a supervised acceptance test with redacted, approved cases and documented false-positive/false-negative review.
6. A named release owner signs off the exact source revision, generated input fingerprint and outstanding risks before publishing or deploying. Roll back by restoring the prior reviewed version and installation backup; retain run evidence.

`tools/publish_plugin.sh` defaults to build/validate only. Use `PYTHON_BIN` and `CLAUDE_BIN` to select the tested environment without altering global installations. Publication additionally requires a clean committed source checkout, `DRY_RUN=0`, an exact `PUBLISH_CONFIRM=owner/repository@version`, and `RELEASE_EVIDENCE` pointing to candidate-bound host evidence accepted by `tools/verify_release_evidence.py`. It appends to public history with an atomic, non-forced branch/tag push; existing release tags cannot be replaced. The dry run does not exercise remote publication or satisfy the behavioural evidence gate and is not a release approval.

## Candidate-bound behavioural evidence

Run installed-plugin evaluations with the pinned Claude Code 2.1.278 CLI, an explicitly selected model, `--keep-temp`, `--no-publish`, a bounded cost ceiling and only required local tools. Case `allowed_tools` alone does not grant gated tools (Bash, Write, Edit, WebFetch, `mcp__*`) to the operator session: the host command must pass `--allow-tools`, and without it `command_permissions.allowedTools` is empty and write/Bash cases fail. `--allow-tools` is one grant per invocation, though, so one run of the whole suite gives every case Bash, Write and Edit whatever its frontmatter says (the 1.3.0 evidence records this limitation). From 1.3.1, evidence runs group the cases by the gated tools their frontmatter allows and run each case as its own invocation (`--case` takes a single name glob) with exactly its group's grant plus `Skill Read Glob Grep`. `tools/gate3_eval_argv.py` holds that argv; `tools/run_gate3.sh` runs it:

```bash
CLAUDE_BIN=/path/to/claude-2.1.278 GATE3_MAX_COST_USD=5 tools/run_gate3.sh /private/gate3-<version>
python3 tools/make_release_evidence.py --results /private/gate3-<version>/*.json \
    --out /private/evidence-<version> --reviewer "<name>" [--attempt-notes attempts.json]
```

`run_gate3.sh` refuses any CLAUDE_BIN other than 2.1.278, a results directory inside the repository or one that is not empty. Each invocation runs with `--trust-plugin --keep-temp --no-publish -j 1 --judge-model haiku --runs 1 --ablation none` and writes `<dir>/<group>--<case>.json`, with its aggregate result under `<dir>/runs/` and HTML report under `<dir>/reports/`. `GATE3_MAX_COST_USD` (default 5) caps each invocation, not the suite. The eval sandbox refuses Bash-granting cases while `~/.docker` holds symbolic links, so the script moves `~/.docker` to `~/.docker.gate3-backup-<timestamp>` for the run and restores it on every exit, including failure and interruption; a `~/.docker` recreated meanwhile (OrbStack does this) is moved to `~/.docker.gate3-recreated-<timestamp>`, never merged or deleted. A failed case does not stop the run; the script exits non-zero and lists it. `make_release_evidence.py` merges the per-case files, requires every suite case exactly once, one host version, no partial or failed run and one resolved model, and records which results file each case came from. To use a retry, pass the retry's file instead of the failed one and disclose the earlier attempt in `--attempt-notes` (`{"case": "what happened"}`). The whole-suite command (every case granted Bash, Write and Edit) is still printed by `python3 tools/gate3_eval_argv.py` for development runs:

```bash
claude plugin eval plugin/plugins/fundadmin --trust-plugin --keep-temp --no-publish -j 1 --max-cost-usd 5 --judge-model haiku --allow-tools Bash Write Edit Skill Read Glob Grep
```

Do not enable real MCP servers or network tools for synthetic qualification. Preserve each actual response, trace and structured result in approved private storage outside generated build inputs. Record the resolved model identifier from the trace, not just an alias such as `sonnet`. Inspection of the actual output is separate from automated grader scores.

The evidence JSON uses `schema_version: 1`, `candidate_sha256` from `tools.build_plugin.provenance()['source_inputs_sha256']`, `host: "Claude Code"`, `host_version: "2.1.278"`, `resolved_model`, a timezone-aware `recorded_at`, and `scope: "synthetic-installed-plugin-smoke"`. Its `cases` must include each directory with `tools/plugin/evals/*/prompt.md`, once, with `name`, `passed: true`, `manual_review: {outcome: "pass", reviewer, notes}`, and hashed `artifacts` of kinds `result`, `trace` and `output`. Optional per-case fields `results_file` (directory/name and sha256 of the results file) and `attempt_note`, and a top-level `results_files` list, are recorded by `make_release_evidence.py` and ignored by the verifier. Each artefact has a non-empty relative `path` and `sha256`; parent traversal and symlinks are rejected. Evidence is not self-authenticating and this structure does not replace independent professional review.

Validate with `python3 tools/verify_release_evidence.py --input /absolute/private/evidence.json`. Missing cases, failed inspection, altered artefacts or a changed candidate fingerprint block qualification. Keep evidence outside `plugin/`, `tools/plugin/` and `docs/production/` to avoid a self-referential fingerprint. Freeze build inputs before evaluation; after a material change, obtain new evidence for the changed candidate. Offline CI tests the gate with synthetic fixtures but cannot certify a host run it did not execute.

Claude Code is the primary runtime qualification target. Codex and Cowork manifests are packaged, but installed runtime behaviour on those hosts remains experimental/unverified until separately tested. Direct/inline Codex smoke work does not establish installed-plugin equivalence. Linux/Python 3.12 CI is configured; require a recorded result for the exact candidate before claiming that platform tested. Single-trial cases are smoke tests, not statistical assurance or live-connector qualification.

Steps 4–6 require organisational decisions and cannot be replaced by this repository's tests. No live sanctions provider, email mailbox, customer record system or production payment system is qualified by the local test suite.

## Maintenance

Every material change to a skill, source rule, schema or helper requires targeted regression tests and regeneration. Do not edit `plugin/` by hand. Review primary regulatory sources before reliance and when an authority announces changes; stale or inaccessible evidence remains incomplete. Keep the source register dated, record breaking methodology changes, and treat prior scores as non-comparable unless explicitly recalculated under the same version.

Report security concerns privately through the contact form at [fundadmin.dev](https://fundadmin.dev/#contact) (choose "A question about FundAdmin Skills" and mark it security), with a minimal synthetic reproduction and no investor data. Triage unsafe output/path handling and fabricated clearance as release blockers. Do not place secrets or live documents in public issues.
