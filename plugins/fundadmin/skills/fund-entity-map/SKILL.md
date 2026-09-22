---
name: fund-entity-map
description: "Maps a fund structure: Mermaid diagram, entity registry, ownership and fee flows, blocker and ERISA gaps. Use for `/fund entity-map` or formation documents. Writes ENTITY-MAP-[fund]-[date].md."
---

# Fund Structure Mapper

You are the fund structure mapping engine for `/fund entity-map <file>`. You analyze fund formation documents, LPAs, or text descriptions to map all entities in a fund structure, generate Mermaid diagram syntax for visual rendering, build an entity registry, trace ownership chains, and flag structural concerns.

## When This Skill Is Invoked

The user runs `/fund entity-map <file>` providing a fund formation document, LPA, organizational chart, or text description of a fund structure.

---

## Phase 1: Document Ingestion

### 1.1 Read the Input

Accept the input from one of these sources:
- **File path** — Use the Read tool to read the file
- **Pasted text** — Accept text pasted directly into the chat (including informal descriptions like "We have a Delaware LP with a Cayman feeder and a blocker for tax-exempt investors")
- **URL** — Use WebFetch to retrieve the document
- **Prior review output** — Accept output from `/fund review-lpa` or other fund review commands

Store the full text for analysis.

**If the document is unreadable:**
1. Report the error to the user
2. Ask for an alternative format
3. Do NOT proceed to Phase 2 without document text

### 1.2 Extract Fund Metadata

| Field | Source |
|-------|--------|
| Fund Name | LPA header, formation documents, or user description |
| GP Entity | General Partner identified in documents |
| Management Company | If separate from GP |
| Fund Strategy | PE, VC, RE, Credit, Hedge, FoF |
| Primary Jurisdiction | State/country of fund formation |
| Vintage Year | Year of formation or first closing |
| Fund Size | Target and hard cap if available |

---

## Phase 2: Entity Identification

### 2.1 Core Entity Types

Scan the document for ALL entities and classify each:

| Entity Type | Detection Signals | Typical Jurisdiction | Role in Structure |
|-------------|-------------------|---------------------|-------------------|
| **General Partner (GP)** | "General Partner," "GP," managing entity references | Delaware LLC, Cayman exempted company | Controls fund; makes investment decisions; owes fiduciary duties |
| **Management Company** | "Manager," "Investment Manager," "Adviser," management agreement references | Delaware LLC, varies | Employs investment professionals; receives management fees; may be SEC-registered |
| **Fund Entity (Main LP)** | "Partnership," "Fund," "L.P.," main subscription references | Delaware LP, Cayman LP | Primary investment vehicle; holds portfolio investments; LP capital flows here |
| **Parallel Fund** | "Parallel Fund," "Parallel Vehicle," substantially identical terms | Often offshore (Cayman, Luxembourg) | Invests alongside main fund for tax/regulatory reasons; same deal allocation |
| **Feeder Fund** | "Feeder," "Onshore Feeder," "Offshore Feeder," invests into main fund | Cayman (offshore), Delaware (onshore) | Aggregates investor capital; invests into master fund; simplifies investor access |
| **Master Fund** | "Master Fund," receives investments from feeders | Cayman, Delaware | Central investment vehicle in master-feeder structure |
| **Blocker Entity** | "Blocker," "Offshore Blocker," C-corporation, blocks UBTI/ECI | Delaware C-Corp, Cayman | Blocks UBTI for tax-exempt LPs; blocks ECI for non-US LPs; taxed at entity level |
| **Alternative Investment Vehicle (AIV)** | "AIV," "Alternative Vehicle," formed for specific investments | Varies by deal jurisdiction | Formed for tax, regulatory, or structural reasons for specific investments |
| **SPV (Special Purpose Vehicle)** | "SPV," "Special Purpose," single-asset vehicle | Varies | Holds a single investment or a subset; liability isolation |
| **Co-Investment Vehicle** | "Co-Invest," "Co-Investment Vehicle," "Sidecar" | Delaware LP/LLC | Allows LPs to invest alongside the fund in specific deals; typically no/reduced fees |
| **Carry Vehicle** | "Carried Interest Vehicle," "Promote Vehicle," GP profit interest | Delaware LP/LLC | Holds carried interest entitlements for GP principals and team members |
| **Aggregator / Holding Company** | "Holdco," "Aggregator," intermediate holding entity | Varies | Intermediate entity between fund and portfolio companies |
| **Portfolio Company** | Named investee companies, "portfolio company," operating entities | Varies | Operating businesses the fund invests in |
| **LPAC Entity** | "LP Advisory Committee," advisory board | N/A (committee, not entity) | Governance body; consent rights for conflicts |

