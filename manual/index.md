---
layout: home
title: FundAdmin AI Manual
hero:
  name: FundAdmin AI
  text: The fundadmin plugin manual
  tagline: 62 fund administration skills and 5 LPA-review agents for Claude Code, Claude Cowork and Codex. No server, no database, no API key.
  image:
    src: /images/hero.jpg
    alt: FundAdmin AI
  actions:
    - theme: brand
      text: Install
      link: /guide/install
    - theme: alt
      text: All 62 commands
      link: /commands/
    - theme: alt
      text: Quick start
      link: /guide/quick-start

features:
  - title: 62 commands in 14 categories
    details: Review LPAs, PPMs, side letters, capital calls, distributions, K-1s and statements. Draft notices and letters. Run compliance, KYC/AML and FATCA/CRS checks. Model performance and cash flows.
    link: /commands/
    linkText: Browse the commands
  - title: 5-agent LPA review
    details: Terms, risks, compliance and obligations agents run in parallel, then recommendations. Weighted into an LPA Safety Score from 0 to 100 with a letter grade.
    link: /agents
    linkText: How the agents work
  - title: Fixed output files
    details: Every skill writes a named markdown file under reviews/[fund]/[date]/, so later skills, PDF export and counsel handoff can find earlier results.
    link: /guide/outputs
    linkText: Output files
  - title: Try it on the samples
    details: 24 synthetic documents for one fictional fund ship with the plugin, most with planted issues and two clean controls.
    link: /guide/samples
    linkText: Sample documents
  - title: Runs inside your AI host
    details: The plugin has no hooks, no MCP servers and makes no network calls. Documents go only where your host already sends them.
    link: /guide/faq
    linkText: FAQ
  - title: Open source, MIT
    details: The skills, agents, templates and PDF script are MIT licensed. Generated from the source repository and republished on every release.
    link: https://github.com/davendra/fundadmin-ai-skills
    linkText: GitHub
---

## How it works

<p style="text-align: center; margin: 24px 0;">
  <img src="/images/how-it-works.jpg" alt="How FundAdmin AI works: drop in a fund document, a skill reviews it, get a scored report" style="max-width: 820px; width: 100%; border-radius: 8px;" />
</p>

A fund document goes in. The `/fundadmin:fund` menu, or the host's own skill matching, hands it to one of 62 skills. The skill follows a written workflow, launching specialist agents where it needs them, and writes a markdown report next to your documents. `report-pdf` can turn any report into a PDF.

::: warning Not advice
FundAdmin AI produces document analysis and drafts to support fund administration work. It is not financial, legal or tax advice. Every report says so. Have qualified professionals review anything you rely on.
:::
