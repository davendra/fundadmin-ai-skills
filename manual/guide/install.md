# Install

The skills ship as one plugin, `fundadmin`, from the public repository [`davendra/fundadmin-ai-skills`](https://github.com/davendra/fundadmin-ai-skills). Choose **Claude Code**, **ChatGPT desktop**, or **ChatGPT in the cloud** below. All use the skills-only package; the separate FundAdmin AI Workspace application is [in development](https://fundadmin.dev/workspace).

Claude Code is the recommended, tested installation route. ChatGPT desktop, ChatGPT Work, Codex and Cowork accept the package format; FundAdmin workflow execution on these hosts remains experimental until separately qualified. Account access and administrator policies determine which plugin surfaces you can use. A public GitHub release is not an OpenAI public-directory listing. See the [dated host-check results](/guide/host-checks) for what was actually exercised and what remains blocked.

## Requirements

- An approved Claude Code, Cowork or Codex environment, with permission to install plugins and read the documents you supply. Host subscriptions, model usage and optional service charges are separate from this MIT-licensed plugin.
- **Python 3.9+** for the standard report, evidence, scoring and calculation helpers. A host without the helper or write access can provide only an UNVERIFIED chat draft.
- An approved output folder for saved reports. PDF generation and Excel output need the additional packages listed below.
- Authorised current evidence or connectors for external checks. Installation alone does not provide live AML screening, mailbox access or payment verification.

See [release and host support](/guide/release) for what has been tested on each host.

## Claude Code — Recommended {#claude-code-recommended}

Recommended for individual supervised use.

```bash
claude plugin marketplace add https://github.com/davendra/fundadmin-ai-skills.git#fundadmin--v1.3.3 --scope project
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

1. [Download the skills ZIP for v1.3.3](https://github.com/davendra/fundadmin-ai-skills/releases/download/fundadmin--v1.3.3/fundadmin-ai-skills-1.3.3.zip). Extract it into a new folder, preserving hidden files. Open the extracted folder as your local project in a supported ChatGPT desktop surface.
2. Confirm `.agents/plugins/marketplace.json` is present at the extracted root and its entry points to `./plugins/fundadmin`. Keep the entire package together.
3. Restart ChatGPT desktop. Open **Plugins**, select the **FundAdmin AI** local marketplace and install **fundadmin**.
4. Start a **new local Work or Codex task**. Use the host's skill picker to select the installed `fund-review-lpa` skill. Work uses `@`; Codex uses `$`. Choose the actual picker entry rather than guessing an alias.
5. Use `samples/OBRELUND-LPA-QUICKSTART.pdf` for the first review. Check that the task can access the packaged files and run the Python report helper before claiming a saved report was generated.

**Shared local catalogue route, tested with a desktop local Codex task:** if the supported Codex CLI is already available, it can install the plugin in the catalogue used by local desktop tasks:

```bash
codex plugin marketplace add davendra/fundadmin-ai-skills --ref fundadmin--v1.3.3
codex plugin add fundadmin@fundadmin-ai-skills
codex plugin list --marketplace fundadmin-ai-skills --json
```

Check for an existing copy before changing it; expect v1.3.3, installed and enabled. Start a new local desktop task using the installed `fund-review-lpa` skill and the synthetic sample, then follow the dependency and PDF checks below. This install-plus-task route was exercised on 13 October 2026; the separate GUI installation sequence above was documented from the platform guidance and was not automated. Do not count a CLI-only review as a desktop task test.

If your account has no local project or Plugins surface, use the managed-workspace route below if your administrator enables it. Do not paste terminal installation commands into an ordinary chat and assume that installed the plugin. The local catalogue does not upload itself to the cloud.

This follows [OpenAI's local marketplace guidance](https://developers.openai.com/plugins/build/plugins#build-your-own-curated-plugin-list). Local project, personal catalogue and managed-workspace installations are different sources; use one route for an environment and avoid duplicate installations.

## ChatGPT cloud — Personal plugin upload {#chatgpt-cloud-personal-upload}

If your account shows **Plugins → Add → Upload plugin archive**, you can install a personal cloud copy without an administrator-managed marketplace. This route was observed in Chat mode on 13 October 2026; account availability varies. It does not unlock Work or change your subscription.

1. [Download the standalone ChatGPT plugin ZIP for v1.3.3](https://github.com/davendra/fundadmin-ai-skills/releases/download/fundadmin--v1.3.3/fundadmin-ai-chatgpt-1.3.3.zip) and [its SHA-256 file](https://github.com/davendra/fundadmin-ai-skills/releases/download/fundadmin--v1.3.3/fundadmin-ai-chatgpt-1.3.3.zip.sha256). This archive contains only the released plugin, with its hidden manifests at the archive root. The larger skills ZIP is for local marketplaces and includes samples and documentation.
2. Open **Plugins → Add → Upload plugin archive**. Upload the standalone ZIP, then choose **Add plugin**. Confirm **FundAdmin AI**, version **1.3.3** and **61 skills**, then choose **Install plugin**.
3. Start a new chat with the installed plugin selected. Separately download and attach the [eight-page synthetic LPA](https://raw.githubusercontent.com/davendra/fundadmin-ai-skills/fundadmin--v1.3.3/samples/OBRELUND-LPA-QUICKSTART.pdf).
4. Check that Python can access the packaged helper scripts and the five agent files. Importing instructions alone does not guarantee these files are mounted in the chat's execution environment.
5. If the helpers are missing, attach the same standalone ZIP to that chat. Ask the assistant to verify its SHA-256 against the release checksum, reject absolute paths, parent traversal and symlink members, and extract the entire plugin into a new isolated software folder. Run only helpers from that verified copy; do not substitute code found beside an uploaded document. Record **verified release-bundle staging** as the setup method.
6. Follow the [full LPA and PDF quick start](/guide/quick-start#full-lpa-and-pdf-check). Download the report and audit bundle while the task's files remain available.

Uploading the plugin ZIP is separate from attaching it to a review chat. Neither action grants connected-app access. Chat, Work, desktop and CLI runs have different execution environments: a successful Chat test does not qualify Work. If Python, helper files or file downloads are unavailable, keep the result labelled as an in-chat draft and list the missing deliverables.

## ChatGPT Work — Cloud / managed workspace {#chatgpt-work-cloud-managed-workspace}

In a workspace, an administrator imports the marketplace once and sets the policy for the user group. Members do not each add a source.

1. Open the [OpenAI Admin Console](https://admin.openai.com), select your workspace, then **Plugins → Add → Import marketplace**.
2. Set **Source** to `https://github.com/davendra/fundadmin-ai-skills`; leave **Path** empty.
3. Enter `fundadmin--v1.3.3` in **Branch, tag, or commit**, or use its reviewed commit for a fixed revision.
4. Import the marketplace, authorise GitHub access if prompted and inspect the import results.
5. Review FundAdmin AI's contents and set its installation policy for eligible roles.
6. Keep data handling and connected-app access under administrator control.

New marketplaces have daily sync enabled. A fixed commit stays at that revision; a branch can bring in future changes. See [OpenAI's import and sync guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).

Once permitted for their role, members open **Plugins**, select their workspace's FundAdmin AI plugin and install it. Start a **new Work task** in ChatGPT on the web or desktop. Type `@` and choose an installed FundAdmin skill from the picker, then attach a synthetic sample from the release. No local Claude Code installation is required for a cloud task.

Importing a marketplace does not grant connected-service permissions. Check which code tools, Python dependencies, specialist-agent execution and packaged helper files are available in the cloud task. If a helper cannot run, keep the result clearly labelled as a draft and state which PDF, source hashes or evidence sidecar were not generated. Package import alone does not qualify a host for a supervised deployment.

The steps follow [OpenAI's workspace import guidance](https://learn.chatgpt.com/docs/enterprise/plugin-management) and [plugin installation and use guidance](https://learn.chatgpt.com/docs/plugins). Availability depends on your account and workspace settings.

Pin the tag, not a branch. This project does not replace published release tags. Git tags can technically be moved by an administrator, so record the resolved commit as well; branches can change between sessions. For a supervised deployment handling approved or redacted fund documents, pin a tag or a specific commit, and review a newer release before moving the group to it.

## Codex CLI — Experimental

Outside a managed workspace, the Codex CLI can install the same plugin. The pinned install and a synthetic LPA/PDF run were exercised through the local CLI on 13 October 2026. This is supplementary runtime evidence; the desktop interface and cloud Work journey still require their own tests.

```bash
codex plugin marketplace add davendra/fundadmin-ai-skills --ref fundadmin--v1.3.3
codex plugin add fundadmin@fundadmin-ai-skills
```

Codex names each skill directly: `$fund-review-lpa <file>` rather than a menu command.

## Other agents — Developer compatibility only {#other-agents-developer-compatibility-only}

`npx skills` is a third-party installer that copies selected raw skill files into an agent-specific skills directory. It does not install this plugin: no plugin manifest, no agents, no marketplace metadata, no version metadata and no release assets. Skills copied that way run without the five review agents, so `review-lpa` falls back to inline prompts, and without the packaged report helper, so output is an unverified draft rather than a saved report with source hashes and an evidence sidecar.

It is for developers who want selected workflows inside another agent. **It is not a route for supervised fund operations.** Read the installer's own documentation and review what it will write before running anything:

```bash
npx skills add davendra/fundadmin-ai-skills --skill fund-review-lpa -a codex
```

Keep it project-local and name the agent and the skills explicitly. Do not install globally with `-g`/`--global`, do not use `--all` or the `--skill '*'` wildcard, and do not skip the prompts with `-y`/`--yes`: each installs more than you reviewed, where you did not choose. Project-local is the tool's default; keep it. Installing a third-party repository is never required to use FundAdmin AI — the routes above are the supported ones.

## Release channels and version pinning

Use one installation method per host environment. The plugin route and a raw-skills copy install skills of the same names, and two copies in one host leave it ambiguous which instructions ran.

Every public release is tagged `fundadmin--vX.Y.Z`; the tag is never moved or replaced, and a correction takes a new version number. Development branches and local checkouts are not user installation targets. A supervised deployment pins a reviewed tag or commit, and records the installation method, plugin version and tag, host version and model or runtime identifier alongside its review evidence.

The full policy is in [installation and release channels](https://github.com/davendra/fundadmin-ai-skills/blob/main/docs/production/installation-and-release-channels.md).

## Alongside Anthropic's financial-services plugins

Anthropic maintains its own [financial-services marketplace](https://github.com/anthropics/financial-services). FundAdmin AI is an independent plugin focused on private-fund document review and drafting. Review each package's current commands, permissions and dependencies before using them together; installing either does not install or qualify the other. FundAdmin AI is not affiliated with or endorsed by Anthropic.

## Optional dependencies

- **PDF reports:** check dependencies before the first review. Create an isolated environment in your project rather than changing system Python, and install the release's pinned packages (the plugin also ships them as `skills/fund/requirements.txt`):

  ```bash
  python3 -m venv .venv
  .venv/bin/python -m pip install -r https://raw.githubusercontent.com/davendra/fundadmin-ai-skills/fundadmin--v1.3.3/requirements-plugin.txt
  source .venv/bin/activate && claude
  ```

  Starting Claude Code from the activated environment makes the skills' `python3` calls use it. Ask the assistant to run `fund_report.py check-env` before the first review: it names the Python in use, any missing package and the install command, and points to a project `.venv` it is not using. The pinned release uses ReportLab 5.0.1. In cloud tasks, check the actual environment: if the pinned dependencies cannot be installed, record the available versions and treat PDF compatibility as unqualified until extraction and layout checks pass. Without a working renderer, retain the Markdown and sidecar and say that no PDF was produced.
- **Excel workbooks:** openpyxl, in the same pinned list, lets the KYC review, KYC tracker, capital account review, reconciliation, fee audit, waterfall review and obligation tracker save an `.xlsx` beside the markdown report. Without it you get a `.csv` of the same tables, and the skill says so.
- **Email:** `monitor-email` needs an approved email connector in your host (for example Gmail) and reports the check as not performed if it is missing.

## Update

| Host | Command |
|---|---|
| Claude Code | `claude plugin marketplace update fundadmin-ai-skills`, then `claude plugin update fundadmin@fundadmin-ai-skills`, then restart the session |
| Codex CLI | `codex plugin marketplace upgrade`, then `codex plugin add fundadmin@fundadmin-ai-skills` |
| Claude Cowork | **Update** on the marketplace entry |
| ChatGPT desktop local marketplace | Download a reviewed newer release into a separate folder, then refresh the local installation; avoid two active copies |
| ChatGPT personal cloud upload | Upload a reviewed newer standalone plugin archive; remove ambiguity from older active copies |
| ChatGPT Work / managed workspace | The administrator reviews the newer revision and marketplace settings, then uses **Marketplaces → Sync now**; a fixed commit remains fixed. The user group does not update itself |

Hosts cache by version, so a release only reaches you once the version number changes. The current version is in the footer of this site and in the [changelog](https://github.com/davendra/fundadmin-ai-skills/blob/main/CHANGELOG.md). A pinned installation does not move on its own — that is the point of pinning. Review an updated release before enabling it for a user group, and record that you did.

## Uninstall

```bash
claude plugin uninstall fundadmin@fundadmin-ai-skills
codex plugin remove fundadmin@fundadmin-ai-skills
```

In a managed workspace, the administrator removes the marketplace entry or the installation policy.

For raw skills copied by a third-party installer, delete them from that agent's skills directory. (Maintainers who installed plain skills from the private source checkout use its `uninstall.sh`.)

## Host documentation

Host interfaces and availability can change. Consult [Claude Code plugin installation](https://code.claude.com/docs/en/discover-plugins) and [OpenAI plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-codex) for current host controls. Package support is separate from this plugin's [runtime verification](/guide/release).
