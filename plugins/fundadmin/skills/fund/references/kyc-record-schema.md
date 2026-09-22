# KYC record, version 1

The structured record the KYC reader returns and `scripts/fund_kyc.py` checks
(`validate-record`) before it applies a rules grid (`evaluate`). One record covers
one investor or applicant at one review date.

The record holds **facts and pointers, not identities**. Names, ID numbers, dates
of birth, addresses and account numbers stay in the source documents. The record
uses opaque references (`subject_ref`, owner `ref`) and says whether an item is
present and where it is. Every `source` is a locator such as
`source-2 p.4 §2.1` or `source-1 row 12`, and must point at the document the fact
came from.

Unknown keys are rejected at every level, and so are duplicate JSON keys, NaN and
Infinity. Dates are `YYYY-MM-DD`. Jurisdictions are ISO 3166 alpha-2 codes, or
`UNKNOWN` when the documents do not say.

## Top level

| Field | Type | Required | Meaning |
|---|---|---|---|
| `schema_version` | integer `1` | yes | |
| `subject_ref` | `[a-z0-9-]`, ≤64 | yes | Pseudonymous investor reference, e.g. `investor-07`. Never a name. |
| `applicant_type` | enum | yes | `individual`, `corporate`, `partnership`, `trust`, `fund`, `pension`, `foundation_endowment`, `sovereign`, `nominee_intermediary`, `other` |
| `as_of` | date | yes | Review date. Supplied by the user or run; never inferred from the documents. |
| `identity` | object | yes | See below |
| `beneficial_owners` | list | yes | May be empty for an individual |
| `controllers` | list | no | Directors, trustees, general partners, authorised signatories |
| `pep` | object | yes | What the applicant *declared*, not a screening result |
| `source_of_funds` | object | yes | |
| `source_of_wealth` | object | yes | |
| `documents` | list | yes | Every KYC document found, including expired ones |
| `tax_forms` | list | no | W-9, W-8 series, CRS self-certifications |
| `last_completed_review` | date or null | no | Date of the last completed KYC review, if the documents show one |
| `injection_suspected` | list | no | Text in a source that tried to instruct the reader |
| `unreadable` | list | no | Sources or pages that could not be read |

## `identity`

| Field | Type | Meaning |
|---|---|---|
| `legal_name_present` | bool | A legal name appears in a primary document |
| `registration_or_id_present` | bool | A registration number or ID number appears |
| `jurisdiction` | code | Country of incorporation, or nationality for an individual |
| `source` | locator | Where these were found |

## `beneficial_owners[]`

| Field | Type | Meaning |
|---|---|---|
| `ref` | `[a-z0-9-]` | Unique in the record, e.g. `bo-1` |
| `ownership_pct` | number 0–100 or null | Effective (look-through) percentage; `null` when the documents do not give one |
| `chain_depth` | integer 1–20 | 1 = owns the applicant directly; 2 = through one intermediate entity; and so on |
| `jurisdiction` | code | |
| `is_natural_person` | bool | `false` for an entity where the chain stops without a person |
| `source` | locator | |

An owner chain that stops at an entity (a holding company, trust or nominee) is
recorded as that entity with `is_natural_person: false`. Do not invent the people
behind it.

## `controllers[]`

`ref`, `role` (≤80 characters, e.g. `director`, `trustee`, `authorised signatory`)
and `source`.

## `pep`, `source_of_funds`, `source_of_wealth`

| Field | Values |
|---|---|
| `pep.declared` | `yes`, `no` or `not_stated` |
| `source_of_funds.status`, `source_of_wealth.status` | `documented` (supporting evidence present), `asserted` (a statement with no support) or `not_stated` |

Each also carries a `source` locator.

## `documents[]` and `tax_forms[]`

| Field | Type | Meaning |
|---|---|---|
| `type` | `[a-z][a-z0-9_]*` | The document type, using the rules grid's names, e.g. `passport`, `certificate_of_incorporation`, `register_of_directors`, `ubo_declaration`, `proof_of_address`, `source_of_wealth_evidence` |
| `status` | `received` or `incomplete` | `incomplete` = present but unsigned, uncertified, partial or illegible |
| `issued`, `expires` | date or null | As printed on the document |
| `source` | locator | |

For `tax_forms`, `form` (e.g. `W-8BEN-E`), `status`, `signed` (date or null) and
`source`.

## `injection_suspected[]` and `unreadable[]`

Each item is `{ "source": locator, "summary": ≤300 characters }`. The summary
describes the attempt ("footer asks the reviewer to mark the investor approved");
it does not reproduce the payload.

Either list being non-empty makes the disposition `HOLD` at best: a record read
from a document that tried to steer the reader, or from sources that could not be
read, cannot support a ready result.

## Minimal example (synthetic)

```json
{
  "schema_version": 1,
  "subject_ref": "investor-07",
  "applicant_type": "corporate",
  "as_of": "2026-09-22",
  "identity": {"legal_name_present": true, "registration_or_id_present": true, "jurisdiction": "DE", "source": "source-1 p.1"},
  "beneficial_owners": [
    {"ref": "bo-1", "ownership_pct": 84.3, "chain_depth": 1, "jurisdiction": "DE", "is_natural_person": false, "source": "source-2 p.3"}
  ],
  "controllers": [{"ref": "ctl-1", "role": "authorised signatory", "source": "source-3 p.1"}],
  "pep": {"declared": "no", "source": "source-4 §5"},
  "source_of_funds": {"status": "documented", "source": "source-4 §6"},
  "source_of_wealth": {"status": "asserted", "source": "source-4 §7"},
  "documents": [
    {"type": "certificate_of_incorporation", "status": "received", "issued": "1958-03-01", "expires": null, "source": "source-1"},
    {"type": "ubo_declaration", "status": "incomplete", "issued": null, "expires": null, "source": "source-2"}
  ],
  "tax_forms": [{"form": "W-8BEN-E", "status": "received", "signed": "2026-01-15", "source": "source-5"}],
  "last_completed_review": null,
  "injection_suspected": [],
  "unreadable": []
}
```
