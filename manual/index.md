---
layout: home
title: FundAdmin AI Manual
hero:
  name: FundAdmin AI
  text: The fundadmin plugin manual
  tagline: 60 fund administration skills, a menu, and 5 LPA-review agents for Claude Code, Claude Cowork and Codex. No server, no database, no API key.
  image:
    light: /images/ring-light.svg
    dark: /images/ring-dark.svg
    alt: The FundAdmin AI mark, a ring split in the LPA review weights
  actions:
    - theme: brand
      text: Install
      link: /guide/install
    - theme: alt
      text: All 60 commands
      link: /commands/
    - theme: alt
      text: Quick start
      link: /guide/quick-start

features:
  - icon:
      light: /images/icons/review-light.svg
      dark: /images/icons/review-dark.svg
    title: Review any fund document
    details: LPAs, PPMs, subscription agreements, side letters, capital calls, distribution notices, capital account statements, K-1s, GP updates. Each review lands as a source-linked markdown draft for professional review.
    link: /commands/document-review
    linkText: Document review
  - icon:
      light: /images/icons/compliance-light.svg
      dark: /images/icons/compliance-dark.svg
    title: Five specialist perspectives on an LPA
    details: Terms first, then risk, compliance and obligations, then recommendations. A heuristic favourability score from 0 to 100, or unavailable when an input is not evidenced. No letter grade.
    link: /agents
    linkText: How the agents work
  - icon:
      light: /images/icons/draft-light.svg
      dark: /images/icons/draft-dark.svg
    title: Draft notices and letters
    details: ILPA-style capital call and distribution notices, investor letters, side letters and LPA amendments, with the arithmetic run through the calculation helper and LPA references cited from the supplied documents or marked for verification.
    link: /commands/document-generation
    linkText: Document generation
  - icon:
      light: /images/icons/investors-light.svg
      dark: /images/icons/investors-dark.svg
    title: Onboard and screen investors
    details: Classification, FATCA/CRS, suitability, AML/KYC and subscription review in one seven-step process that assembles the evidence and the open checks for a person to decide.
    link: /commands/investor-compliance-onboarding
    linkText: Investor compliance
  - icon:
      light: /images/icons/analysis-light.svg
      dark: /images/icons/analysis-dark.svg
    title: Model and reconcile
    details: IRR, TVPI, DPI and PME from cash flows, waterfall tiers as code, cash-flow forecasts, fee audits, and line-by-line reconciliation of paired documents.
    link: /commands/analytics-modeling
    linkText: Analytics and modeling
  - icon:
      light: /images/icons/tracking-light.svg
      dark: /images/icons/tracking-dark.svg
    title: Track what the documents commit you to
    details: MFN elections, side letter obligations, credit covenants and the regulatory filing calendar, each written as a new dated tracking report; runs never overwrite earlier reports.
    link: /commands/tracking-monitoring
    linkText: Tracking and monitoring
---

## How it works

<img class="figure" src="/images/how-it-works.jpg" alt="How FundAdmin AI works: drop in a fund document, a skill reviews it, get a report" />

A fund document goes in. The `/fundadmin:fund` menu, or the host's own skill matching, hands it to one of 60 skills. The skill follows a written workflow, launching specialist agents where it needs them, and writes a markdown report under the [shared run tree](/guide/outputs) (`reviews/<fund>/<date>/<run-id>/…`). `report-pdf` can turn any report into a PDF, and every skill writes to a fixed filename family so later skills can build on earlier output.

## The LPA review

The flagship command. The terms agent inventories the agreement first; risk, compliance and obligations then work from the source and that inventory; a fifth agent turns their findings into ranked negotiation points and is not scored. The four scored dimensions give a heuristic favourability score, or none when one of them is not evidenced. The report opens with a ranked Key Issues and Asks list, and compliance is assessed only when you supply the regulatory facts (adviser status, offering route, investor mix, marketing jurisdictions). [How the agents and the score work](/agents).

## Two more workflows

<div class="figures">
  <figure>
    <img class="figure" src="/images/ingest-flow.jpg" alt="Batch intake: classify a folder of GP PDFs, review by priority, reconcile matching pairs, portfolio dashboard, ingest report" />
    <figcaption><a href="/commands/document-intake#ingest">Batch intake</a> takes a folder of mixed PDFs from GP portals, reviews them in priority order and drafts reconciliations of matching pairs; ambiguous matches stay open.</figcaption>
  </figure>
</div>

[Investor onboarding](/commands/investor-compliance-onboarding#subscription-process) runs seven checks in order and assembles the documents, the evidence and the checks still open. Missing verification gives a `PARTIAL` or `BLOCKED` draft, not an admission decision; a name hit is not a confirmed match. Authorised people make admission and clearance decisions.

::: warning Not advice
FundAdmin AI produces document analysis and drafts to support fund administration work. Not financial, legal or tax advice. Qualified human review is required. Every report says so.
:::
