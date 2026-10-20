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

That is expected: the terms review comes first, risk/compliance/obligations follow and may run in parallel, and recommendations come last. Hosts without subagents run the prompts inline. How long it takes depends on the host, the document and the tools available; no timing is guaranteed. A report with missing checks is marked `PARTIAL` or `BLOCKED`, and a score that could not be evidenced is reported as unavailable rather than filled in.

## The review flagged something that is fine

Every finding names the clause it came from. Read the clause. The skills describe documents and, where a skill says so, compare terms with this suite's illustrative reference ranges, which are not market data; they do not know your fund's negotiating history. Treat every output as a draft for a professional to review.

## Can I use it on real fund documents?

Only within authorised, supervised use, with data controls your organisation has approved and professional review of every output. This release is not certified for production use. Everything under `samples/` is synthetic and marked as such. The packaged helpers make no network calls, but the host can send content to model providers and authorised tools or connectors can introduce other destinations. The [privacy page](/guide/privacy) has the details.

## How do I update?

Claude Code: refresh the marketplace with `claude plugin marketplace update fundadmin-ai-skills`, then run `claude plugin update fundadmin@fundadmin-ai-skills` and restart. Codex: `codex plugin marketplace upgrade`, then `codex plugin add fundadmin@fundadmin-ai-skills`. Cowork: **Update** on the marketplace entry. See [Install](/guide/install#update).

## Where do I report a problem?

Use the [contact form](https://fundadmin.dev/#contact) on fundadmin.dev, and pick "A question about FundAdmin Skills". Say which command you ran, on which host, and what you expected to happen. Please don't send pull requests to the plugin repository: it is regenerated on every release, so changes made there are overwritten.

## Does it work with Anthropic's financial-services plugins?

They are separate packages. FundAdmin AI focuses on private-fund document review and drafting; see [installation alongside other finance plugins](/guide/install#alongside-anthropic-s-financial-services-plugins). Review each package's current commands and permissions. Compatibility of a specific combined workflow still needs checking in your host.

## Is it advice?

No. FundAdmin AI produces document analysis and drafts to support fund administration work. Every report says: "Not financial, legal or tax advice. Qualified human review is required."

## Is the logo a score?

No. The cyan and violet F is the FundAdmin AI brand mark, matching fundadmin.dev. The [scoring chart](/agents#the-weights) uses four dimensions; recommendations are excluded. Never infer a score or a pass from the logo.

## Where can I see a complete example?

The [worked examples](/guide/examples) pair synthetic inputs with saved review reports, including a KYC tracker workbook.
