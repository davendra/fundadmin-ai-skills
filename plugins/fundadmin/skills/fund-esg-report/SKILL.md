---
name: fund-esg-report
description: "ESG report across SFDR (Art. 6/8/9, PAI), TCFD, EDCI, UN PRI and EU Taxonomy, scoring data gaps. Use for `/fund esg-report` or an SFDR/PAI disclosure. Writes ESG-REPORT-[fund]-[date].md."
---

# ESG/Impact Reporting Generator

You are the ESG/Impact reporting engine for `/fund esg-report <data>`. You accept portfolio company ESG data, fund classification information, and applicable framework selections, then produce a comprehensive ESG report with framework-specific disclosures, Principal Adverse Impact (PAI) indicators, data completeness scores, and a data collection gap analysis.

## Trigger

This skill is activated by `/fund esg-report <data>` where `<data>` is portfolio company ESG data (file path, pasted text, or URL), optionally accompanied by fund classification (e.g., SFDR Article 8) and the frameworks to report against. If no framework is specified, default to all applicable frameworks based on fund jurisdiction and classification.

---

## Phase 1: Data Ingestion & Framework Selection

### 1.1 Read the ESG Data

Accept ESG data from one of these sources:
- **File path** -- Use the Read tool to read the file (CSV, spreadsheet, PDF, or text)
- **Pasted text** -- Accept ESG metrics or portfolio company descriptions pasted directly
- **URL** -- Use WebFetch to retrieve the document

Store the full data for analysis.

**If the input is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed without ESG data

### 1.2 Identify the Fund and Classification

Extract or ask the user for:

| Field | Description | Example |
|-------|-------------|---------|
| **Fund Name** | Legal name of the fund | Obrelund Growth Fund III |
| **Fund Type** | PE, VC, RE, Credit, Hedge, Infrastructure | Private Equity |
| **SFDR Classification** | Article 6, 8, or 9 | Article 8 |
| **Domicile** | Fund jurisdiction | Luxembourg |
| **AUM** | Assets under management | EUR 500M |
| **Reporting Period** | Period covered by report | FY 2025 |
| **Number of Portfolio Companies** | Active investments | 12 |

### 1.3 Select Applicable Frameworks

Determine which frameworks apply based on fund classification and user request:

| Framework | When Required | Key Trigger |
|-----------|--------------|-------------|
| **SFDR** | EU-domiciled funds or marketed into EU | Article 6/8/9 classification; mandatory PAI statement for >500 employees at entity level |
| **TCFD** | Large asset managers, UK-regulated, voluntary adopters | Climate risk disclosure expectations from LPs; UK FCA requirements |
| **EDCI** | PE funds participating in ESG Data Convergence Initiative | LP request or GP voluntary participation; 400+ GP participants globally |
| **UN PRI** | PRI signatories | Annual PRI reporting and assessment obligations |
| **EU Taxonomy** | Article 8/9 funds under SFDR | Taxonomy-eligible and taxonomy-aligned revenue disclosure |

---

## Phase 2: SFDR Analysis

### 2.1 Article Classification Assessment

Evaluate the fund against SFDR classification criteria:

| Classification | Criteria | Key Requirements |
|---------------|----------|-----------------|
| **Article 6** | No sustainability characteristics promoted | Disclose how sustainability risks are integrated into investment decisions; explain if sustainability risks are not considered relevant |
| **Article 8** | Promotes environmental or social characteristics | Pre-contractual disclosures (Annex II), periodic reporting (Annex IV), website disclosures (Annex III), binding ESG criteria in investment process |
| **Article 9** | Has sustainable investment as its objective | All Article 8 requirements plus: sustainable investment objective with measurable targets, DNSH assessment for all investments, EU Taxonomy alignment disclosure |

### 2.2 Mandatory PAI Indicators (18 Indicators)

For each of the 18 mandatory Principal Adverse Impact indicators, assess data availability and report values:

#### Climate and Environment (Indicators 1-6)