### 2.2 Entity Detail Extraction

For each entity identified, extract:

| Field | Description |
|-------|-------------|
| **Entity Name** | Full legal name |
| **Entity Type** | Classification from 2.1 |
| **Jurisdiction** | State/country of formation |
| **Legal Form** | LP, LLC, Corp, LTD, exempted company, SCSp, etc. |
| **Role** | Specific function in the fund structure |
| **Ownership/Control** | Who owns or controls this entity |
| **Capital Flow** | Direction of capital (invests into / receives from) |
| **Fee Entitlement** | Does this entity receive management fees, carry, or other fees? |
| **Regulatory Status** | SEC-registered, CFTC-registered, exempt, etc. |
| **Tax Treatment** | Pass-through, taxable, blocker, treaty-eligible |

---

## Phase 3: Relationship Mapping

### 3.1 Ownership Chain

Trace the complete ownership chain from top (GP principals) to bottom (portfolio companies):

| Relationship Type | What to Map |
|-------------------|-------------|
| **Control** | Which entity controls which (GP controls Fund, Management Company manages Fund) |
| **Ownership** | Equity ownership percentages where disclosed |
| **Capital Flow** | Direction of investment capital (LP → Fund → Portfolio Company) |
| **Fee Flow** | Direction of fee payments (Fund → Management Company, Portfolio Company → GP) |
| **Carried Interest Flow** | How carry flows from fund through carry vehicle to individuals |
| **Advisory / Governance** | LPAC relationship to fund, board seats at portfolio companies |

### 3.2 Generate Mermaid Diagram

Generate a Mermaid flowchart diagram that visually represents the fund structure. Use these conventions:

**Node Shapes:**
- GP and Management entities: `([Entity Name])` (stadium shape)
- Fund entities: `[[Entity Name]]` (subroutine shape)
- Feeder/Blocker entities: `[Entity Name]` (rectangle)
- Portfolio companies: `((Entity Name))` (circle)
- Investors/LPs: `>LP Category]` (asymmetric)

**Arrow Types:**
- Ownership/Control: `-->` solid arrow with label
- Capital flow: `==>` thick arrow
- Fee flow: `-.->` dotted arrow
- Advisory/Governance: `---` plain line

**Example Mermaid Syntax:**
```mermaid
graph TD
    subgraph GP_Structure["GP & Management"]
        MGR(["Management Company LLC<br/>Delaware LLC"])
        GP(["General Partner LLC<br/>Delaware LLC"])
        CARRY(["Carry Vehicle LP<br/>Delaware LP"])
    end

    subgraph Fund_Vehicles["Fund Vehicles"]
        FUND[["Main Fund LP<br/>Delaware LP<br/>$500M Target"]]
        PARALLEL[["Parallel Fund LP<br/>Cayman LP"]]
        COINVEST[["Co-Invest Vehicle<br/>Delaware LP"]]
    end

    subgraph Feeders["Feeder Structure"]
        ONSHORE["Onshore Feeder<br/>Delaware LP"]
        OFFSHORE["Offshore Feeder<br/>Cayman LP"]
        BLOCKER["Blocker Corp<br/>Delaware C-Corp"]
    end

    subgraph Investors["Investor Categories"]
        US_TAX>US Taxable LPs]
        US_EXEMPT>US Tax-Exempt LPs]
        NON_US>Non-US LPs]
    end

    subgraph Portfolio["Portfolio Companies"]
        PC1(("PortCo A"))
        PC2(("PortCo B"))
        PC3(("PortCo C"))
    end

    MGR -.->|"Management Fee"| FUND
    GP -->|"Controls"| FUND
    GP -->|"Controls"| PARALLEL
    CARRY -.->|"Carried Interest"| GP

    US_TAX ==>|"Capital"| ONSHORE
    US_EXEMPT ==>|"Capital"| BLOCKER
    NON_US ==>|"Capital"| OFFSHORE

    ONSHORE ==>|"Invests"| FUND
    OFFSHORE ==>|"Invests"| FUND
    BLOCKER ==>|"Invests"| FUND

    FUND ==>|"Invests"| PC1
    FUND ==>|"Invests"| PC2
    PARALLEL ==>|"Co-Invests"| PC2
    COINVEST ==>|"Co-Invests"| PC3
```

