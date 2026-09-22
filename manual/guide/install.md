# Install

The skills ship as one plugin, `fundadmin`, from the repository [`davendra/fundadmin-ai-skills`](https://github.com/davendra/fundadmin-ai-skills). The plugin marketplace is the supported route. Pick the one that matches how you work.

## Claude Code — Recommended

Recommended for individual supervised-pilot use.

```bash
claude plugin marketplace add davendra/fundadmin-ai-skills
claude plugin install fundadmin@fundadmin-ai-skills
```

Or inside a session: `/plugin marketplace add davendra/fundadmin-ai-skills`, then `/plugin install fundadmin@fundadmin-ai-skills`. Restart the session once to load it.

Check the install:

```bash
claude plugin details fundadmin@fundadmin-ai-skills
```

Expect 63 skills (the 62 commands plus the `fund` menu) and 5 agents, at the version shown in the footer of this site.

**Claude Cowork** installs the same plugin from the same marketplace through its interface: **Customize → Plugins → Add marketplace**, enter `davendra/fundadmin-ai-skills`, then install **FundAdmin AI**.

## Codex / ChatGPT Workspace — Team-managed

In a workspace, an administrator imports the marketplace once and sets the policy for the pilot group. Members do not each add a source.

1. Open **Workspace settings → Plugins → Add → Import marketplace**.
2. Enter `https://github.com/davendra/fundadmin-ai-skills`.
3. Select the reviewed immutable release tag, `fundadmin--v1.2.0`, rather than a branch.
4. Review what that tag contains: the skills, the agents, the bundled references and `catalog.json`.
5. Set the installation policy for the pilot group.
6. Keep access, data handling and any connected-app permissions under administrator control.

Pin the tag, not a branch. A tag names one fixed set of bytes that cannot change after it has been reviewed, so the group keeps running the version that was actually reviewed; a branch can differ from one session to the next. For a supervised pilot handling approved or redacted fund documents, pin a tag or a specific commit, and review a newer release before moving the group to it.

Outside a managed workspace, the Codex CLI installs the same plugin:

```bash
codex plugin marketplace add davendra/fundadmin-ai-skills
codex plugin add fundadmin@fundadmin-ai-skills
```

Codex names each skill directly: `$fund-review-lpa <file>` rather than a menu command.

## Other agents — Developer compatibility only

`npx skills` is a third-party installer that copies selected raw skill files into an agent-specific skills directory. It does not install this plugin: no plugin manifest, no agents, no marketplace metadata, no version metadata and no release assets. Skills copied that way run without the five review agents, so `review-lpa` falls back to inline prompts, and without the packaged report helper, so output is an unverified draft rather than a saved report with source hashes and an evidence sidecar.

It is for developers who want selected workflows inside another agent. **It is not a route for supervised fund-operation pilots.** Read the installer's own documentation and review what it will write before running anything:

```bash
npx skills add davendra/fundadmin-ai-skills --skill fund-review-lpa -a codex
```

Keep it project-local and name the agent and the skills explicitly. Do not install globally with `-g`/`--global`, do not use `--all` or the `--skill '*'` wildcard, and do not skip the prompts with `-y`/`--yes`: each installs more than you reviewed, where you did not choose. Project-local is the tool's default; keep it. Installing a third-party repository is never required to use FundAdmin AI — the routes above are the supported ones.

## Plain skills, no plugin system

There is no remote installer, and you should not pipe a script from the internet into a shell.

From a reviewed checkout of the source repository [`davendra/fundadmin-ai`](https://github.com/davendra/fundadmin-ai), read its diff, run its verification helpers, then run the local `install.sh` from that same checkout. It copies the skills into `~/.claude/skills/` and the agents into `~/.claude/agents/`, so commands become `/fund <command>` without the plugin prefix. Everything else in this manual applies unchanged; drop the `fundadmin:` prefix from the examples. The full recipe, including the virtual environment and the checks to run first, is in that repository's README. An existing installation is refused unless you authorise an update, and an authorised update is backed up first.

This is a maintainer route. For pilot users, use the plugin marketplace.

## Release channels and version pinning

Use one installation method per host environment. The plugin route and a plain-skills or raw-skills copy install skills of the same names, and two copies in one host leave it ambiguous which instructions ran.

Every public release is tagged `fundadmin--vX.Y.Z`; the tag is never moved or replaced, and a correction takes a new version number. Development branches and local checkouts are not user installation targets. A supervised pilot pins a reviewed tag or commit, and records the installation method, plugin version and tag, host version and model or runtime identifier alongside its review evidence.

The full policy is in [installation and release channels](https://github.com/davendra/fundadmin-ai-skills/blob/main/docs/production/installation-and-release-channels.md).

## Alongside Anthropic's financial-services plugins

Anthropic publishes a separate marketplace, [`anthropics/financial-services`](https://github.com/anthropics/financial-services), with general finance-operations plugins: ledger reconciliation, break tracing, accruals, roll-forwards, variance commentary, NAV tie-out, a KYC screener, financial models and market-data connectors. FundAdmin AI covers the private-fund documents those plugins do not: LPAs, side letters, PPMs, subscription documents, capital calls, distributions, capital accounts, K-1s, waterfalls, fees and MFN elections, with KYC routing built around fund investor types. The two install side by side and their skill names do not overlap. FundAdmin AI is independent and is not affiliated with or endorsed by Anthropic.

## Optional dependencies

- **PDF reports:** `pip3 install reportlab` lets `report-pdf` turn any review into a branded PDF. Without it the skill hands you the markdown and the command to run elsewhere.
- **Excel workbooks:** `pip3 install openpyxl` lets the KYC review, KYC tracker, capital account review, reconciliation, fee audit, waterfall review and obligation tracker save an `.xlsx` beside the markdown report. Without it you get a `.csv` of the same tables, and the skill says so.
- **Gmail:** `monitor-email` needs your host's Gmail connector and stops with a message if it is missing.
- **Obsidian vault:** `vault-init`, `vault-sync` and precedent search across a vault use the MCP vault server from the [source repository](https://github.com/davendra/fundadmin-ai). Every skill works without it and says when it skipped something.

## Update

| Host | Command |
|---|---|
| Claude Code | `claude plugin update fundadmin@fundadmin-ai-skills`, then restart the session |
| Codex CLI | `codex plugin marketplace upgrade`, then `codex plugin add fundadmin@fundadmin-ai-skills` |
| Claude Cowork | **Update** on the marketplace entry |
| Codex / ChatGPT workspace | The administrator reviews the newer release tag and selects it; the pilot group does not update itself |

Hosts cache by version, so a release only reaches you once the version number changes. The current version is in the footer of this site and in the [changelog](https://github.com/davendra/fundadmin-ai-skills/blob/main/CHANGELOG.md). A pinned installation does not move on its own — that is the point of pinning. Review an updated release before enabling it for a pilot group, and record that you did.

## Uninstall

```bash
claude plugin uninstall fundadmin@fundadmin-ai-skills
codex plugin remove fundadmin@fundadmin-ai-skills
```

In a managed workspace, the administrator removes the marketplace entry or the installation policy.

For the plain-skills install, run `uninstall.sh` from the same reviewed source checkout you installed from, or delete the `fund*` directories under `~/.claude/skills/` and `~/.claude/agents/`. For raw skills copied by a third-party installer, delete them from that agent's skills directory.
