# Regulatory and screening hardening — release candidate

Reviewed on 21 September 2026. This is a bounded correction and evidence-validation implementation, not exhaustive legal certification, legal advice or production approval. Common generated policy is maintained by the main integration task; this document covers regulatory-specific behaviour and the screening adapter.

## Source use and dates

[regulatory-sources.json](regulatory-sources.json) records authoritative sources, jurisdictions, access results, review dates and verified effective/compliance dates. READ means the page or PDF was retrieved. SEARCH_EXCERPT means only indexed primary-source text was inspected; it is not full-text verification. UNAVAILABLE records failed retrieval. A null effective date means no single date was established; it must not be replaced with the review date.

Each operational review must establish its own entity, transaction, jurisdiction and relevant date, obtain current applicable text and record unavailable sources. This register does not contain screening lists or authorise using an old list. Legislation, regulator guidance, international standards, fund contracts and internal policy must be distinguished.

Confirmed corrections and boundaries:

- FATF increased monitoring alone is not a FATF requirement for EDD. The June 2026 statement calls for risk-based assessment; domestic law may require additional measures. Call-for-action statements are a separate source. [FATF statement](https://www.fatf-gafi.org/en/publications/High-risk-and-other-monitored-jurisdictions/increased-monitoring-june-2026.html).
- Former-PEP treatment is risk-based, not automatic expiry. UK guidance provides a minimum period for the former office-holder and distinct family/associate treatment. [FATF guidance](https://www.fatf-gafi.org/content/dam/fatf/documents/recommendations/Guidance-PEP-Rec12-22.pdf), [HMRC guidance](https://www.gov.uk/hmrc-internal-manuals/economic-crime-supervision-handbook/ecsh33316). The direct legislation retrieval failed and is recorded.
- UK designation sourcing changed on 28 January 2026; the closed OFSI consolidated list is not a current source. [UK Sanctions List](https://www.gov.uk/government/publications/the-uk-sanctions-list). No static sanctions/FATF country lists remain in the owned skills.
- FinCEN CDD ownership and control tests are distinct and entity scope matters; the 2026 account-opening relief is not an exemption from all CDD. [CDD rule guidance](https://www.fincen.gov/resources/statutes-and-regulations/cdd-final-rule), [FIN-2026-R001](https://www.fincen.gov/system/files/2026-02/FinCEN-Order-CCDExceptiveRelief.pdf). The IA AML rule was deferred to 1 January 2028, without removing other applicable obligations. [FinCEN announcement](https://www.fincen.gov/news/news-releases/fincen-issues-final-rule-postpone-effective-date-investment-adviser-rule-2028).
- Qualified-client monetary tests changed effective 29 June 2026; use the actual contract date, transition provisions and alternative routes. [SEC IA-6961](https://www.sec.gov/files/rules/ia/2026/ia-6961.pdf).
- Form PF thresholds/sections and event scope were corrected. IA-6992 is effective 3 September 2026 and delays compliance for the February 2024 amendments to 1 July 2027, not all existing Form PF duties. [SEC IA-6992](https://www.sec.gov/files/rules/final/2026/ia-6992.pdf). The downloadable reference form must be paired with the applicable-date analysis.
- W-8 expiry is generally calendar-year based, subject to exceptions/changes. W-8BEN-E certification is Part XXX, not XXVIII; entity-status and owner-disclosure parts were corrected. [IRS requester instructions](https://www.irs.gov/instructions/iw8), [W-8BEN-E instructions](https://www.irs.gov/instructions/iw8bene).
- Form 990-T filing scope includes relevant IRA trusts; the gross-income filing threshold is not tax payable and Form 5329 is not the UBTI return. ECTI/section 1446 withholding differs from FDAP. [990-T instructions](https://www.irs.gov/instructions/i990t), [partnership withholding](https://www.irs.gov/individuals/international-taxpayers/partnership-withholding).
- Stale tax-year thresholds, universal CRS/ownership assumptions and dollar-based Annex IV bands were removed in favour of applicable-year/jurisdiction verification. SFDR's old numbered indicator table was removed; [ESMA confirms controversial weapons as indicator 14](https://www.esma.europa.eu/publications-data/questions-answers/2371). Full EUR-Lex RTS/annex access was blocked, so exact current templates and indicators require verification before drafting a disclosure. No comprehensive SFDR certification is claimed.

### Register additions, 23 September 2026

Added for the compliance, filing, calendar and ESG skills; every entry is `reverify_before_use: true` and records how it was accessed:

- US rules and staff guidance: `sec-exam-priorities-fy2026`, `sec-reg-sp-2024` (compliance 3 Dec 2025 larger / 3 Jun 2026 smaller entities; dates read in a law-firm summary), `sec-pfar-vacatur` (Private Fund Adviser Rules vacated; never flag their requirements as missing), `sec-marketing-faq` (FAQ updates 19 Mar 2025 and 15 Jan 2026), `sec-custody-206-4-2` (120-day audited-financials route), `sec-adv-204-1` (90 days after fiscal year end), `sec-form-d-503` (15 calendar days after first sale), `sec-13h-1`, `sec-13f-faq` (45 days, weekend roll), `sec-pay-to-play`, `sec-205-3`. Rule text was read on Cornell LII where eCFR redirected to a bot check; eCFR remains the canonical source.
- Proposals, recorded as PROPOSED and never applied to a current period: `sec-form-pf-2026-proposal` (20 Apr 2026), `eu-sfdr2-proposal` (COM(2025) 841; SEARCH_EXCERPT).
- EU and UK: `eu-aifmd-ii` (transposition 16 Apr 2026, read in a law-firm summary; directive text not retrieved; new Annex IV template date not established), `esma-fund-names` (80% threshold; application dates derived), `uk-sdr-ps23-16` (entity disclosures for firms over GBP 5bn from 2 Dec 2026), `edci-metrics` (voluntary; 2025 data due 30 Apr 2026).

Not added because no source was read: Form N-PX and Schedules 13D/13G deadlines, SFDR entity-level PAI date (30 June), FBAR, advisers-act section 206(3), EDGAR Next dates and state pay-to-play rules. Skills treat these as UNSUPPORTED or CURRENT VERIFICATION REQUIRED.

## Distinct exemption and qualification tests

The skills must evaluate these separately; this adapter does not implement a legal qualification engine.

| Test | Required distinction |
|---|---|
| Rule 506(b) versus 506(c) | Solicitation, purchaser eligibility and verification conditions differ. |
| 3(c)(1), qualifying VC, 3(c)(7) | Counting/capital conditions and QP routes are separate from the Securities Act offering exemption. |
| AI, QP and QC | Different statutes, definitions, valuation dates and evidence; one result must not silently satisfy another. |
| Regulation S | Offshore-transaction and selling-effort/category conditions, not foreign address alone. |
| ERISA | Less-than-25% participation with exclusions/look-through is separate from VCOC/REOC and other exceptions. |
| FATCA, CRS and treaty claims | Different entity/account/payment rules; exemption in one regime does not establish another. |
| CTA BOI versus CDD | A reporting exemption does not remove bank CDD or sanctions checks. |

## Supplied-evidence adapter

Run from the source root:

```sh
python3 scripts/fund_screening.py --input /absolute/path/to/evidence.json
```

The CLI requires a local JSON file; `--input -` is not stdin support. It emits privacy-minimised JSON to stdout and writes no report or external state. There is no live connector, network request, name matching, list download, evidence authentication or human-disposition engine. Installed script/reference resolution belongs to the packaging integration.

Exit codes: 0 means supplied evidence meets the caller's validation requirements; 1 means HOLD/ESCALATE; 2 means invalid or unreadable input. Even exit 0 means only PRELIMINARY READY FOR HUMAN REVIEW, never admission, payment approval or sanctions clearance.

### Version 1 input

All timestamps must have a time zone. `as_of` is the explicit assessment instant; the adapter does not silently substitute the machine clock. Each requirement is one subject/check/jurisdiction/source combination. Use opaque references; keep names, identifiers and evidence documents in access-controlled storage.

```json
{
  "schema_version": 1,
  "as_of": "2026-09-21T09:00:00Z",
  "requirements": [
    {
      "subject_ref": "synthetic-investor-01",
      "check": "sanctions",
      "jurisdiction": "US",
      "source": "synthetic-list",
      "identity_fingerprint": "synthetic-identity-revision-1",
      "max_age_days": 7,
      "max_source_age_days": 2
    }
  ],
  "records": [
    {
      "subject_ref": "synthetic-investor-01",
      "check": "sanctions",
      "jurisdiction": "US",
      "source": "synthetic-list",
      "identity_fingerprint": "synthetic-identity-revision-1",
      "provider": "synthetic-provider",
      "source_version": "synthetic-v1",
      "source_as_of": "2026-09-20T08:00:00Z",
      "screened_at": "2026-09-20T09:00:00Z",
      "expires_at": "2026-09-22T09:00:00Z",
      "evidence_ref": "synthetic-evidence-001",
      "coverage_complete": true,
      "status": "NO MATCH"
    }
  ]
}
```

This example is synthetic and intentionally covers only one source/subject. It is not a real screen or a complete onboarding scope. Freshness values are examples, not statutory windows.

`check` accepts `sanctions`, `pep` or `adverse_media`. Establish the complete subject/source scope separately, including relevant owners, controllers, trust parties and intermediaries; do not let a provider's partial export define the required scope. Each time limit must be an integer from 0 to 3660 days (an input guard, not permission to use decade-old records). Specify the actual approved policy. Scope values that stand in for a missing value are treated as missing, not as scope: a `subject_ref`, `jurisdiction` or `source` such as `UNKNOWN`, `N/A`, `TBD`, `placeholder` or `list-scope-not-supplied` adds `PLACEHOLDER_SCOPE`; an `identity_fingerprint` such as `identity-link-not-supplied` adds `IDENTITY_LINK_NOT_ASSESSED`; and a time limit set to the 3660-day ceiling adds `FRESHNESS_NOT_ASSESSED`. Each makes that check INCOMPLETE (or leaves it POTENTIAL MATCH), never NO MATCH REPORTED. Do not fill scope fields with invented or placeholder values to get a file past validation; if the list scope, jurisdiction, identity link or freshness policy was not supplied, leave the check NOT PERFORMED or INCOMPLETE and say which value is missing. `identity_fingerprint` links to the protected identity revision; equality is not identity authentication. Provider/version/evidence references are assertions whose authenticity and retrievability require independent review.

`status` accepts NO MATCH, POTENTIAL MATCH, CONFIRMED MATCH, NOT PERFORMED or INCOMPLETE. The output deliberately converts any supplied confirmed hit to POTENTIAL MATCH pending qualified human adjudication, retaining an escalation and validation issues. This does not dismiss the supplied hit. Preserve the original evidence in restricted storage.

### Validation and propagation

| Condition | Output |
|---|---|
| Required check has no record | NOT PERFORMED; HOLD |
| All required checks absent | Overall NOT PERFORMED |
| Some complete checks but another absent | Overall INCOMPLETE; absent check remains NOT PERFORMED |
| Stale/expired, incomplete coverage, missing metadata, wrong identity, duplicate records or invalid dates | INCOMPLETE; HOLD |
| Placeholder scope (`UNKNOWN`, `not-supplied`, `N/A`…), placeholder identity link or a freshness limit at the 3660-day ceiling | INCOMPLETE; HOLD; identity linkage or freshness NOT ASSESSED |
| Potential or confirmed hit, even stale or outside requested scope | POTENTIAL MATCH; ESCALATE; other gaps remain visible |
| Every requirement satisfied with no-match records | NO MATCH REPORTED; PRELIMINARY READY FOR HUMAN REVIEW |
| Empty requirements, unknown records or malformed input | Never ready; INCOMPLETE/HOLD or input error |

Source-as-of must precede or equal screening time, screening must not be after `as_of`, and expiry must be strictly after `as_of`. Screen/source age limits are independent and inclusive. Source effective dates and legal applicability still require the surrounding workflow; source-as-of is not a legal effective date. Duplicate records require review rather than latest-record selection. No-match evidence cannot overwrite a hit. Extra fields are ignored in output, but non-finite numbers anywhere are rejected.

The CLI rejects duplicate JSON keys at every nesting level, NaN, positive/negative Infinity and exponent overflow such as `1e999`. This prevents a second `status` field from silently replacing a hit. Failures emit a fixed diagnostic without raw values, file contents or traceback. Python callers must pass JSON-compatible dictionaries and handle `ValueError`; duplicate keys cannot be recovered after another parser has already discarded them.

Only fixed status/diagnostic codes and generated SHA-256 reference tokens are returned. Tokens support correlation to the caller's restricted records; they are not anonymisation, proof of authenticity or hashes of the underlying evidence file. Do not feed raw PII into reference fields. Analytical skill outputs additionally mask identifiers and omit full birth dates, residential addresses and signatures. They are distinct from restricted official filing payloads.

Human match resolutions are not imported by this adapter. Keep an unresolved match escalated and document officer decisions separately; do not remove hits from evidence merely to obtain a green output. The caller must also assess ownership/control, programme/activity restrictions, licences, other AML duties and unperformed work beyond this record schema.

## Verification and integration boundary

Run `python3 -m unittest tests.test_fund_screening -v`. Tests cover scope, timestamps, freshness boundaries, coverage, identity linkage, status propagation, duplicate/conflicting records, malformed JSON, duplicate keys, non-finite values, output privacy, determinism and CLI exit codes. All test records are synthetic.

These tests validate adapter behaviour, not law, provider authenticity or actual screening coverage. Source skill edits remove contradictory static rule tables and require evidence-dependent review. The main task owns shared-policy generation, packaged reference paths and the generated plugin tree. Do not interpret a successful build or test run as regulatory certification.
