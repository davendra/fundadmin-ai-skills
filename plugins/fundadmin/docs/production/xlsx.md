# Spreadsheet companion contract

`scripts/fund_xlsx.py` writes the tables of a review as an Excel workbook
(`.xlsx`) or a CSV file. The Markdown report stays the record. The spreadsheet is
a companion for people who work in Excel, and it carries nothing the report does
not.

## Two ways to call it

After `fund_report.py write-report` has saved the report, attach a companion with
the same stem in the same report directory:

```sh
python3 scripts/fund_report.py companion --report <run>/reports/<id>/CAPITAL-ACCOUNT-REVIEW-....md \
  --spec tables.json --format xlsx
```

The helper refuses the companion when the report or its sidecar is missing, or
when the report's SHA-256 no longer matches its sidecar (it was edited after it
was written). The companion gets its own sidecar, `<name>.xlsx.json`, recording
the run, the report filename, both hashes, the source (`spec` with its SHA-256,
or `report tables`) and `human_review_required: true`. The report's own sidecar
is never rewritten.

A spec can name the report it was built from: `provenance.report_filename` and
`provenance.report_sha256` (as `fund_kyc.py xlsx-spec --report` writes). The
companion is refused when that hash or filename does not match the report being
accompanied, so a revised report cannot be paired with a workbook built for an
earlier revision; rebuild the spec from the revised report. A `fund_kyc.py` spec
must carry this binding. Any other spec without it is accepted with a warning on
stderr to confirm it was built from this revision.

Or, for a report whose tables are the whole story, build the sheets from the
report itself instead of a spec:

```sh
python3 scripts/fund_report.py companion --report <run>/.../FEE-AUDIT-....md --from-report
```

Each Markdown pipe table becomes one sheet, named after the nearest heading above
it (first 20 tables). Cells are copied as written. A column becomes numeric only
when every non-empty cell is a plainly written figure of one kind: `1,250.00`,
`$1,250.00`, `(3,000)` for negatives, or `8.5%` (stored as 0.085). Figures such as
`1.2m`, `USD 5`, `1.23x` and dates stay text, so does a column of bare digits such
as years, and so does any column that mixes figures with text. Nothing is recalculated: the workbook is the report's
tables, so a wrong figure is fixed in the report.

Standalone, for a file outside a run:

```sh
python3 scripts/fund_xlsx.py --input tables.json --output TABLES.xlsx
python3 scripts/fund_xlsx.py --from-markdown --input REPORT.md --output REPORT.xlsx
```

Exit codes: `fund_xlsx.py` prints `XLSX generated: <path>` or `CSV generated:
<path>` and returns 0, or prints `ERROR: ...` and returns 1. `fund_report.py
companion` returns 2 for an invalid or unsafe request and 3 when openpyxl is
missing.

## When openpyxl is missing

`.xlsx` output needs `openpyxl` (pinned in `requirements-plugin.txt`, shipped in
the plugin as `skills/fund/requirements.txt`). Without it the helper creates
nothing and says so: `openpyxl is not installed for <python>; no workbook was
generated`, followed by the exact install command for that Python. The calling skill then re-runs with `--format csv` and tells the
user it produced a CSV. It never renames a CSV to `.xlsx` or silently changes
format.

## Table spec

```json
{
  "schema_version": "1",
  "title": "Capital account review — Fund, period",
  "sheets": [
    {
      "name": "Validation",
      "columns": [
        {"key": "check", "label": "Check", "type": "text"},
        {"key": "expected", "label": "Expected", "type": "currency"}
      ],
      "rows": [{"check": "Ending capital", "expected": 1250000.5}],
      "freeze_header": true,
      "autofilter": true
    }
  ],
  "notes": ["Figures recomputed with fund_calculations.py"],
  "provenance": {"run_id": "...", "report": "CAPITAL-ACCOUNT-REVIEW-....md"}
}
```

- `schema_version` is `"1"`. Unknown keys are rejected everywhere, and so are
  duplicate JSON keys and NaN or Infinity.
- 1 to 20 sheets. A sheet name is at most 31 characters, has none of `[]:*?/\`,
  and is unique. `Notes` is reserved.
- 1 to 60 columns per sheet. `key` matches `[a-z][a-z0-9_]*`. `type` is one of
  `text`, `number`, `integer`, `currency`, `percent` or `date`. The type sets the
  number format; `percent` expects a fraction (0.08 displays as 8.00%).
- Up to 100,000 rows. A row is an object whose keys are column keys; a missing
  key or `null` is an empty cell. Numbers must be finite JSON numbers, never
  strings or booleans. Dates are `YYYY-MM-DD`.
- Every workbook ends with a `Notes` sheet holding the title, the draft-for-human-
  review status line, the provenance pairs and the notes.

## Output safety

The same rules as the PDF helper ([pdf.md](pdf.md)):

- The file is created exclusively with mode `0600`. Existing files, hard links
  and symlinks, dangling ones included, are refused and left unchanged.
- The whole spec is validated and rendered in memory before the file is created,
  so a bad spec leaves no partial file.
- Paths with `..` or a symlinked parent directory are refused.
- Input and output cannot be the same path, and the output extension must match
  the format.

## No formulas

The helper never writes a formula. Text that begins with `=`, `+`, `-`, `@`, a
tab or a carriage return is stored as a text cell in `.xlsx`, and prefixed with
`'` in CSV (the OWASP CSV-injection guard). Values extracted from documents are
therefore inert in Excel, whatever they contain. Totals and recalculations belong
in `fund_calculations.py` and the report, not in spreadsheet formulas.
