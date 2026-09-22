---
layout: home
title: FundAdmin AI Manual
hero:
  name: FundAdmin AI
  text: The fundadmin plugin manual
  tagline: 62 fund administration skills and 5 LPA-review agents for Claude Code, Claude Cowork and Codex. No server, no database, no API key.
  image:
    light: /images/ring-light.svg
    dark: /images/ring-dark.svg
    alt: The FundAdmin AI mark, a ring split in the LPA Safety Score weights
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
  - icon:
      light: /images/icons/review-light.svg
      dark: /images/icons/review-dark.svg
    title: Review any fund document
    details: LPAs, PPMs, subscription agreements, side letters, capital calls, distribution notices, capital account statements, K-1s, GP updates. Each review lands as a scored markdown report.
    link: /commands/document-review
    linkText: Document review
  - icon:
      light: /images/icons/compliance-light.svg
      dark: /images/icons/compliance-dark.svg
    title: Five agents score an LPA
    details: Terms, risks, compliance and obligations run in parallel, then recommendations. Weighted into an LPA Safety Score from 0 to 100 with a letter grade.
    link: /agents
    linkText: How the agents work
  - icon:
      light: /images/icons/draft-light.svg
      dark: /images/icons/draft-dark.svg
    title: Draft notices and letters
    details: ILPA-style capital call and distribution notices, investor letters, side letters and LPA amendments, with the arithmetic and LPA references worked in.
    link: /commands/document-generation
    linkText: Document generation
  - icon:
      light: /images/icons/investors-light.svg
      dark: /images/icons/investors-dark.svg
    title: Onboard and screen investors
    details: Classification, FATCA/CRS, suitability, AML/KYC and subscription review in one seven-step process that returns one of five recommendations.
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
    details: MFN elections, side letter obligations, credit covenants and the regulatory filing calendar, each as a register that later reviews update.
    link: /commands/tracking-monitoring
    linkText: Tracking and monitoring
---

## How it works

<img class="figure" src="/images/how-it-works.jpg" alt="How FundAdmin AI works: drop in a fund document, a skill reviews it, get a scored report" />

A fund document goes in. The `/fundadmin:fund` menu, or the host's own skill matching, hands it to one of 62 skills. The skill follows a written workflow, launching specialist agents where it needs them, and writes a markdown report next to your documents. `report-pdf` can turn any report into a PDF, and every skill writes to a [fixed filename](/guide/outputs) so later skills can build on earlier output.

## The LPA review

<img class="figure" src="/images/lpa-pipeline.jpg" alt="LPA review pipeline: four agents in parallel, then recommendations, then the LPA Safety Score and the LPA-REVIEW report" />

The flagship command. Four agents read the agreement in parallel, a fifth turns their findings into ranked negotiation points, and the five results are weighted into the LPA Safety Score. [How the agents and the score work](/agents).

## Two more workflows

<div class="figures">
  <figure>
    <img class="figure" src="/images/ingest-flow.jpg" alt="Batch intake: classify a folder of GP PDFs, review by priority, auto-reconcile, portfolio dashboard, ingest report" />
    <figcaption><a href="/commands/document-intake#ingest">Batch intake</a> takes a folder of mixed PDFs from GP portals, reviews them in priority order and reconciles matching pairs.</figcaption>
  </figure>
  <figure>
    <img class="figure" src="/images/onboarding-flow.jpg" alt="Investor onboarding: seven steps from classification to an acceptance recommendation with five possible outcomes" />
    <figcaption><a href="/commands/investor-compliance-onboarding#subscription-process">Investor onboarding</a> runs seven checks in order; the most restrictive result decides, so one hard fail cannot be averaged away.</figcaption>
  </figure>
</div>

::: warning Not advice
FundAdmin AI produces document analysis and drafts to support fund administration work. It is not financial, legal or tax advice. Every report says so. Have qualified professionals review anything you rely on.
:::