| # | PAI Indicator | Metric | Unit | Data Status | Value | Notes |
|---|--------------|--------|------|-------------|-------|-------|
| 1 | **GHG Emissions — Scope 1** | Scope 1 GHG emissions of investee companies | Tonnes CO2e | [Available/Partial/Missing] | [value] | Direct emissions from owned/controlled sources |
| 2 | **GHG Emissions — Scope 2** | Scope 2 GHG emissions of investee companies | Tonnes CO2e | [Available/Partial/Missing] | [value] | Indirect emissions from purchased energy |
| 3 | **GHG Emissions — Scope 3** | Scope 3 GHG emissions of investee companies | Tonnes CO2e | [Available/Partial/Missing] | [value] | All other indirect emissions in value chain |
| 4 | **Carbon Footprint** | Carbon footprint of the portfolio | Tonnes CO2e / EUR M invested | [Available/Partial/Missing] | [value] | Total GHG / current value of all investments |
| 5 | **GHG Intensity of Investee Companies** | GHG intensity per revenue | Tonnes CO2e / EUR M revenue | [Available/Partial/Missing] | [value] | Weighted average across portfolio |
| 6 | **Fossil Fuel Exposure** | Share of investments in fossil fuel sector | % | [Available/Partial/Missing] | [value] | NACE codes B.05, B.06, B.09.1, C.19, D.35.1 |

#### Energy (Indicators 7-8)

| # | PAI Indicator | Metric | Unit | Data Status | Value |
|---|--------------|--------|------|-------------|-------|
| 7 | **Non-Renewable Energy Share** | Share of non-renewable energy consumption and production | % | [Available/Partial/Missing] | [value] |
| 8 | **Energy Consumption Intensity** | Energy consumption intensity per high-impact climate sector | GWh / EUR M revenue | [Available/Partial/Missing] | [value] |

#### Biodiversity, Water, Waste (Indicators 9-11)

| # | PAI Indicator | Metric | Unit | Data Status | Value |
|---|--------------|--------|------|-------------|-------|
| 9 | **Biodiversity Impact** | Activities negatively affecting biodiversity-sensitive areas | Share of investments | [Available/Partial/Missing] | [value] |
| 10 | **Water Emissions** | Emissions to water | Tonnes per EUR M invested | [Available/Partial/Missing] | [value] |
| 11 | **Hazardous Waste** | Hazardous waste and radioactive waste ratio | Tonnes per EUR M invested | [Available/Partial/Missing] | [value] |

#### Social and Governance (Indicators 12-18)

| # | PAI Indicator | Metric | Unit | Data Status | Value |
|---|--------------|--------|------|-------------|-------|
| 12 | **UN Global Compact / OECD Violations** | Violations of UNGC principles and OECD Guidelines | Share of investments | [Available/Partial/Missing] | [value] |
| 13 | **UNGC / OECD Monitoring Processes** | Lack of processes to monitor compliance | Share of investments | [Available/Partial/Missing] | [value] |
| 14 | **Gender Pay Gap** | Unadjusted gender pay gap | % | [Available/Partial/Missing] | [value] |
| 15 | **Board Gender Diversity** | Female-to-male ratio on boards | % female | [Available/Partial/Missing] | [value] |
| 16 | **Controversial Weapons** | Exposure to controversial weapons (AP mines, cluster munitions, chemical, biological) | Share of investments | [Available/Partial/Missing] | [value] |
| 17 | **GHG Intensity of Sovereigns** | GHG intensity of investee countries | Tonnes CO2e / EUR M GDP | [Available/Partial/Missing] | [value] |
| 18 | **Investee Countries Subject to Social Violations** | Countries with social violations | Number of investee countries | [Available/Partial/Missing] | [value] |

### 2.3 Optional PAI Indicators

Flag which optional indicators the fund elects to report (at least one environmental and one social required):

| Category | Example Optional Indicators | Selected |
|----------|----------------------------|----------|
| **Environmental** | Water usage and recycling, investments in companies without carbon reduction initiatives, land degradation/desertification, untreated waste discharge, non-recycled waste ratio | [Yes/No] |
| **Social** | Insufficient whistleblower protection, human rights due diligence gaps, lack of anti-corruption/bribery policies, excessive CEO pay ratio, lack of human rights policy | [Yes/No] |

---

### Data Completeness Scoring

- For each framework (SFDR, TCFD, EDCI, UN PRI), calculate % of required fields populated
- Score: Complete (>90%), Partial (50-90%), Minimal (<50%)
- Prioritize gaps: mandatory SFDR PAI indicators first, then optional
- Generate a Data Collection Roadmap listing missing fields by priority

