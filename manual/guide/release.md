# Release and host support

**Documentation reviewed: 20 October 2026.** This manual describes plugin **v1.3.3**: 60 commands, the `fund` menu and 5 LPA-review agents. A documentation update does not change the installed plugin version.

The published package is a **supervised release candidate**. Use approved inputs, review every output and keep operational decisions with authorised people.

## What has been verified?

| Host | Package and evidence |
|---|---|
| Claude Code | Each release from v1.3.0 is published only with recorded evidence for all 18 synthetic installed-plugin cases on Claude Code 2.1.278. This is evidence for that release and host configuration, not a guarantee for every document or later host version. |
| Codex | A pinned marketplace installation completed a supplementary synthetic LPA review using the inline fallback. This is not a complete host/model qualification matrix; the route remains experimental. |
| ChatGPT desktop and cloud | A desktop local task completed a synthetic installed-plugin review. An assisted cloud Chat run produced saved outputs, but substantive source-evidence corrections remain open. Cloud Work was not tested. See [host checks](/guide/host-checks) for the exact routes and limits. |
| Claude Cowork | A compatible plugin package is supplied. The Cowork runtime is unverified. |

The [verification record](https://github.com/davendra/fundadmin-ai-skills/blob/main/docs/production/verification.md) describes the tested candidate, retries, reviewer notes and limits. Local package checks do not establish live screening, legal accuracy or production readiness.

## What is included?

- 60 task commands plus the `fund` menu.
- 5 specialist LPA-review prompts, with an inline fallback where subagents are unavailable.
- Local helpers for reports, evidence, scoring, calculations, screening evidence, spreadsheet companions and PDFs.
- Reference materials, templates and 24 synthetic sample documents.

Python 3.9+ is required for the core helpers. PDF and Excel output have additional dependencies; see [installation requirements](/guide/install#requirements).

## Keep your installation traceable

Record the plugin version, reviewed tag or commit, host version and resolved model identifier. Use one installation method per environment and review a newer release before updating a user group. A Git tag can be moved by a repository administrator; retain the resolved commit as well as the tag. This project's release policy prohibits replacing published tags.

- [Published v1.3.3 tag](https://github.com/davendra/fundadmin-ai-skills/tree/fundadmin--v1.3.3)
- [Changelog](https://github.com/davendra/fundadmin-ai-skills/blob/main/CHANGELOG.md)
- [Installation and updates](/guide/install)
- [Privacy and data handling](/guide/privacy)

## Need help?

Use the [FundAdmin AI contact form](https://fundadmin.dev/#contact). Include the command, plugin version, host version and a redacted description of the issue. Do not include confidential fund documents, bank details or identity records in an initial support message.
