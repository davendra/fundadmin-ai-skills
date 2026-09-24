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
   The output also carries `completeness`, `tax_forms`, `expiring`,
   `refresh_overdue` and the screening scope (below).

## What the evaluation checks beyond the grid

**Screening scope and date.** Evidence counts only for the subjects and the date
it covers. The evidence file's `subject_ref` values must be the record's own
references (`investor-07`, `bo-1`, `ctl-1`); the mapping from a provider's
subject to a record reference is kept in the run folder and is never changed to
make coverage pass. The required subjects (`screening.required_subjects`) are
the record's `subject_ref`, every natural-person owner at or above the grid's
`ubo_threshold_pct` or with no percentage (every natural-person owner when no
grid is supplied) and every controller. Each needs a `sanctions`, `pep` and
`adverse_media` requirement in the evidence; any missing pair is listed in
`screening.uncovered`. The evidence `as_of`, converted to a UTC date, must not
be earlier than the record's `as_of` (the review date): every freshness window
is measured from the evidence `as_of`, so a later date can only tighten them,
while an earlier one would let a stale screen through. A missing subject or
check, or evidence dated before the review date, turns NO MATCH REPORTED into
INCOMPLETE (HOLD). A POTENTIAL MATCH is never downgraded: it still gives
ESCALATE FOR EDD and the scope gaps are listed as further reasons. Entity owners
are not required by the helper; a firm that screens them adds them to the
evidence, and extra subjects do no harm.

**Identity.** `identity.legal_name_present: false` or
`registration_or_id_present: false` adds an `Identity:` reason and routes to
REQUEST DOCUMENTS at best.

**Tax forms.** Each supplied form is normalised (`w8 ben e` -> `W-8BEN-E`) and
given a state. W-8BEN, W-8BEN-E, W-8ECI and W-8EXP are valid until 31 December
of the third succeeding calendar year after signature (general rule, Treas. Reg.
1.1441-1(e)(4)(ii); exceptions and changes in circumstances need a person). A
W-8 of those types with no signature date is INCOMPLETE. W-9 and W-8IMY get no
routine expiry. An EXPIRED or INCOMPLETE form routes to REQUEST DOCUMENTS; an
EXPIRING one is listed in `expiring` and does not change the disposition. The
grid condition `tax_form_missing` (`forms: [...]`) triggers when none of the
listed forms is RECEIVED or EXPIRING.

**Completeness.** `completeness: {received, required, pct}` counts the grid's
required documents for this applicant type and risk rating; RECEIVED and
EXPIRING count as received. `pct` is rounded down, so 100 means every required
document is on file. Without a grid, or with no required documents, all three
values are `null` (NOT CALCULABLE). It measures document collection only, never
readiness or compliance.

**Refresh.** `refresh_due` is `last_completed_review` plus the grid's
`refresh_months` for the rating; `refresh_overdue` is `true` when that date is
before the review date, `null` when there is no completed review on file. It is
an alert for the tracker and does not change the disposition. `expiring` lists
received documents and tax forms that expire within `expiry_warning_days`
(default 60).

`fund_kyc.py xlsx-spec --evaluation e.json [--evaluation e2.json ...]` turns one
evaluation into a review workbook spec, or several into a tracker, for
`fund_xlsx.py` / `fund_report.py companion` ([xlsx.md](xlsx.md)). The tracker's
Investors sheet has refresh-overdue and completeness columns; its Open items
sheet has blank Owner and Target date columns for the team to fill in.

One reader record and one evaluation per investor per run. `aml-screen`
produces and validates the screening evidence file; `kyc-review` owns the
evaluation. A skill that finds a validated record or evaluation for the same
investor and review date already in the run reuses it instead of reading or
evaluating again.

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
`no_controller_identified`, `tax_form_missing`); nothing in a grid is executed
as code. Run `fund_kyc.py validate-grid --grid <file>` before citing a grid as a
requirement basis: a grid that fails, or that reports `EXAMPLE GRID`, is never a
basis, and the basis is UNKNOWN (policy not supplied).

## Dispositions

| Disposition | When | `operational_readiness` |
|---|---|---|
| ESCALATE FOR EDD | Any screening hit (potential or confirmed), a high risk rating, or a rule routed `escalate-edd` | ESCALATE |
| HOLD | Injection suspected or a source unreadable; no grid supplied (nothing evaluated) | HOLD |
| REQUEST DOCUMENTS | A required document is missing, incomplete or expired; an identity flag is false; a tax form is expired or incomplete; or a rule routed `request-docs` | HOLD |
| HOLD | Screening not performed or incomplete, screening scope short of the required subjects or dated before the review date, a rule routed `hold`, a factor or rule that could not be evaluated, or the example grid | HOLD |
| PRELIMINARY READY FOR HUMAN REVIEW | None of the above: every required document current, identity flags present, no expired or incomplete tax form, every required subject screened with NO MATCH REPORTED on or after the review date, a firm grid, no rule triggered | PRELIMINARY READY FOR HUMAN REVIEW |

Rows are checked in order and the first that applies wins. Every reason is listed
whichever disposition wins, so a hit never hides a missing document or the
reverse. There is no disposition that admits, rejects, clears or declines an
investor, and no input can produce one: a person makes that decision and records
it separately.

In a report, readiness maps to the evidence sidecar `status` with the table in
`references/report-contract.md`: HOLD (which includes REQUEST DOCUMENTS) ->
BLOCKED; ESCALATE -> PARTIAL, or BLOCKED when a blocking check was not
performed; PRELIMINARY READY FOR HUMAN REVIEW -> READY_FOR_REVIEW only with no
UNKNOWN findings and no checks not performed, otherwise PARTIAL. When a
consolidating report sees both ESCALATE and HOLD items, ESCALATE wins and every
HOLD item stays listed.

Without the helper (no Python, or a failing run) no skill may report NO MATCH
REPORTED or PRELIMINARY READY FOR HUMAN REVIEW: screening is INCOMPLETE or NOT
PERFORMED and readiness is HOLD.

## Errors

On invalid input the CLI prints a fixed code, e.g.
`{"error": "DUPLICATE_KEY", "disposition": "HOLD", "operational_readiness": "HOLD"}`,
and exits 2. It never echoes values from the record, because they come from
investor documents.