## Phase 3: TCFD Analysis

Assess the fund's climate-related disclosures across the 4 TCFD pillars:

### 3.1 Governance

| Disclosure | What to Assess | Data Status |
|-----------|---------------|-------------|
| Board oversight of climate risks | Does the GP/board have designated responsibility for climate risk oversight? | [Documented/Partial/Missing] |
| Management's role in assessing climate risks | Is there a climate/ESG committee or designated officer? What is the reporting cadence? | [Documented/Partial/Missing] |

### 3.2 Strategy

| Disclosure | What to Assess | Data Status |
|-----------|---------------|-------------|
| Climate risks and opportunities identified | Physical risks (acute: extreme weather; chronic: sea-level rise) and transition risks (policy, technology, market, reputation) | [Documented/Partial/Missing] |
| Impact on business, strategy, financial planning | How climate risks affect investment thesis, portfolio construction, exit strategy | [Documented/Partial/Missing] |
| Scenario analysis | Has the fund modeled 1.5C, 2C, and/or 4C warming scenarios? Impact on portfolio valuations? | [Documented/Partial/Missing] |

### 3.3 Risk Management

| Disclosure | What to Assess | Data Status |
|-----------|---------------|-------------|
| Process for identifying climate risks | Is climate risk part of the investment due diligence process? | [Documented/Partial/Missing] |
| Process for managing climate risks | Portfolio-level risk management, engagement strategies, divestment criteria | [Documented/Partial/Missing] |
| Integration with overall risk management | Is climate risk integrated into the fund's broader ERM framework? | [Documented/Partial/Missing] |

### 3.4 Metrics and Targets

| Disclosure | What to Assess | Data Status |
|-----------|---------------|-------------|
| Climate metrics used | Scope 1+2+3 emissions, carbon intensity, WACI, implied temperature rise | [Documented/Partial/Missing] |
| Scope 1, 2, 3 emissions | Portfolio-level GHG emissions (link to SFDR PAI 1-3) | [Documented/Partial/Missing] |
| Targets and progress | Net-zero commitment, interim targets, decarbonization pathway, SBTi alignment | [Documented/Partial/Missing] |

### 3.5 Physical and Transition Risk Assessment

For each portfolio company (if data available):

| Company | Sector | Physical Risk Exposure | Transition Risk Exposure | Overall Climate Risk |
|---------|--------|----------------------|------------------------|---------------------|
| [name] | [sector] | [Low/Medium/High] — [description] | [Low/Medium/High] — [description] | [Low/Medium/High] |

---

## Phase 4: EDCI Analysis

Assess the fund's standardized PE metrics per the ESG Data Convergence Initiative:

| # | EDCI Metric | Category | Unit | Data Status | Value | Benchmark |
|---|------------|----------|------|-------------|-------|-----------|
| 1 | **Total GHG Emissions (Scope 1+2)** | Environment | Tonnes CO2e | [Available/Partial/Missing] | [value] | Median PE: varies by sector |
| 2 | **Renewable Energy Percentage** | Environment | % of total energy | [Available/Partial/Missing] | [value] | Target: increasing year-over-year |
| 3 | **Board Diversity** | Social | % female directors | [Available/Partial/Missing] | [value] | EDCI median: ~25% |
| 4 | **Work-Related Injuries** | Social | Rate per 200K hours | [Available/Partial/Missing] | [value] | Sector-dependent |
| 5 | **Net New Hires** | Social | Number or % growth | [Available/Partial/Missing] | [value] | Positive = job creation |
| 6 | **Employee Engagement** | Social | Survey score or % | [Available/Partial/Missing] | [value] | >70% typically positive |

---

## Phase 5: UN PRI & EU Taxonomy Assessment

### 5.1 UN PRI Principles Alignment

| Principle | Description | Implementation Status |
|-----------|-------------|----------------------|
| **Principle 1** | Incorporate ESG issues into investment analysis and decision-making processes | [Implemented/Partial/Not Implemented] |
| **Principle 2** | Be active owners and incorporate ESG issues into ownership policies and practices | [Implemented/Partial/Not Implemented] |
| **Principle 3** | Seek appropriate disclosure on ESG issues by the entities in which we invest | [Implemented/Partial/Not Implemented] |
| **Principle 4** | Promote acceptance and implementation of the Principles within the investment industry | [Implemented/Partial/Not Implemented] |
| **Principle 5** | Work together to enhance effectiveness in implementing the Principles | [Implemented/Partial/Not Implemented] |
| **Principle 6** | Report on activities and progress towards implementing the Principles | [Implemented/Partial/Not Implemented] |

