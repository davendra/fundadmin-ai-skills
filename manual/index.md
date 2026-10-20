---
layout: home
title: FundAdmin AI Help
description: Install FundAdmin AI, try a sample review and find the right workflow for your fund administration team.
hero:
  name: FundAdmin AI
  text: Your guide to better fund reviews.
  tagline: Source-linked findings, draft workpapers and clear human-review steps. Learn to use the supervised AI copilot inside your approved AI host.
  image:
    src: /images/fundadmin-ai-mark.png
    alt: FundAdmin AI cyan and violet F logo
  actions:
    - theme: brand
      text: Get started
      link: /guide/quick-start
    - theme: alt
      text: Browse 60 commands
      link: /commands/
    - theme: alt
      text: Install the plugin
      link: /guide/install

features:
  - icon:
      light: /images/icons/review-light.svg
      dark: /images/icons/review-dark.svg
    title: Review fund documents
    details: Review LPAs, PPMs, subscriptions, side letters, notices and statements. Trace findings to the supplied documents and keep missing evidence visible.
    link: /commands/document-review
    linkText: Document reviews
  - icon:
      light: /images/icons/compliance-light.svg
      dark: /images/icons/compliance-dark.svg
    title: Understand an LPA
    details: Five specialist perspectives cover terms, risk, compliance, obligations and negotiation. Evidence coverage is separate from document favourability.
    link: /agents
    linkText: The review workflow
  - icon:
      light: /images/icons/draft-light.svg
      dark: /images/icons/draft-dark.svg
    title: Prepare a first draft
    details: Draft capital calls, distributions, investor letters and side letters from supplied facts. Check the figures and cited terms before issuing anything.
    link: /commands/document-generation
    linkText: Drafting workflows
  - icon:
      light: /images/icons/investors-light.svg
      dark: /images/icons/investors-dark.svg
    title: Organise investor checks
    details: Bring classification, tax forms, suitability and AML/KYC evidence into a structured review. Missing screening or firm rules remain open checks.
    link: /commands/investor-compliance-onboarding
    linkText: Investor workflows
  - icon:
      light: /images/icons/analysis-light.svg
      dark: /images/icons/analysis-dark.svg
    title: Calculate and reconcile
    details: Prepare performance metrics, cash-flow scenarios, waterfall workpapers, fee checks and document reconciliations using the packaged calculation helpers.
    link: /commands/analytics-modeling
    linkText: Calculations and models
  - icon:
      light: /images/icons/tracking-light.svg
      dark: /images/icons/tracking-dark.svg
    title: Keep obligations in view
    details: Build dated reports for side-letter obligations, MFN elections, credit covenants and filing calendars. Assign owners and follow up through your own controls.
    link: /commands/tracking-monitoring
    linkText: Tracking workflows
---

<div class="release-strip"><span>Plugin v1.3.3</span><span>60 commands + the fund menu</span><span>5 LPA-review agents</span><a href="/guide/release">Release and host support →</a></div>

## From document to review

<div class="workflow-steps">
  <div><span class="step-number">01</span><h3>Start with a sample</h3><p>Install the plugin and choose a synthetic document. Check the host, Python requirements and output permissions.</p><a href="/guide/quick-start">Run your first review →</a></div>
  <div><span class="step-number">02</span><h3>Follow the evidence</h3><p>Read the findings alongside their source references, calculations and unresolved checks. A missing input stays missing.</p><a href="/guide/outputs">Understand the report →</a></div>
  <div><span class="step-number">03</span><h3>Review before acting</h3><p>A qualified person checks the draft and decides what happens next. The plugin does not approve investments, investors or payments.</p><a href="/guide/examples">See worked examples →</a></div>
</div>

## Choose your starting point

| You want to… | Start here |
|---|---|
| Install in Claude Code, Cowork or Codex | [Installation and requirements](/guide/install) |
| See a sample input and its finished draft | [Worked examples](/guide/examples) |
| Review an LPA and understand the score | [The 5 review agents](/agents) |
| Review a folder of fund documents | [Batch intake](/commands/document-intake#ingest) |
| Review an investor's subscription evidence | [Subscription process](/commands/investor-compliance-onboarding#subscription-process) |
| Find a command or troubleshoot a run | [Command reference](/commands/) · [FAQ](/guide/faq) |

::: info Supervised use
Version 1.3.3 is a supervised release candidate. Claude Code has published synthetic test evidence; Codex and Cowork have different verification limits. Read [release and host support](/guide/release) and [privacy](/guide/privacy) before using approved fund documents. Python 3.9+ is required for saved reports and the standard helpers.
:::

FundAdmin AI provides document analysis and drafting support. Not financial, legal or tax advice. Qualified human review is required.
