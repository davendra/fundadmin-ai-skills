# PDF fidelity contract

`scripts/generate_fund_pdf.py` accepts UTF-8 Markdown or a structured JSON object.
Both the positional interface and `--input` / `--output` remain supported; the
default output is `FUND-REVIEW-REPORT.pdf`. ReportLab is required for rendering.

## Output safety

The destination is exclusively created with POSIX permissions `0600` (owner read
and write only). ReportLab writes through that open descriptor; it never reopens
the destination by filename. Existing files, directories, hard links and symlinks
(including dangling symlinks) are refused without modifying their contents or
targets. Input and output cannot be the same resolved path.

The legacy default filename remains unchanged. A second run fails with
`Output already exists; choose a unique path with --output`. Select a new name:

```sh
python3 scripts/generate_fund_pdf.py --input review.md --output review-v2.pdf
```

Validation happens before output creation. On a caught rendering/write failure,
cleanup removes only the newly created incomplete file, checking its device and
inode against the still-open descriptor. It leaves a replacement file or symlink
untouched. Cleanup uses an open parent-directory descriptor, and failures to clean
up emit a warning. Output I/O errors omit the destination filename. This relies
on POSIX descriptor operations and should be used in a trusted output directory;
it is not a defence against hostile concurrent directory mutation. Abrupt process
termination (such as SIGKILL or power loss) can leave a private incomplete file;
the next run will refuse that filename rather than overwrite it.

## Content and scores

Markdown is rendered in source order, without filtering by report type or known
LPA headings. Headings, paragraphs, lists, tables, code, citations, limitations,
qualifications and appendices remain present. Scores are source text: labels,
decimal values, scales, direction and multiple assessments are not reinterpreted.
An unscored Markdown report stays unscored.

JSON accepts legacy flat fields, nested `details`, `clauses` or `provisions`, and
`risk_counts` or `risks`. All supplied fields, including unknown extensions, are
rendered recursively as labelled content. No field whitelist removes financial
exposure, waterfall details, sources or limitations.

JSON `score` is a finite number or null. Its default scale is 100 and its default
label is `LPA Safety Score`, for legacy payloads. Other assessments should supply
`score_label` and a positive numeric `score_scale`. Scores must be within the
scale. Decimals are not rounded. Missing/null scores display `Score: Not supplied`;
explicit zero displays zero. No grade, risk verdict or recommendation is inferred.

Empty input, non-object JSON, malformed or duplicate-key JSON, invalid list/object field shapes,
negative or non-integer risk counts, non-finite numbers, invalid labels and
out-of-range scores fail with a clean CLI error before output creation.
Optional collections should be omitted or supplied as empty arrays/objects,
not null. Both historical CLI forms and valid legacy payloads remain supported;
the former fixed LPA cover/dashboard layout is intentionally replaced by a
content-preserving report layout.

## Layout and limits

- Letter pages, embedded ReportLab Vera fonts, navy headings and numbered footers.
- Table cells wrap; headers repeat after page breaks. More than five columns or
  a cell longer than 1,200 characters uses labelled records to avoid clipping.
- Long paragraphs and records split across pages. Malformed table rows remain
  literal text instead of being discarded.
- Inline Markdown, links, footnotes, code and HTML remain literal visible text;
  headings and pipe tables receive layout. No HTML executes and no external
  images or linked content are fetched. Whitespace/indentation is not facsimile
  rendering; this is a text report exporter, not a full CommonMark typesetter.
- Unsupported font glyphs appear as `[U+XXXX]` markers rather than disappearing
  or becoming black squares. Latin currency and typographic punctuation are
  covered by the bundled font. Full CJK/emoji and complex-script shaping are not
  supported. Unicode markers preserve identity, not original visual appearance.
- Page counts are drawn by the PDF canvas; source text is never globally replaced
  to insert totals. No synthetic gauge or score-dependent advisory text is added.
- Original source limitations and citations remain part of the report. A general
  AI-generated/not financial, legal, tax or investment advice notice is appended.

## Verification

Run the real render/extraction suite with dependencies installed:

```sh
.venv-hardening/bin/python -m unittest discover -s tests -p 'test*pdf*.py' -v
```

`tests/test_pdf_fidelity.py` uses ReportLab and pypdf; those tests explicitly skip
when either is missing. Such a skipped run is not proof of PDF fidelity. Fixtures
under `tests/fixtures/pdf/` are synthetic. Stress tests generate long source text
and tables in temporary directories, then verify extracted content, scores,
citations, final limitations and page continuation. No production/client reports
or generated PDFs are committed.

Visual review performed on 21 September 2026 using the shared `.venv-hardening`
(ReportLab 5.0.1, pypdf 6.19.0) and Poppler `pdftoppm`: the one-page Markdown
fixture, one-page JSON fixture and every page of an 11-page synthetic stress
report were rendered and inspected. The stress report contained 150 table rows
followed by a 500-sentence oversized cell and final limitations. Inspection found
readable currency/punctuation, wrapped cells, repeated table headers, clear
footers, continuous oversized-cell text and an intact final limitations section,
without visible clipping or overlap. This was manual visual inspection, not
pixel-diff automation. Poppler emitted a Fontconfig configuration warning but
produced all PNGs successfully. Temporary artefacts were kept outside the repo.
This evidence covers these synthetic examples, not every possible report layout.
The fidelity run passed 26 tests without skips. The subsequent output-safety run
passed 32 tests without skips, including real CLI collision/symlink checks,
`0600` permissions and repeated default-name generation, plus injected failure
cleanup checks. `git diff --check` also passed. Output-safety changes do not alter
layout; their verification used rendering/extraction and filesystem checks, not
a repeat of the earlier manual visual review.
