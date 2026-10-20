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
label is `LPA document favourability (heuristic, methodology v2)`, for legacy
payloads; it is a heuristic, not a safety verdict. Other assessments should supply
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
  a cell longer than 1,200 characters uses labelled records to avoid clipping:
  one record per row, each value preceded by its bold column name, records
  separated by a thin rule. No pipe-joined header line is printed; a header-only
  wide table still lists its column names.
- Thematic breaks (`---`, `***`, `___`, also spaced as `- - -`) are drawn as a
  thin horizontal rule rather than printed; inside a code fence they stay
  literal text.
- Long paragraphs and records split across pages. Malformed table rows remain
  literal text instead of being discarded.
- Headings (three sizes), pipe tables, bullet and task lists, block quotes and a
  small inline subset receive layout: `**bold**`, `*italic*`, `` `code` `` and
  `[text](https://…)`, which prints as `text (URL)` so the address stays
  visible. Markup characters are removed only where they are typeset. Source
  text is escaped before this subset is applied, so HTML in the source remains
  literal visible text and never executes; footnotes remain literal text. No
  external images or linked content are fetched. Code fences stay literal.
  Whitespace/indentation is not facsimile rendering; this is a text report
  exporter, not a full CommonMark typesetter.
- Report symbols the bundled font cannot draw are mapped to words so their
  meaning survives: 🔴 `HIGH`, 🟠 `ELEVATED`, 🟡 `MEDIUM`, 🟢 `LOW`, ⬜/☐ `[ ]`,
  ☑/✅ `[x]`, ❌ `[no]`, ⚠ `WARNING`, → `->`. Any other unsupported glyph appears
  as a `[U+XXXX]` marker rather than disappearing or becoming a black square;
  for example the full block, light shade, check mark and ballot X print as
  `[U+2588]`, `[U+2591]`, `[U+2713]` and `[U+2717]`. Templates should use plain
  text (`OK`, `FAIL`, `[ ]`, `->`) instead.
  Latin currency and typographic punctuation are covered by the bundled font.
  Full CJK/emoji and complex-script shaping are not supported.
- Page counts are drawn by the PDF canvas; source text is never globally replaced
  to insert totals. No synthetic gauge or score-dependent advisory text is added.
- Original source limitations and citations remain part of the report. An
  AI-generated notice is appended with the exact sentence "Not financial, legal or
  tax advice. Qualified human review is required." and a data-handling note.
- The PDF is untagged: it is not PDF/UA and has no structure tags for screen
  readers. Accessibility is a known limitation.
- When `/fund review-lpa` has already rendered `FUND-REVIEW-REPORT.pdf` for a
  report, `/fund report-pdf` returns that path instead of rendering again; a new
  rendering uses `--output` with a new name in the same report directory.

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

The pinned version in `requirements-plugin.txt` is ReportLab 5.0.1. The 23
September review below ran on ReportLab 4.4.10, an older version than the pin;
repeat it on the pinned version before relying on it for a release.

Visual review on 23 September 2026 (ReportLab 4.4.10, Poppler `pdftoppm`) after
inline typesetting and symbol mapping were added: the Obrelund quickstart LPA
review (17 pages) and ERISA subscription review (10 pages) rendered with no
`[U+…]` markers, no stray `**`, backticks or quote markers in extracted text, and
all sections through the final limitations. Tables still split long rows across
pages with repeated headers. This supersedes the layout description below for
inline Markdown and symbols; the earlier stress-test findings still apply.

Earlier visual review performed on 21 September 2026 using the shared `.venv-hardening`
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

## Reusable Markdown fidelity checker

Run the packaged read-only checker after rendering:

```sh
python3 scripts/fund_pdf_fidelity.py --markdown review.md --pdf review.pdf
```

It requires pypdf and returns JSON on stdout: source/PDF SHA-256 hashes, page and
assessed-unit counts, mismatches with Markdown line numbers, and reconstructed
table continuations. Exit 0 means all assessed source units matched; exit 1 means
mismatches; exit 2 means an input, dependency or unsupported-format error (JSON on
stderr). Save the output under a fresh workpaper name; the helper never writes to
its inputs. A failed check must not be reported as a fidelity pass.

The checker independently interprets the renderer's Markdown subset. It ignores
layout whitespace and known generated footer spans only within the footer area.
Case, punctuation, decimal points, percentages, currency, signs, comparison
operators, qualifications and citation text remain significant. Prose occurrences
are matched in source order. Tables are checked within their own rows and columns;
repeated headers are recognised by content and column positions, and split cells
are reconstructed across pages. No document-specific fragment exceptions are used.

This is a source-content check, not an exact PDF diff: it does not reject arbitrary
extra PDF prose, assess factual accuracy, or certify layout/accessibility. Whitespace
normalisation cannot distinguish differences consisting solely of whitespace.
It accepts Markdown, not structured JSON, and ordinary unrotated horizontal text.
Tables need non-empty first-column row anchors and distinguishable column positions;
unsupported layouts/glyphs can require manual investigation, never a silent pass.
Encrypted, rotated and non-extractable PDFs fail closed. Continue visual review of
all pages, especially table continuations and the final limitations/disclaimer.

`tests/test_fund_pdf_fidelity.py` renders both valid and deliberately corrupted
reports, including changed decimals, signs, operators, qualifiers, citations,
missing repeated paragraphs, moved table values, continuations and footer literals.
It is required by the offline production gate, which rejects dependency skips.