### 5.2 EU Taxonomy Assessment

For each portfolio company, assess:

| Company | Revenue (EUR M) | Taxonomy-Eligible Revenue (%) | Taxonomy-Aligned Revenue (%) | Environmental Objectives Contributed To | DNSH Compliance |
|---------|----------------|------------------------------|-----------------------------|-----------------------------------------|-----------------|
| [name] | [value] | [value]% | [value]% | [Climate Mitigation / Adaptation / Water / Circular Economy / Pollution / Biodiversity] | [Yes/Partial/No] |

**Fund-Level Aggregates:**

| Metric | Value |
|--------|-------|
| Weighted Average Taxonomy-Eligible Revenue | [X]% |
| Weighted Average Taxonomy-Aligned Revenue | [X]% |
| Companies with Taxonomy Data Available | [X] of [Y] |

---

## Phase 6: Data Gap Analysis

### 6.1 Data Collection Framework

For each framework, identify what data should be requested from portfolio companies:

| Data Point | SFDR | TCFD | EDCI | EU Tax | Collection Method | Typical Source |
|-----------|------|------|------|--------|-------------------|----------------|
| Scope 1 GHG Emissions | Mandatory (PAI 1) | Required | Required | Required | Annual questionnaire | Energy bills, fuel records |
| Scope 2 GHG Emissions | Mandatory (PAI 2) | Required | Required | Required | Annual questionnaire | Electricity bills |
| Scope 3 GHG Emissions | Mandatory (PAI 3) | Recommended | Optional | Optional | Estimation models | Spend-based or activity-based |
| Revenue by Activity | Optional | Recommended | N/A | Required | Financial statements | Audited accounts |
| Energy Consumption | Mandatory (PAI 7-8) | Required | Required | Required | Utility data | Energy management system |
| Water Usage | Optional | Optional | N/A | Conditional | Utility data | Water meters |
| Waste Data | Mandatory (PAI 11) | Optional | N/A | Conditional | Waste manifests | Waste contractor reports |
| Employee Count | Indirect | Indirect | Required | Indirect | HR systems | Payroll records |
| Gender Pay Data | Mandatory (PAI 14) | N/A | N/A | N/A | HR systems | Compensation analysis |
| Board Composition | Mandatory (PAI 15) | N/A | Required | N/A | Corporate records | Board resolutions |
| Health & Safety | Optional | N/A | Required | N/A | HR/EHS systems | OSHA logs or equivalent |

### 6.2 Gap Analysis Summary

| Framework | Total Required Data Points | Data Available | Data Partially Available | Data Missing | Completeness Score |
|-----------|--------------------------|----------------|------------------------|--------------|-------------------|
| SFDR (Mandatory PAI) | 18 | [X] | [X] | [X] | [X]% |
| TCFD (4 Pillars) | 11 | [X] | [X] | [X] | [X]% |
| EDCI (Core Metrics) | 6 | [X] | [X] | [X] | [X]% |
| EU Taxonomy | [X] | [X] | [X] | [X] | [X]% |
| **Overall** | **[X]** | **[X]** | **[X]** | **[X]** | **[X]%** |

---

## Phase 7: Generate Output File

Generate `ESG-REPORT-[fund]-[date].md` with the following structure:

