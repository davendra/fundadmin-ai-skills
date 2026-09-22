# Privacy

FundAdmin AI is a set of instructions your AI host follows. It has no server or account of its own, so there is nothing for it to collect.

## The plugin

- **No hooks, no MCP servers, no network calls of its own.** The plugin is 63 markdown skill files, five agent prompts, six templates and five Python scripts: four standard-library helpers that create runs, check evidence and do the arithmetic, and one that renders PDF reports locally.
- **Your documents go where your host already sends them.** When a skill reads a file, your host passes its contents to the model it uses, under the host's own terms.
- **Links are fetched by your host.** If you give a skill a URL instead of a file, it asks your host to fetch that page with the host's own web tool. No skill searches the web by itself.
- **Reports stay on your machine.** Skills write markdown files under `reviews/<fund>/<date>/<run-id>/…` beneath the approved output root, and `report-pdf` renders PDFs with ReportLab on your machine. Nothing is written beside inputs or into the working-directory root.
- **Optional integrations are yours to connect.** `monitor-email` reads Gmail only through your host's Gmail connector, and only when you run it. The Obsidian vault server, if you install it from the source repository, reads and writes files in your local vault and nowhere else.

## This manual

- Static pages at help.fundadmin.dev, hosted on Vercel, which keeps standard request logs.
- Fonts are loaded from Google Fonts.
- No cookies, no analytics and no tracking scripts. The light or dark theme you pick is kept in your browser's local storage.

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