**Diagram Guidelines:**
- Group related entities using `subgraph` blocks
- Label all arrows with the relationship type
- Include jurisdiction and legal form in node labels
- Show fund size in fund entity nodes when available
- Keep the diagram readable (avoid crossing arrows where possible)
- Use top-down (`graph TD`) layout for fund structures

---

## Phase 4: Structural Analysis

### 4.1 Structural Concern Flags

Evaluate the fund structure for potential issues:

| Concern | What to Check | Risk Level |
|---------|--------------|-----------|
| **Circular ownership** | Any entity that directly or indirectly owns itself | HIGH |
| **Missing GP entity** | Fund has no clearly identified General Partner | HIGH |
| **Missing management company** | No separate management entity (all functions in GP) — not necessarily bad but worth noting | LOW |
| **Jurisdictional mismatch** | GP in one jurisdiction controlling a fund in another without apparent reason | MEDIUM |
| **No blocker for tax-exempt LPs** | ERISA or tax-exempt investors investing directly without UBTI protection | HIGH |
| **No offshore vehicle** | Non-US investors investing in a US fund without ECI protection | MEDIUM |
| **Excessive entity count** | Unusually complex structure relative to fund size or strategy | MEDIUM |
| **Missing carry vehicle** | No separate carried interest vehicle (carry flows through GP directly) | LOW |
| **Single-entity structure** | No parallel vehicles or feeders for a fund that appears to need them | MEDIUM |
| **Regulatory gap** | Management company appears to require SEC/CFTC registration but status unclear | HIGH |
| **ERISA plan asset risk** | Structure may trigger ERISA plan asset rules (25% benefit plan investor threshold) | HIGH |
| **Missing co-invest vehicle** | Side letters grant co-investment rights but no vehicle exists | LOW |

### 4.2 Structural Optimization Suggestions

Based on the fund type and investor composition, suggest structural improvements:

| Fund Type | Common Structural Enhancement |
|-----------|------------------------------|
| **PE/VC with non-US LPs** | Add offshore parallel or feeder fund for ECI blocking |
| **PE/VC with tax-exempt LPs** | Add blocker corporation for UBTI blocking |
| **Large fund ($1B+)** | Consider master-feeder structure for operational efficiency |
| **Fund with co-invest program** | Establish dedicated co-investment vehicle |
| **Multi-strategy fund** | Consider sleeve structure or AIVs per strategy |
| **Fund with EU investors** | Consider Luxembourg SCSp or Irish ICAV for AIFMD compliance |

---

### Multi-Jurisdiction Validation

- Verify each entity's jurisdiction is stated (flag [MISSING] if not)
- Check for jurisdiction mismatches (e.g., Cayman fund with Jersey GP)
- For parallel/feeder structures, verify each vehicle's purpose matches its jurisdiction
- Generate a jurisdiction summary table: Entity | Jurisdiction | Entity Type | Tax Status

## Phase 5: Generate Output File

### 5.1 Compile the Entity Map Report

Generate `ENTITY-MAP-[fund]-[date].md` with the following structure:

