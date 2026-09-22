# Install

The skills ship as one plugin, `fundadmin`, from the repository [`davendra/fundadmin-ai-skills`](https://github.com/davendra/fundadmin-ai-skills). Pick your host.

## Claude Code

```bash
claude plugin marketplace add davendra/fundadmin-ai-skills
claude plugin install fundadmin@fundadmin-ai-skills
```

Or inside a session: `/plugin marketplace add davendra/fundadmin-ai-skills`, then `/plugin install fundadmin@fundadmin-ai-skills`. Restart the session once to load it.

Check the install:

```bash
claude plugin details fundadmin@fundadmin-ai-skills
```

Expect 63 skills (the 62 commands plus the `fund` menu) and 5 agents.

## Claude Cowork

**Customize → Plugins → Add marketplace**, enter `davendra/fundadmin-ai-skills`, then install **FundAdmin AI**.

## Codex

```bash
codex plugin marketplace add davendra/fundadmin-ai-skills
codex plugin add fundadmin@fundadmin-ai-skills
```

Codex names each skill directly: `$fund-review-lpa <file>` rather than a menu command.

## Plain skills, no plugin system

```bash
curl -fsSL https://raw.githubusercontent.com/davendra/fundadmin-ai/main/install.sh | bash
```

Installs the same skills into `~/.claude/skills/` and the agents into `~/.claude/agents/` from the source repository. Commands are then `/fund <command>` without the plugin prefix. Everything else in this manual applies unchanged; drop the `fundadmin:` prefix from the examples.

## Optional dependencies

- **PDF reports:** `pip3 install reportlab` lets `report-pdf` turn any review into a branded PDF. Without it the skill hands you the markdown and the command to run elsewhere.
- **Gmail:** `monitor-email` needs your host's Gmail connector and stops with a message if it is missing.
- **Obsidian vault:** `vault-init`, `vault-sync` and precedent search across a vault use the MCP vault server from the [source repository](https://github.com/davendra/fundadmin-ai). Every skill works without it and says when it skipped something.

## Update

| Host | Command |
|---|---|
| Claude Code | `claude plugin update fundadmin@fundadmin-ai-skills`, then restart the session |
| Codex | `codex plugin marketplace upgrade`, then `codex plugin add fundadmin@fundadmin-ai-skills` |
| Claude Cowork | **Update** on the marketplace entry |

Both hosts cache by version, so a release only reaches you once the version number changes. The current version is in the footer of this site and in the [changelog](https://github.com/davendra/fundadmin-ai-skills/blob/main/CHANGELOG.md).

## Uninstall

```bash
claude plugin uninstall fundadmin@fundadmin-ai-skills
codex plugin remove fundadmin@fundadmin-ai-skills
```

For the plain-skills install, run `uninstall.sh` from the source repository or delete the `fund*` directories under `~/.claude/skills/` and `~/.claude/agents/`.