```markdown
# ESG/Impact Report

> DISCLAIMER: This ESG report is generated by an AI assistant and does not constitute
> investment, legal, regulatory, or sustainability advice. ESG frameworks (SFDR, TCFD,
> EDCI, UN PRI, EU Taxonomy) have specific regulatory requirements that may change over
> time. Data completeness and accuracy depend entirely on the portfolio company data
> provided. This report is intended as a starting point for ESG disclosure — it must be
> reviewed by qualified ESG professionals, legal counsel, and compliance officers before
> use in regulatory filings, LP reports, or marketing materials. AI-generated ESG
> disclosures are not a substitute for professional ESG consulting or audit services.

---

## Report Summary

| Field | Value |
|-------|-------|
| Fund Name | [name] |
| Fund Type | [type] |
| SFDR Classification | Article [6/8/9] |
| Domicile | [jurisdiction] |
| AUM | [value] |
| Reporting Period | [period] |
| Portfolio Companies | [count] |
| Frameworks Covered | [list] |
| Overall Data Completeness | [X]% |
| Date of Report | [date] |

---

## Data Completeness Dashboard

| Framework | Score | Status |
|-----------|-------|--------|
| SFDR Mandatory PAI | [X]% | [Sufficient/Gaps Identified/Insufficient] |
| TCFD Pillars | [X]% | [Sufficient/Gaps Identified/Insufficient] |
| EDCI Core Metrics | [X]% | [Sufficient/Gaps Identified/Insufficient] |
| EU Taxonomy | [X]% | [Sufficient/Gaps Identified/Insufficient] |
| UN PRI Alignment | [X]/6 principles | [Strong/Moderate/Weak] |

---

## 1. SFDR Disclosure

### SFDR Classification Assessment
[Paragraph explaining Article 6/8/9 classification rationale and whether the fund
meets the requirements for its current or target classification]

### Mandatory PAI Statement

#### Climate and Environment Indicators

| # | Indicator | Metric | Value | Coverage | YoY Change |
|---|-----------|--------|-------|----------|------------|
| 1 | GHG Scope 1 | Tonnes CO2e | [value] | [X]% of portfolio | [+/-X%] |
| 2 | GHG Scope 2 | Tonnes CO2e | [value] | [X]% of portfolio | [+/-X%] |
| 3 | GHG Scope 3 | Tonnes CO2e | [value] | [X]% of portfolio | [+/-X%] |
| 4 | Carbon Footprint | tCO2e/EUR M | [value] | [X]% of portfolio | [+/-X%] |
| 5 | GHG Intensity | tCO2e/EUR M rev | [value] | [X]% of portfolio | [+/-X%] |
| 6 | Fossil Fuel Exposure | % | [value] | [X]% of portfolio | [+/-X%] |
| 7 | Non-Renewable Energy | % | [value] | [X]% of portfolio | [+/-X%] |
| 8 | Energy Intensity | GWh/EUR M rev | [value] | [X]% of portfolio | [+/-X%] |
| 9 | Biodiversity Impact | % investments | [value] | [X]% of portfolio | [+/-X%] |
| 10 | Water Emissions | t/EUR M invested | [value] | [X]% of portfolio | [+/-X%] |
| 11 | Hazardous Waste | t/EUR M invested | [value] | [X]% of portfolio | [+/-X%] |

#### Social and Governance Indicators

| # | Indicator | Metric | Value | Coverage | YoY Change |
|---|-----------|--------|-------|----------|------------|
| 12 | UNGC/OECD Violations | % investments | [value] | [X]% of portfolio | [+/-X%] |
| 13 | UNGC/OECD Monitoring Gaps | % investments | [value] | [X]% of portfolio | [+/-X%] |
| 14 | Gender Pay Gap | % | [value] | [X]% of portfolio | [+/-X%] |
| 15 | Board Gender Diversity | % female | [value] | [X]% of portfolio | [+/-X%] |
| 16 | Controversial Weapons | % investments | [value] | [X]% of portfolio | [+/-X%] |
| 17 | Sovereign GHG Intensity | tCO2e/EUR M GDP | [value] | N/A | [+/-X%] |
| 18 | Social Violations (Sovereigns) | Count | [value] | N/A | [+/-X%] |

### Selected Optional PAI Indicators
[List any optional indicators the fund reports on with values]

---

## 2. TCFD Disclosure

### Governance
[Narrative on board and management oversight of climate-related risks]

### Strategy
[Narrative on climate risks/opportunities and their impact on fund strategy]

### Risk Management
[Narrative on how climate risks are identified, assessed, and managed]

### Metrics and Targets
[Portfolio climate metrics, targets, and progress]

### Portfolio Climate Risk Summary

| Company | Sector | Physical Risk | Transition Risk | Overall |
|---------|--------|--------------|----------------|---------|
| [name] | [sector] | [L/M/H] | [L/M/H] | [L/M/H] |

---

## 3. EDCI Metrics

| Metric | Value | Coverage | EDCI Benchmark | Relative Performance |
|--------|-------|----------|---------------|---------------------|
| GHG Scope 1+2 | [value] tCO2e | [X]% | [benchmark] | [Above/At/Below] |
| Renewable Energy | [value]% | [X]% | [benchmark] | [Above/At/Below] |
| Board Diversity | [value]% female | [X]% | ~25% | [Above/At/Below] |
| Work-Related Injuries | [value] | [X]% | [benchmark] | [Above/At/Below] |
| Net New Hires | [value] | [X]% | Positive | [Above/At/Below] |
| Employee Engagement | [value]% | [X]% | >70% | [Above/At/Below] |

---

## 4. EU Taxonomy Assessment

### Portfolio Taxonomy Alignment

| Company | Eligible Revenue | Aligned Revenue | Objectives | DNSH |
|---------|-----------------|----------------|------------|------|
| [name] | [X]% | [X]% | [objectives] | [Y/N] |

### Fund-Level Aggregates
- **Taxonomy-Eligible Revenue:** [X]%
- **Taxonomy-Aligned Revenue:** [X]%
- **Data Coverage:** [X]% of portfolio by value

---

## 5. UN PRI Alignment

| Principle | Status | Evidence |
|-----------|--------|----------|
| 1. ESG in Investment Analysis | [status] | [evidence] |
| 2. Active Ownership | [status] | [evidence] |
| 3. Seek Disclosure | [status] | [evidence] |
| 4. Promote Principles | [status] | [evidence] |
| 5. Collaborative Implementation | [status] | [evidence] |
| 6. Reporting | [status] | [evidence] |

---

## 6. Data Gap Analysis

### Missing Data — Priority Collection Items

| Priority | Data Point | Framework(s) | Portfolio Companies Affected | Collection Method |
|----------|-----------|-------------|----------------------------|-------------------|
| CRITICAL | [data] | [frameworks] | [companies] | [method] |
| HIGH | [data] | [frameworks] | [companies] | [method] |
| MEDIUM | [data] | [frameworks] | [companies] | [method] |

### Recommended Data Collection Timeline

| Phase | Action | Timeline | Expected Completeness Improvement |
|-------|--------|----------|----------------------------------|
| Immediate | [action] | 0-30 days | +[X]% |
| Short-Term | [action] | 1-3 months | +[X]% |
| Medium-Term | [action] | 3-6 months | +[X]% |

---

## Recommended Next Steps

1. [ ] Review and validate all reported ESG data with portfolio company management
2. [ ] Address CRITICAL data gaps before regulatory filing deadlines
3. [ ] Engage third-party ESG data verification provider for material metrics
4. [ ] Update SFDR pre-contractual and periodic disclosures based on this report
5. [ ] Distribute portfolio company ESG questionnaire for missing data points
6. [ ] Schedule portfolio company ESG engagement meetings for gap remediation
7. [ ] Consult qualified ESG advisor and legal counsel before regulatory filings
```

---

## Phase 8: Present to User

After generating the report:

1. Display the **Overall Data Completeness Score** prominently
2. Display the **SFDR Classification Assessment** summary
3. List the **Top 3 Data Gaps** requiring immediate attention
4. Summarize the **PAI indicator coverage** (X of 18 mandatory indicators with data)
5. Show the full report
6. Ask: "Would you like me to check the fund's regulatory compliance? Run `/fund check-compliance <file>`."
7. Mention: "Run `/fund report-pdf` to generate a professional PDF version of this ESG report."

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| No ESG data provided | Ask user to provide portfolio company ESG data, metrics, or a description of available data |
| Fund classification unknown | Ask user for SFDR Article classification; default to Article 8 analysis if in EU, or TCFD/EDCI only if non-EU |
| No portfolio company data available | Generate a data collection template showing exactly what data to request from each portfolio company |
| Partial data across companies | Analyze what is available, clearly mark coverage percentages, and prioritize gap-filling recommendations |
| Non-EU fund | Skip SFDR/EU Taxonomy sections unless user specifically requests them; focus on TCFD and EDCI |
| Framework not applicable | Explain why the framework does not apply and which frameworks are more appropriate |
