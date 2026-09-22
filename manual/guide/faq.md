# FAQ and troubleshooting

## "Unknown command" or the skills do not appear

Use the plugin prefix: `/fundadmin:fund`, not the bare form (that is for the plain-skills install). Restart the session after installing. `claude plugin details fundadmin@fundadmin-ai-skills` should list 63 skills and 5 agents.

## The PDF was not generated

`report-pdf` needs Python 3.9+ and the pinned PDF dependencies (`python3 -m pip install -r requirements-plugin.txt` from the plugin repository). Without them it keeps the validated markdown report and says that the PDF was not produced.

## An LPA review is taking a long time

That is expected: five agents work through the whole agreement, in order. How long it takes depends on the host, the document and the tools available; no timing is guaranteed. A report with missing checks is marked `PARTIAL` or `BLOCKED`, and a score that could not be evidenced is reported as unavailable rather than filled in.

## The review flagged something that is fine

Every finding names the clause it came from. Read the clause. The skills describe documents and compare them with common market terms; they do not know your fund's negotiating history. Treat every output as a draft for a professional to review.

## Can I use it on real fund documents?

Only within an authorised, supervised pilot, with data controls your organisation has approved and professional review of every output. This release is not certified for production use. Everything under `samples/` is synthetic and marked as such. Documents go only where your AI host already sends them: the plugin has no hooks, no MCP servers and makes no network calls of its own. The [privacy page](/guide/privacy) has the details.

## How do I update?

Claude Code: `claude plugin update fundadmin@fundadmin-ai-skills`, then restart. Codex: `codex plugin marketplace upgrade`, then `codex plugin add fundadmin@fundadmin-ai-skills`. Cowork: **Update** on the marketplace entry. See [Install](/guide/install#update).

## Where do I report a problem?

Use the [contact form](https://fundadmin.dev/#contact) on fundadmin.dev, and pick "A question about the plugin". Say which command you ran, on which host, and what you expected to happen. Please don't send pull requests to the plugin repository: it is regenerated on every release, so changes made there are overwritten.

## Does it work with Anthropic's financial-services plugins?

Yes, alongside them. Anthropic publishes a separate marketplace, [`anthropics/financial-services`](https://github.com/anthropics/financial-services), with general finance-operations plugins: ledger reconciliation, break tracing, accruals, roll-forwards, variance commentary, NAV tie-out, a KYC screener, financial models and market-data connectors. FundAdmin AI covers the private-fund documents those plugins do not: LPAs, side letters, PPMs, subscription documents, capital calls, distributions, capital accounts, K-1s, waterfalls, fees and MFN elections, with KYC routing built around fund investor types. The two install side by side and their skill names do not overlap. FundAdmin AI is independent and is not affiliated with or endorsed by Anthropic.

## Is it advice?

No. FundAdmin AI produces document analysis and drafts to support fund administration work. It is not financial, legal or tax advice, and every report says so.
