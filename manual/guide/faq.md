# FAQ and troubleshooting

## "Unknown command" or the skills do not appear

Use the plugin prefix: `/fundadmin:fund`, not the bare form. Restart the session after installing. `claude plugin details fundadmin@fundadmin-ai-skills` should list 61 skills (60 commands plus the `fund` menu) and 5 agents.

## The PDF was not generated

`report-pdf` needs Python 3.9+, the packaged renderer and its dependencies. Use the [isolated dependency setup](/guide/install#optional-dependencies) before reviewing. Without a working renderer it retains any validated Markdown and sidecar and says that no PDF was produced. An in-chat draft is not a saved report.

In ChatGPT cloud, the plugin can load its instructions without making scripts available to Python. Follow [personal cloud helper staging](/guide/install#chatgpt-cloud-personal-upload) using the verified released ZIP; never ask the model to invent a substitute helper. Download the PDF and audit ZIP and check the final limitations and table continuations.

## ChatGPT says Work requires an upgrade

Plugin installation does not grant Work access. Use an account that already has Work enabled, or test the available Chat mode with its tools and limitations recorded. Do not buy an upgrade solely because a setup prompt asks. Chat and Work qualification are separate.

## Cloud data analysis stopped or reached a limit

Keep the failed attempt and do not call the report complete. Resume when your account has available code-tool capacity, or use an existing authorised host with those tools. Work access and analysis quota are account features, not supplied by the plugin. Download any real audit files while available; never invent a PDF link. See the [host-check results](/guide/host-checks).

## An LPA review is taking a long time

That is expected: five agents work through the whole agreement, in order. How long it takes depends on the host, the document and the tools available; no timing is guaranteed. A report with missing checks is marked `PARTIAL` or `BLOCKED`, and a score that could not be evidenced is reported as unavailable rather than filled in.

## The review flagged something that is fine

Every finding names the clause it came from. Read the clause. The skills describe documents and, where a skill says so, compare terms with this suite's illustrative reference ranges, which are not market data; they do not know your fund's negotiating history. Treat every output as a draft for a professional to review.

## Can I use it on real fund documents?

Only within an authorised, supervised pilot, with data controls your organisation has approved and professional review of every output. This release is not certified for production use. Everything under `samples/` is synthetic and marked as such. Documents go only where your AI host already sends them: the plugin has no hooks, no MCP servers and makes no network calls of its own. The [privacy page](/guide/privacy) has the details.

## How do I update?

Claude Code: `claude plugin update fundadmin@fundadmin-ai-skills`, then restart. Codex: `codex plugin marketplace upgrade`, then `codex plugin add fundadmin@fundadmin-ai-skills`. Cowork: **Update** on the marketplace entry. See [Install](/guide/install#update).

## Where do I report a problem?

Use the [contact form](https://fundadmin.dev/#contact) on fundadmin.dev, and pick "A question about the plugin". Say which command you ran, on which host, and what you expected to happen. Please don't send pull requests to the plugin repository: it is regenerated on every release, so changes made there are overwritten.

## Does it work with Anthropic's financial-services plugins?

Yes, alongside them. Anthropic publishes a separate marketplace, [`anthropics/financial-services`](https://github.com/anthropics/financial-services), with general finance-operations plugins: ledger reconciliation, break tracing, accruals, roll-forwards, variance commentary, NAV tie-out, a KYC screener, financial models and market-data connectors. FundAdmin AI covers the private-fund documents those plugins do not: LPAs, side letters, PPMs, subscription documents, capital calls, distributions, capital accounts, K-1s, waterfalls, fees and MFN elections, with KYC routing built around fund investor types. The two install side by side and their skill names do not overlap. FundAdmin AI is independent and is not affiliated with or endorsed by Anthropic.

## Is it advice?

No. FundAdmin AI produces document analysis and drafts to support fund administration work. Every report says: "Not financial, legal or tax advice. Qualified human review is required."
