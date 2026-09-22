# KYC routing contract

`scripts/fund_kyc.py` is the deterministic half of the KYC skills
(`kyc-review`, `aml-screen`, `kyc-tracker`, `investor-onboard`). The model reads
the documents; this helper applies the firm's rules and routes the result. It
has no network access and makes no decision about an investor.

## The three steps

1. **Read.** A reader, isolated where the host allows it, turns the onboarding
   documents into a KYC record (`kyc-reader.md`, schema in `kyc-record-schema.md`; both in the fund skill's
   `references/`, `fund/references/` in the source).
   The record carries references and locators, not names or ID numbers.
2. **Check.** `fund_kyc.py validate-record --record r.json` rejects unknown or
   duplicate fields, invalid dates, out-of-range percentages and missing locators.
3. **Evaluate.** `fund_kyc.py evaluate --record r.json [--grid firm.yaml]
   [--screening evidence.json]` returns JSON with the risk rating and factors, a
   document matrix, one outcome per rule, the disposition, the reasons and fixed
   limitations. Screening evidence uses the `fund_screening.py` version 1 input
   ([regulatory.md](regulatory.md)) and is validated by that helper, unchanged.

`fund_kyc.py xlsx-spec --evaluation e.json [--evaluation e2.json ...]` turns one
evaluation into a review workbook spec, or several into a tracker, for
`fund_xlsx.py` / `fund_report.py companion` ([xlsx.md](xlsx.md)).

## Rules grid

The grid is the firm's policy expressed as data: risk factors and thresholds,
required documents by applicant type and risk, refresh cycles, jurisdiction lists
and rules. The shipped `kyc-rules-grid.example.yaml` (next to the reader in `references/`)
shows the structure and is marked `example: true`; its values are placeholders,
not recommendations. A firm grid sets `example: false` and must name an `owner`
and `effective_date`. Conditions come from a fixed list the helper implements
(`document_missing`, `document_expired`, `pep_declared_in`, `funds_status_in`,
`chain_depth_over`, `no_natural_person_owner_at_threshold`,
`unknown_ownership_pct`, `jurisdiction_in_list`, `applicant_type_in`,
`no_controller_identified`); nothing in a grid is executed as code.

## Dispositions

| Disposition | When | `operational_readiness` |
|---|---|---|
| ESCALATE FOR EDD | Any screening hit (potential or confirmed), a high risk rating, or a rule routed `escalate-edd` | ESCALATE |
| HOLD | Injection suspected or a source unreadable; no grid supplied (nothing evaluated) | HOLD |
| REQUEST DOCUMENTS | A required document is missing, incomplete or expired, or a rule routed `request-docs` | HOLD |
| HOLD | Screening not performed or incomplete, a rule routed `hold`, a factor or rule that could not be evaluated, or the example grid | HOLD |
| PRELIMINARY READY FOR HUMAN REVIEW | None of the above: every required document current, all screening checks NO MATCH REPORTED, a firm grid, no rule triggered | PRELIMINARY READY FOR HUMAN REVIEW |

Rows are checked in order and the first that applies wins. Every reason is listed
whichever disposition wins, so a hit never hides a missing document or the
reverse. There is no disposition that admits, rejects, clears or declines an
investor, and no input can produce one: a person makes that decision and records
it separately.

## Errors

On invalid input the CLI prints a fixed code, e.g.
`{"error": "DUPLICATE_KEY", "disposition": "HOLD", "operational_readiness": "HOLD"}`,
and exits 2. It never echoes values from the record, because they come from
investor documents.
