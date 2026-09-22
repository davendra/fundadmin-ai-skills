# FAQ and troubleshooting

## "Unknown command" or the skills do not appear

Use the plugin prefix: `/fundadmin:fund`, not the bare form (that is for the plain-skills install). Restart the session after installing. `claude plugin details fundadmin@fundadmin-ai-skills` should list 63 skills and 5 agents.

## The PDF was not generated

`report-pdf` needs Python 3 and `reportlab` (`pip3 install reportlab`). Without them it hands you the markdown report and the exact command to run elsewhere.

## An LPA review is taking a long time

That is expected: five agents read the whole agreement, and a full review usually takes 15 to 40 minutes. Shorter documents are faster. The report is written once, at the end, with the final score; if you see a draft with placeholder scores, the run was interrupted.

## The review flagged something that is fine

Every finding names the clause it came from. Read the clause. The skills describe documents and compare them with common market terms; they do not know your fund's negotiating history. Treat every output as a draft for a professional to review.

## Can I use it on real fund documents?

Yes; that is what it is for. Everything under `samples/` is synthetic and marked as such. Documents go only where your AI host already sends them: the plugin has no hooks, no MCP servers and makes no network calls of its own. The [privacy page](/guide/privacy) has the details.

## How do I update?

Claude Code: `claude plugin update fundadmin@fundadmin-ai-skills`, then restart. Codex: `codex plugin marketplace upgrade`, then `codex plugin add fundadmin@fundadmin-ai-skills`. Cowork: **Update** on the marketplace entry. See [Install](/guide/install#update).

## Where do I report a problem?

Open an issue on the [source repository](https://github.com/davendra/fundadmin-ai/issues). The plugin repository is generated from it on every release, so changes made there are overwritten.

## Is it advice?

No. FundAdmin AI produces document analysis and drafts to support fund administration work. It is not financial, legal or tax advice, and every report says so.
