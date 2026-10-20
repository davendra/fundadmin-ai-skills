# Privacy

The FundAdmin AI plugin runs through your chosen AI host. The plugin does not operate its own document-processing service. Your host, model providers, authorised connectors and locally saved reports still have data-handling implications.

## The plugin

- **No hooks, no MCP servers, no network calls of its own.** The plugin includes 60 task commands plus the `fund` menu, 5 agent prompts, templates and 8 Python scripts for runs, evidence, scoring, screening evidence records, calculations, spreadsheets, PDF rendering and text fidelity checks (`fund_pdf_fidelity.py`). Excel output needs `openpyxl`; PDF rendering needs `reportlab`, and PDF text fidelity checks need `pypdf`.
- **Your documents go where your host already sends them.** When a skill reads a file, your host passes its contents to the model it uses, under the host's own terms.
- **Links are fetched by your host.** If you give a skill a URL instead of a file, it asks your host to fetch that page with the host's own web tool. Some workflows request current official sources through host tools. Those requests are subject to the host's permissions and provider terms.
- **Reports are written in the host's approved workspace.** Their content has already passed through your host and its model, since that is how the analysis was produced. Skills write markdown files under `reviews/<fund>/<date>/<run-id>/…` beneath the approved output root, and `report-pdf` renders PDFs with ReportLab where the helper runs. A cloud or remote host may store that workspace remotely. Nothing is written beside inputs or into the working-directory root.
- **Optional integrations are yours to connect.** `monitor-email` reads mail only through an email connector you approve in your host (for example Gmail), and only when you run it. While mailbox content is in the conversation it does not use outbound connectors.
- **Every report says how its content was handled.** The report should identify which helpers and connectors actually ran and disclose missing operations. This is an instruction to the host, not a technical guarantee against disclosure.

## Your fund documents' confidentiality terms

LPAs, side letters and subscription documents usually restrict who fund information may be shared with. Before you give a confidential fund document to any AI tool, check whether your host's model provider is a permitted recipient under those terms, and what your host agreement says about retention and model training. That is a question for your legal or compliance team; FundAdmin AI cannot answer it for you, and some GPs now ask LPs not to use AI tools on their documents at all.

## This manual

- Static pages at help.fundadmin.dev, hosted on Vercel, which keeps standard request logs.
- This manual uses system fonts; it does not request fonts from Google Fonts.
- The manual includes no analytics or tracking scripts and does not set application cookies. The light or dark theme you pick is kept in your browser's local storage.

## fundadmin.dev

- Static pages hosted on Vercel, which keeps standard request logs. Fonts are bundled with the site.
- No cookies, no analytics, no tracking scripts, and nothing kept in your browser's storage.

## The contact form on fundadmin.dev

- It asks for your name, work email, company (optional), a topic and your message.
- Sending it emails what you wrote to our inbox through Resend, our email provider, with your address as the reply-to. The website itself does not store it.
- We use it only to reply to you. There is no mailing list, and the form does not sign you up to anything.
- To have a message deleted, ask in a reply to our email or through the form.

## Questions

Use the [contact form](https://fundadmin.dev/#contact) on fundadmin.dev.
