# Privacy

FundAdmin AI is a set of instructions your AI host follows. It has no server or account of its own, so there is nothing for it to collect.

## The plugin

- **No hooks, no MCP servers, no network calls of its own.** The plugin is 63 markdown skill files, five agent prompts, six templates and one Python script that renders PDF reports locally.
- **Your documents go where your host already sends them.** When a skill reads a file, your host passes its contents to the model it uses, under the host's own terms.
- **Links are fetched by your host.** If you give a skill a URL instead of a file, it asks your host to fetch that page with the host's own web tool. No skill searches the web by itself.
- **Reports stay on your machine.** Skills write markdown files under `reviews/` in your working directory, and `report-pdf` renders PDFs with ReportLab on your machine.
- **Optional integrations are yours to connect.** `monitor-email` reads Gmail only through your host's Gmail connector, and only when you run it. The Obsidian vault server, if you install it from the source repository, reads and writes files in your local vault and nowhere else.

## This site

- Static pages hosted on Vercel, which keeps standard request logs.
- Fonts are loaded from Google Fonts.
- No cookies, no analytics and no tracking scripts. The light or dark theme you pick is kept in your browser's local storage.

## Questions

Open an issue on the [plugin repository](https://github.com/davendra/fundadmin-ai-skills/issues).