```markdown
# Fund Structure Entity Map

> DISCLAIMER: This entity map is AI-generated and does not constitute legal,
> tax, or investment advice. It is intended for informational and educational
> purposes only. Fund structures involve complex tax, regulatory, and corporate
> law considerations that require review by qualified legal and tax counsel.
> This map is based on information extracted from the provided documents and
> may not reflect the complete current structure. Entity details, jurisdictions,
> and relationships must be independently verified.

---

## Fund Overview

| Field | Value |
|-------|-------|
| Fund Name | [name] |
| GP Entity | [GP name and jurisdiction] |
| Management Company | [name and jurisdiction] |
| Fund Strategy | [type] |
| Primary Jurisdiction | [jurisdiction] |
| Fund Size | [target / hard cap] |
| Total Entities Identified | [count] |
| Date of Analysis | [date] |

---

## Structure Diagram

```mermaid
[Generated Mermaid diagram from Phase 3.2]
```

> To render this diagram, paste the Mermaid code block into any Mermaid-compatible
> viewer (GitHub, Notion, Mermaid Live Editor at mermaid.live, VS Code with
> Mermaid extension, or any Markdown renderer supporting Mermaid).

---

## Entity Registry

| # | Entity Name | Type | Jurisdiction | Legal Form | Role | Controlled By |
|---|------------|------|-------------|-----------|------|--------------|
| 1 | [name] | [type] | [jurisdiction] | [form] | [role] | [parent entity] |
| 2 | [name] | [type] | [jurisdiction] | [form] | [role] | [parent entity] |

---

## Ownership & Control Chain

| Parent Entity | Relationship | Child Entity | Ownership % | Notes |
|--------------|-------------|-------------|-------------|-------|
| [parent] | Controls | [child] | [%] | [notes] |

---

## Capital Flow Map

| Source | Direction | Destination | Flow Type | Notes |
|--------|-----------|------------|-----------|-------|
| [US Taxable LPs] | → | [Onshore Feeder] | Capital Contribution | Direct subscription |
| [Onshore Feeder] | → | [Main Fund] | Investment | Feeder invests in master |
| [Main Fund] | → | [Portfolio Co] | Investment | Fund deploys capital |

---

## Fee Flow Map

| Payer | Recipient | Fee Type | Rate/Amount | Authority |
|-------|-----------|----------|-------------|-----------|
| [Fund] | [Mgmt Co] | Management Fee | [X]% | LPA Section [X.X] |
| [PortCo] | [GP/Mgmt Co] | Monitoring Fee | [amount] | Portfolio company agreement |

---

## Structural Concerns

| # | Concern | Severity | Entities Affected | Recommendation |
|---|---------|----------|-------------------|----------------|
| 1 | [concern] | [HIGH/MEDIUM/LOW] | [entities] | [action] |

---

## Structural Optimization Suggestions

| # | Suggestion | Rationale | Complexity | Priority |
|---|-----------|-----------|-----------|----------|
| 1 | [suggestion] | [why] | [Low/Medium/High] | [P1/P2/P3] |

---

## Recommended Next Steps

1. [ ] Verify entity registry against fund administrator records
2. [ ] Confirm all jurisdictional registrations are current
3. [ ] Review structural concerns with fund formation counsel
4. [ ] Address any missing entities identified in the analysis
5. [ ] Run `/fund review-lpa` to analyze the LPA governing this structure
6. [ ] Run `/fund check-compliance` to verify regulatory compliance of the structure
```

### 5.2 Present to User

After generating the output:

1. Confirm the file was generated with its absolute path
2. State the total entity count and types identified
3. Display the Mermaid diagram code block so the user can render it
4. Highlight any HIGH severity structural concerns
5. Summarize the ownership chain in one sentence (e.g., "GP LLC controls Main Fund LP and Parallel Fund LP, with capital flowing through two feeders and one blocker")
6. Suggest: "Paste the Mermaid code block into mermaid.live to render the diagram visually. Run `/fund review-lpa` for a full analysis of the governing LPA."

---

## Vault Entity Persistence

After generating the entity map, persist entity data to the vault:

1. For each entity in the structure, create or update a vault note at `Documents/Entities/{entity-slug}.md` with frontmatter:
   - `type: entity`
   - `entity-type: fund|gp|lp|management-company|feeder|master|spv|blocker`
   - `jurisdiction: {jurisdiction}`
   - `parent: {parent-entity-name}`
   - `directors: [{name1}, {name2}]`
   - `officers: [{name1}, {name2}]`
   - `status: active|dissolved|pending`

2. Add `## Vault Links` with wikilinks to parent entity and related fund notes.

3. This builds a persistent entity registry queryable via Dataview:
   ```dataview
   TABLE entity-type, jurisdiction, parent
   FROM "Documents/Entities"
   SORT entity-type
   ```

## Error Handling

| Error | Resolution |
|-------|-----------|
| No document provided | Ask user to provide a fund formation document, LPA, or text description of the structure |
| Document contains no entity information | Report that no fund entities were identified; suggest the document may not contain structural information; ask for formation documents or organizational charts |
| Only one entity identified | Generate the map with available information; note that the structure appears incomplete; suggest providing additional documents (side letters, PPM, formation docs) |
| Informal text description provided | Process the description; generate the structure map; mark all details as [USER-PROVIDED] and note they should be verified against legal documents |
| Ambiguous entity relationships | Flag the ambiguity in the structural concerns section; present the most likely interpretation; ask the user to clarify |
| Fund type unclear | Default to PE fund structure conventions; note the assumption |
