# LPA scoring — methodology v2

The pipeline runs **terms first → risk, compliance and obligations in parallel → recommendations last**. Each downstream agent receives the source document manifest, full text and completed terms inventory. Recommendations receive all four outputs, including failure and uncertainty records. Inline execution follows the same dependency order. Retry a failed agent once; preserve an unavailable dimension if it still fails. Never substitute another agent's opinion.

The score describes **document favourability to an LP**, using an author's heuristic. It is neither a safety verdict, a legal compliance certification nor an investment recommendation. The legacy label “LPA Safety Score” must carry this qualification and methodology version. Do not issue investment verdicts. Recommendations are excluded: the quality or number of proposed changes says nothing about the existing document. Version 1's five-agent weights are not comparable to v2.

## Calculation

| Dimension | Input | Weight | Effective weight |
|---|---|---|---|
| Terms | 0–100, higher is more LP-protective | 20 | 25% |
| Risk | 1–10, higher is worse | 25 | 31.25% |
| Compliance | 0–100, higher is more adequately addressed | 20 | 25% |
| Obligations | 0–100, higher is clearer and more balanced | 15 | 18.75% |

Convert risk to favourability with `R = (10 - risk) × 100 / 9`.
Aggregate = `(20 × terms + 25 × R + 20 × compliance + 15 × obligations) / 80`.
Keep full precision until the final result; round to two decimals, half up. Displayed contributions may differ from the total by 0.01 due to rounding. Do not round a risk mean before conversion.

Omitted or null dimensions make the aggregate `null`, status `unavailable`; list missing dimensions. Do not renormalise over the available subset, use a midpoint, infer a zero, or invent a replacement. A documented absent protection is a finding and can score zero; missing evidence is not evidence of an absent protection.

## Dimension assessment and evidence

Before scoring, record the applicable assessment inventory and exclusions. Each assessed item needs a stable finding ID, document ID/version, page/section (or text line range), supporting quotation and rationale. For absence findings record the reviewed scope and search, rather than inventing a quotation. Retain item inputs and arithmetic in the review so the dimension values can be reproduced.

- Terms: mean of the terms agent's 0–5 provision protection/completeness ratings, multiplied by 20. Completeness here concerns drafting, not extraction confidence. A fully extracted but GP-favourable provision can score poorly.
- Risk: mean of provision risk composites (1–10). Each composite uses severity 40%, likelihood 25%, exposure 20%, asymmetry 15%. These are reasoned assessments, not observed probabilities. Unknown factors make the item and hence dimension unavailable.
- Compliance: mean of applicable documented checks, rated 0 (identified deficiency), 50 (partially addressed) or 100 (adequately addressed in the document). Record jurisdiction, applicability, authority identifier/version and checked date. Unknown applicability or unverified required authority makes the dimension unavailable. A wholly inapplicable dimension is unavailable, not an automatic 100.
- Obligations: mean of item ratings, 0 (unclear or materially one-sided), 50 (partly specified or limited safeguards), 100 (clear actor, trigger, deadline and balanced safeguards), with rationale. Do not infer balance from counts of GP and LP duties.

Use equal item weights within each dimension; freeze and disclose the inventory to avoid selective omissions or duplicate counting. Any unresolved required item makes its dimension unavailable. These rubrics involve judgement; the CLI makes aggregation reproducible, not objective.

Coverage is separately reported as assessed/expected checks and percentage, with exclusions, unreadable sections and confidence rationale. It measures review coverage, not favourability or probability that the analysis is correct. High coverage can accompany very poor terms. The CLI neither infers confidence nor weights favourability by coverage. It validates source identifiers structurally; the reviewer must verify them against the source manifest.

## Standard-library JSON CLI

Run from the repository root: `python3 scripts/fund_lpa_score.py --input review-score-input.json`.
Omit `--input` or pass `--input -` to read stdin. JSON goes to stdout; validation errors go to stderr with exit code 2. An unavailable aggregate is a valid result (exit 0). The CLI does not write or overwrite files.

```json
{
  "dimensions": {
    "terms": {"value": 80, "source_ids": ["DOC-1:TERMS"], "rationale": "Mean provision rating 4/5; see retained item table"},
    "risk": {"value": 4, "source_ids": ["DOC-1:RISK"], "rationale": "Mean unrounded composite 4; see factor table"},
    "compliance": {"value": 75, "source_ids": ["DOC-1:COMPLIANCE"], "rationale": "Mean applicable check rating 75"},
    "obligations": {"value": 60, "source_ids": ["DOC-1:OBLIGATIONS"], "rationale": "Mean obligation rating 60"}
  },
  "coverage": {"assessed": 18, "expected": 20}
}
```

This yields 70.83 favourability and 90% coverage. Only the four named dimensions are accepted; recommendations are rejected as an input. Unknown fields, duplicate keys, booleans, numeric strings, non-finite numbers, out-of-range values and empty evidence references are errors. `coverage` may be omitted or null. Retain the exact input and output JSON alongside the report under collision-safe names for audit.
