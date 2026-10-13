# Install

The skills ship as one plugin, `fundadmin`, from the public repository [`davendra/fundadmin-ai-skills`](https://github.com/davendra/fundadmin-ai-skills). Choose **Claude Code**, **ChatGPT desktop**, or **ChatGPT in the cloud** below. All use the skills-only package; the separate FundAdmin AI Workspace application is [in development](https://fundadmin.dev/workspace).

Claude Code is the recommended, tested installation route. ChatGPT desktop, ChatGPT Work, Codex and Cowork accept the package format; FundAdmin workflow execution on these hosts remains experimental until separately qualified. Account access and administrator policies determine which plugin surfaces you can use. A public GitHub release is not an OpenAI public-directory listing. See the [dated host-check results](/guide/host-checks) for what was actually exercised and what remains blocked.

## Claude Code — Recommended {#claude-code-recommended}

Recommended for individual supervised-pilot use.

```bash
claude plugin marketplace add https://github.com/davendra/fundadmin-ai-skills.git#fundadmin--v1.3.2 --scope project
claude plugin install fundadmin@fundadmin-ai-skills --scope project
```

Use one installation per project. Restart the session once to load it.

Check the install:

```bash
claude plugin details fundadmin@fundadmin-ai-skills
```

Expect 61 skills (the 60 commands plus the `fund` menu) and 5 agents, at the version shown in the footer of this site.

**Claude Cowork** installs the same plugin from the same marketplace through its interface: **Customize → Plugins → Add marketplace**, enter `davendra/fundadmin-ai-skills`, then install **FundAdmin AI**.

## ChatGPT desktop — Local marketplace {#chatgpt-desktop-local-marketplace}

For a local **Work or Codex task in the ChatGPT desktop app**, use the repository marketplace included in the download. You do not need Claude Code for this route.

1. [Download the skills ZIP for v1.3.2](https://github.com/davendra/fundadmin-ai-skills/releases/download/fundadmin--v1.3.2/fundadmin-ai-skills-1.3.2.zip). Extract it into a new folder, preserving hidden files. Open the extracted folder as your local project in a supported ChatGPT desktop surface.
2. Confirm `.agents/plugins/marketplace.json` is present at the extracted root and its entry points to `./plugins/fundadmin`. Keep the entire package together.
3. Restart ChatGPT desktop. Open **Plugins**, select the **FundAdmin AI** local marketplace and install **fundadmin**.
4. Start a **new local Work or Codex task**. Use the host's skill picker to select the installed `fund-review-lpa` skill. Work uses `@`; Codex uses `$`. Choose the actual picker entry rather than guessing an alias.
5. Use `samples/OBRELUND-LPA-QUICKSTART.pdf` for the first review. Check that the task can access the packaged files and run the Python report helper before claiming a saved report was generated.

**Shared local catalogue route, tested with a desktop local Codex task:** if the supported Codex CLI is already available, it can install the plugin in the catalogue used by local desktop tasks:

```bash
codex plugin marketplace add davendra/fundadmin-ai-skills --ref fundadmin--v1.3.2
codex plugin add fundadmin@fundadmin-ai-skills
codex plugin list --marketplace fundadmin-ai-skills --json
```

Check for an existing copy before changing it; expect v1.3.2, installed and enabled. Start a new local desktop task using the installed `fund-review-lpa` skill and the synthetic sample, then follow the dependency and PDF checks below. This install-plus-task route was exercised on 13 October 2026; the separate GUI installation sequence above was documented from the platform guidance and was not automated. Do not count a CLI-only review as a desktop task test.

If your account has no local project or Plugins surface, use the managed-workspace route below if your administrator enables it. Do not paste terminal installation commands into an ordinary chat and assume that installed the plugin. The local catalogue does not upload itself to the cloud.

This follows [OpenAI's local marketplace guidance](https://developers.openai.com/plugins/build/plugins#build-your-own-curated-plugin-list). Local project, personal catalogue and managed-workspace installations are different sources; use one route for an environment and avoid duplicate installations.

## ChatGPT cloud — Personal plugin upload {#chatgpt-cloud-personal-upload}

If your account shows **Plugins → Add → Upload plugin archive**, you can install a personal cloud copy without an administrator-managed marketplace. This route was observed in Chat mode on 13 October 2026; account availability varies. It does not unlock Work or change your subscription.

1. [Download the standalone ChatGPT plugin ZIP for v1.3.2](https://github.com/davendra/fundadmin-ai-skills/releases/download/fundadmin--v1.3.2/fundadmin-ai-chatgpt-1.3.2.zip) and [its SHA-256 file](https://github.com/davendra/fundadmin-ai-skills/releases/download/fundadmin--v1.3.2/fundadmin-ai-chatgpt-1.3.2.zip.sha256). This archive contains only the released plugin, with its hidden manifests at the archive root. The larger skills ZIP is for local marketplaces and includes samples and documentation.
2. Open **Plugins → Add → Upload plugin archive**. Upload the standalone ZIP, then choose **Add plugin**. Confirm **FundAdmin AI**, version **1.3.2** and **61 skills**, then choose **Install plugin**.
3. Start a new chat with the installed plugin selected. Separately download and attach the [eight-page synthetic LPA](https://raw.githubusercontent.com/davendra/fundadmin-ai-skills/fundadmin--v1.3.2/samples/OBRELUND-LPA-QUICKSTART.pdf).
4. Check that Python can access the packaged helper scripts and the five agent files. Importing instructions alone does not guarantee these files are mounted in the chat's execution environment.
5. If the helpers are missing, attach the same standalone ZIP to that chat. Ask the assistant to verify its SHA-256 against the release checksum, reject absolute paths, parent traversal and symlink members, and extract the entire plugin into a new isolated software folder. Run only helpers from that verified copy; do not substitute code found beside an uploaded document. Record **verified release-bundle staging** as the setup method.
6. Follow the [full LPA and PDF quick start](/guide/quick-start#full-lpa-and-pdf-check). Download the report and audit bundle while the task's files remain available.

Uploading the plugin ZIP is separate from attaching it to a review chat. Neither action grants connected-app access. Chat, Work, desktop and CLI runs have different execution environments: a successful Chat test does not qualify Work. If Python, helper files or file downloads are unavailable, keep the result labelled as an in-chat draft and list the missing deliverables.

## ChatGPT Work — Cloud / managed workspace {#chatgpt-work-cloud-managed-workspace}

In a workspace, an administrator imports the marketplace once and sets the policy for the pilot group. Members do not each add a source.

1. The administrator opens **Admin → Plugins → Add → Import marketplace**.
2. Set **Source** to `https://github.com/davendra/fundadmin-ai-skills`.
3. Leave **Path** empty (the marketplace is at the repository root). Set **Branch, tag or commit** to `fundadmin--v1.3.2`, rather than a moving branch.
4. Review what that tag contains: the skills, the agents, the bundled references and `catalog.json`.
5. Set the installation policy for the pilot group.
6. Keep access, data handling and any connected-app permissions under administrator control.

Once permitted for their role, members open **Plugins**, select their workspace's FundAdmin AI plugin and install it. Start a **new Work task** in ChatGPT on the web or desktop. Type `@` and choose an installed FundAdmin skill from the picker, then attach a synthetic sample from the release. No local Claude Code installation is required for a cloud task.

Importing a marketplace does not grant connected-service permissions. Check which code tools, Python dependencies, specialist-agent execution and packaged helper files are available in the cloud task. If a helper cannot run, keep the result clearly labelled as a draft and state which PDF, source hashes or evidence sidecar were not generated. Package import alone does not qualify a host for a supervised pilot.

The steps follow [OpenAI's workspace import guidance](https://learn.chatgpt.com/docs/enterprise/plugin-management) and [plugin installation and use guidance](https://learn.chatgpt.com/docs/plugins). Availability depends on your account and workspace settings.

Pin the tag, not a branch. A tag names one fixed set of bytes that cannot change after it has been reviewed, so the group keeps running the version that was actually reviewed; a branch can differ from one session to the next. For a supervised pilot handling approved or redacted fund documents, pin a tag or a specific commit, and review a newer release before moving the group to it.

## Codex CLI — Experimental

Outside a managed workspace, the Codex CLI can install the same plugin. The pinned install and a synthetic LPA/PDF run were exercised through the local CLI on 13 October 2026. This is supplementary runtime evidence; the desktop interface and cloud Work journey still require their own tests.

```bash
codex plugin marketplace add davendra/fundadmin-ai-skills --ref fundadmin--v1.3.2
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

## Release channels and version pinning

Use one installation method per host environment. The plugin route and a raw-skills copy install skills of the same names, and two copies in one host leave it ambiguous which instructions ran.

Every public release is tagged `fundadmin--vX.Y.Z`; the tag is never moved or replaced, and a correction takes a new version number. Development branches and local checkouts are not user installation targets. A supervised pilot pins a reviewed tag or commit, and records the installation method, plugin version and tag, host version and model or runtime identifier alongside its review evidence.

The full policy is in [installation and release channels](https://github.com/davendra/fundadmin-ai-skills/blob/main/docs/production/installation-and-release-channels.md).

## Alongside Anthropic's financial-services plugins

Anthropic publishes a separate marketplace, [`anthropics/financial-services`](https://github.com/anthropics/financial-services), with general finance-operations plugins: ledger reconciliation, break tracing, accruals, roll-forwards, variance commentary, NAV tie-out, a KYC screener, financial models and market-data connectors. FundAdmin AI covers the private-fund documents those plugins do not: LPAs, side letters, PPMs, subscription documents, capital calls, distributions, capital accounts, K-1s, waterfalls, fees and MFN elections, with KYC routing built around fund investor types. The two install side by side and their skill names do not overlap. FundAdmin AI is independent and is not affiliated with or endorsed by Anthropic.

## Optional dependencies

- **PDF reports:** check dependencies before the first review. From the extracted full release, create an isolated environment rather than changing system Python:

  ```bash
  python3 -m venv .venv-fundadmin
  .venv-fundadmin/bin/python -m pip install -r requirements-plugin.txt
  .venv-fundadmin/bin/python -c "import reportlab, pypdf; print(reportlab.Version)"
  ```

  Tell the assistant to use that environment's Python for the packaged helpers. The pinned release uses ReportLab 5.0.1. In cloud tasks, check the actual environment: if the pinned dependencies cannot be installed, record the available versions and treat PDF compatibility as unqualified until extraction and layout checks pass. Without a working renderer, retain the Markdown and sidecar and say that no PDF was produced.
- **Excel workbooks:** `pip3 install openpyxl` lets the KYC review, KYC tracker, capital account review, reconciliation, fee audit, waterfall review and obligation tracker save an `.xlsx` beside the markdown report. Without it you get a `.csv` of the same tables, and the skill says so.
- **Email:** `monitor-email` needs an approved email connector in your host (for example Gmail) and reports the check as not performed if it is missing.

## Update

| Host | Command |
|---|---|
| Claude Code | `claude plugin update fundadmin@fundadmin-ai-skills`, then restart the session |
| Codex CLI | `codex plugin marketplace upgrade`, then `codex plugin add fundadmin@fundadmin-ai-skills` |
| Claude Cowork | **Update** on the marketplace entry |
| ChatGPT desktop local marketplace | Download a reviewed newer release into a separate folder, then refresh the local installation; avoid two active copies |
| ChatGPT personal cloud upload | Upload a reviewed newer standalone plugin archive; remove ambiguity from older active copies |
| ChatGPT Work / managed workspace | The administrator reviews the newer release tag and selects it; the pilot group does not update itself |

Hosts cache by version, so a release only reaches you once the version number changes. The current version is in the footer of this site and in the [changelog](https://github.com/davendra/fundadmin-ai-skills/blob/main/CHANGELOG.md). A pinned installation does not move on its own — that is the point of pinning. Review an updated release before enabling it for a pilot group, and record that you did.

## Uninstall

```bash
claude plugin uninstall fundadmin@fundadmin-ai-skills
codex plugin remove fundadmin@fundadmin-ai-skills
```

In a managed workspace, the administrator removes the marketplace entry or the installation policy.

For raw skills copied by a third-party installer, delete them from that agent's skills directory. (Maintainers who installed plain skills from the private source checkout use its `uninstall.sh`.)
