#!/usr/bin/env python3
"""Local evidence/run contract. No network access; no business approvals."""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import unicodedata
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

VERSION = '1.0'
FOLDERS = {'reports', 'analysis', 'drafts', 'compliance', 'tracking', 'analytics', 'portfolio'}
KINDS = {'DOCUMENT_FACT', 'CALCULATION', 'ASSUMPTION', 'EXTERNAL_EVIDENCE', 'UNKNOWN'}
STATUSES = {'DRAFT', 'PARTIAL', 'BLOCKED', 'READY_FOR_REVIEW'}
MAX_FILENAME = 180
SLUG_HASH_LENGTH = 12
SLUG_RULE = '^[a-z0-9][a-z0-9-]{0,79}$'


class ReportInputError(ValueError):
    """A rule violation whose message is fixed text written here.

    The CLI prints these messages. They name the field and the rule, never a
    value taken from the report, because values can come from fund documents.
    """


def required(ok, message):
    if not ok:
        raise ReportInputError(message)


def slug(value, field='identifier'):
    if isinstance(value, str) and re.fullmatch(SLUG_RULE[1:-1], value):
        return value
    if not isinstance(value, str) or not value:
        problem = 'is missing or not a string'
    elif len(value) > 80:
        problem = 'is longer than 80 characters'
    elif re.fullmatch(SLUG_RULE[1:-1], value.lower()):
        problem = 'contains uppercase letters'
    elif value[0] == '-':
        problem = 'starts with a hyphen'
    else:
        problem = 'contains characters other than a-z, 0-9 and hyphen'
    raise ReportInputError(f'{field} {problem}; it must match {SLUG_RULE} '
                           '(lowercase letters, digits and hyphens, at most 80 characters)')


def safe_slug(name, max_length=80):
    """Derive a path label, never a legal name or a unique entity identifier."""
    required(isinstance(name, str) and bool(name.strip()), 'Missing name')
    required(type(max_length) is int and 14 <= max_length <= 80, 'Invalid slug length')
    # NFC gives canonically equivalent Unicode the same label. The hash retains
    # distinctions lost by case folding, punctuation removal and truncation.
    identity = unicodedata.normalize('NFC', name)
    ascii_name = unicodedata.normalize('NFKD', identity).encode('ascii', 'ignore').decode('ascii')
    stem = re.sub(r'[^a-z0-9]+', '-', ascii_name.lower()).strip('-') or 'fund'
    suffix = hashlib.sha256(identity.encode('utf-8')).hexdigest()[:SLUG_HASH_LENGTH]
    stem = stem[:max_length - SLUG_HASH_LENGTH - 1].rstrip('-')
    return slug(f'{stem}-{suffix}')


def report_filename(family, fund_name, report_date, qualifiers=()):
    """Return one bounded Markdown basename for direct and routed skills."""
    required(isinstance(family, str) and re.fullmatch(r'[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*', family), 'Invalid filename family')
    required(isinstance(report_date, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', report_date), 'Invalid report date')
    try:
        date.fromisoformat(report_date)
    except ValueError:  # its message echoes the value
        raise ReportInputError('Invalid report date: not a real calendar date') from None
    required(isinstance(qualifiers, (list, tuple)), 'Invalid filename qualifiers')
    names = [fund_name, *qualifiers]
    # Include all separators, the date and extension in the total byte budget.
    budget = MAX_FILENAME - len(family) - len(report_date) - len('.md') - len(names) - 1
    component_length = min(80, budget // len(names))
    required(component_length >= 14, 'Too many or oversized filename components')
    components = [safe_slug(name, component_length) for name in names]
    return valid_filename('-'.join([family, *components, report_date]) + '.md')


def valid_filename(filename):
    required(isinstance(filename, str) and re.fullmatch(r'[A-Z][A-Z0-9-]*-[A-Za-z0-9-]+\.md', filename) and len(filename) <= MAX_FILENAME, 'Invalid report filename')
    return filename


def no_symlinks(path):
    # Reject traversal before abspath can hide a symlink followed by '..'.
    required('..' not in Path(path).parts, 'Parent path traversal is not supported')
    path = Path(os.path.abspath(path))
    required(not any(p.is_symlink() for p in [path, *path.parents]), 'Symlink paths are not supported')
    return path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def private_json(path, data):
    with path.open('x', encoding='utf-8') as f:
        os.chmod(path, 0o600)
        json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')


def load(path):
    def reject_constant(_):
        raise ReportInputError('Non-finite JSON number (NaN or Infinity) is not allowed')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            required(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'), parse_constant=reject_constant, object_pairs_hook=unique)
    except json.JSONDecodeError as exc:  # report only the position, never the text
        raise ReportInputError(f'Invalid JSON at line {exc.lineno} column {exc.colno}') from None


def create_run(root, fund, inputs):
    root = no_symlinks(root)
    required(root.is_dir(), 'Output root must already exist')
    slug(fund, 'fund slug')
    input_paths = []
    for value in inputs:
        source = no_symlinks(value)
        required(source.is_file(), 'Input must be an existing regular file')
        input_paths.append(source)
    now = datetime.now(timezone.utc)
    parent = root / 'reviews' / fund / now.strftime('%Y-%m-%d')
    no_symlinks(parent)
    # Create each new directory privately; do not chmod existing operator directories.
    for directory in (root / 'reviews', root / 'reviews' / fund, parent):
        directory.mkdir(mode=0o700, exist_ok=True)
    run = parent / uuid.uuid4().hex
    run.mkdir(mode=0o700)
    sources = []
    if input_paths:
        retained = run / 'sources'
        retained.mkdir(mode=0o700)
        for index, source in enumerate(input_paths, 1):
            source_id = f'source-{index}'
            copy = retained / source_id
            with source.open('rb') as original, copy.open('xb') as snapshot:
                os.chmod(copy, 0o600)
                shutil.copyfileobj(original, snapshot)
            sources.append({'id': source_id, 'sha256': digest(copy), 'size_bytes': copy.stat().st_size})
    private_json(run / 'run.json', {'schema_version': VERSION, 'run_id': run.name,
                                  'created_at': now.isoformat(), 'fund': fund, 'sources': sources})
    return run


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(report):
    required(isinstance(report, dict), 'Report must be a JSON object')
    required(report.get('schema_version') == VERSION, f'schema_version must be the string "{VERSION}"')
    slug(report.get('report_id'), 'report_id')
    required(nonempty(report.get('skill')) and report['skill'].startswith('fund'),
             'skill must be the producing skill name, starting with "fund"')
    required(report.get('status') in STATUSES, 'status must be one of ' + ', '.join(sorted(STATUSES)))
    required(report.get('human_review_required') is True, 'human_review_required must be true')
    for key in ('sources', 'findings', 'assumptions', 'limitations', 'checks_not_performed'):
        required(isinstance(report.get(key), list), f'{key} must be a list')
    for key in ('assumptions', 'limitations', 'checks_not_performed'):
        required(all(nonempty(v) for v in report[key]), f'{key} entries must be nonempty strings')
    ids = set()
    for i, source in enumerate(report['sources']):
        where = f'sources[{i}]'
        required(isinstance(source, dict), f'{where} must be an object')
        sid = slug(source.get('id'), f'{where}.id')
        required(sid not in ids, f'{where}.id repeats an earlier source id')
        ids.add(sid)
        required(isinstance(source.get('sha256'), str) and re.fullmatch(r'[0-9a-f]{64}', source['sha256']),
                 f'{where}.sha256 must be 64 lowercase hex characters')
        required(type(source.get('size_bytes')) is int and source['size_bytes'] >= 0,
                 f'{where}.size_bytes must be a non-negative integer')
    findings = set()
    unknown = False
    for i, finding in enumerate(report['findings']):
        where = f'findings[{i}]'
        required(isinstance(finding, dict), f'{where} must be an object')
        fid = slug(finding.get('id'), f'{where}.id (finding id)')
        required(fid not in findings, f'{where}.id repeats an earlier finding id')
        findings.add(fid)
        kind = finding.get('kind')
        required(kind in KINDS, f'{where}.kind must be one of ' + ', '.join(sorted(KINDS)))
        required(nonempty(finding.get('text')), f'{where}.text must be a nonempty string')
        required(isinstance(finding.get('citations'), list), f'{where}.citations must be a list')
        for j, citation in enumerate(finding['citations']):
            required(isinstance(citation, dict) and citation.get('source_id') in ids and nonempty(citation.get('locator')),
                     f'{where}.citations[{j}] must be an object whose source_id is listed in sources '
                     'and whose locator is a nonempty string')
        if kind == 'DOCUMENT_FACT':
            required(bool(finding['citations']), f'{where}: a DOCUMENT_FACT finding requires at least one citation')
        if kind == 'CALCULATION':
            w = finding.get('workpaper')
            required(isinstance(w, dict) and nonempty(w.get('method')) and isinstance(w.get('inputs'), (list, dict)) and bool(w['inputs']) and w.get('result') is not None,
                     f'{where}: a CALCULATION finding requires a workpaper with a method, nonempty inputs and a non-null result; use UNKNOWN when unavailable')
        if kind == 'EXTERNAL_EVIDENCE':
            e = finding.get('external_source')
            required(isinstance(e, dict) and all(nonempty(e.get(k)) for k in ('url', 'retrieved_at', 'scope')),
                     f'{where}: EXTERNAL_EVIDENCE requires external_source with url, retrieved_at and scope')
            required(e['url'].startswith(('https://', 'http://')), f'{where}.external_source.url must be an HTTP(S) URL')
            try:
                datetime.fromisoformat(e['retrieved_at'].replace('Z', '+00:00'))
            except ValueError:
                raise ReportInputError(f'{where}.external_source.retrieved_at must be an ISO 8601 timestamp') from None
        if kind == 'UNKNOWN':
            unknown = True
            required('result' not in finding, f'{where}: an UNKNOWN finding cannot carry a result')
    required(not (report['status'] == 'READY_FOR_REVIEW' and (unknown or report['checks_not_performed'])),
             'status READY_FOR_REVIEW is not allowed with UNKNOWN findings or checks_not_performed; use PARTIAL')
    if 'human_decision' in report:
        decision = report['human_decision']
        required(isinstance(decision, dict) and all(nonempty(decision.get(k)) for k in ('author', 'recorded_at', 'decision', 'evidence')),
                 'human_decision requires author, recorded_at, decision and evidence')
    # Reject nested NaN/Infinity even when called directly rather than through load().
    try:
        json.dumps(report, allow_nan=False)
    except ValueError:
        raise ReportInputError('Report contains a non-finite number (NaN or Infinity)') from None
    except TypeError:
        raise ReportInputError('Report contains a value that is not plain JSON') from None
    return report


def write_report(run, folder, filename, report, markdown):
    validate(report)
    run = no_symlinks(run)
    manifest = load(no_symlinks(run / 'run.json'))
    required(manifest.get('schema_version') == VERSION and manifest.get('run_id') == run.name, 'Invalid run manifest')
    required(report['sources'] == manifest['sources'], 'Report sources differ from run manifest')
    for source in manifest['sources']:
        retained = no_symlinks(run / 'sources' / source['id'])
        required(retained.is_file(), 'Retained source is unavailable')
        required(retained.stat().st_size == source['size_bytes'] and digest(retained) == source['sha256'],
                 'Retained source differs from run manifest')
    required(folder in FOLDERS, 'Unknown output folder')
    valid_filename(filename)
    required(nonempty(markdown), 'Empty Markdown')
    parent = no_symlinks(run / folder)
    parent.mkdir(mode=0o700, exist_ok=True)
    destination = no_symlinks(parent / report['report_id'])
    destination.mkdir(mode=0o700)  # exclusive allocation: no retry overwrites
    try:
        output = destination / filename
        with output.open('x', encoding='utf-8') as f:
            os.chmod(output, 0o600)
            f.write(markdown)
        saved = dict(report, markdown_sha256=digest(output), run_id=run.name)
        private_json(destination / (filename + '.json'), saved)
    except Exception:
        shutil.rmtree(destination)  # only the newly created, validated report directory
        raise
    return output


def write_companion(report_path, spec_path, fmt):
    """Write a spreadsheet of the report's tables beside an already written report.

    The Markdown stays the record: the companion is refused unless the report
    and its sidecar are intact, and it gets its own sidecar tying it to them.
    With spec_path None the sheets are built from the report's own tables.
    A spec that names a report (provenance report_sha256, as fund_kyc.py
    xlsx-spec --report writes) must name this exact report revision; a KYC
    helper spec must name one. A revised report therefore needs a new spec.
    """
    required(fmt in {'xlsx', 'csv'}, 'Unknown companion format')
    report_path = no_symlinks(report_path)
    valid_filename(report_path.name)
    required(report_path.is_file(), 'Report must already exist')
    sidecar = load(no_symlinks(report_path.parent / (report_path.name + '.json')))
    required(sidecar.get('markdown_sha256') == digest(report_path), 'Report differs from its sidecar')
    required(nonempty(sidecar.get('run_id')), 'Report sidecar has no run')
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import fund_xlsx
    output = report_path.with_suffix('.' + fmt)
    if spec_path is None:
        source = {'source': 'report tables'}
        fund_xlsx.build(report_path, output, fmt, from_markdown=True)
    else:
        spec_path = no_symlinks(spec_path)
        provenance = fund_xlsx.load_spec(spec_path).get('provenance')
        provenance = provenance if isinstance(provenance, dict) else {}
        bound = provenance.get('report_sha256')
        required(bound is not None or provenance.get('helper') != 'fund_kyc.py',
                 'KYC spec is not bound to a report; rebuild it with fund_kyc.py xlsx-spec --report')
        if bound is not None:
            required(bound == sidecar['markdown_sha256'] and provenance.get('report_filename') == report_path.name,
                     'Spec was built from a different report or revision; rebuild it from this report')
        else:
            print('WARNING: the spec is not bound to a report; confirm it was built from this report revision',
                  file=sys.stderr)
        source = {'source': 'spec', 'spec_sha256': digest(spec_path), 'spec_bound_to_report': bound is not None}
        fund_xlsx.build(spec_path, output, fmt)
    try:
        private_json(output.parent / (output.name + '.json'), {
            'schema_version': VERSION, 'run_id': sidecar['run_id'], 'report_id': sidecar.get('report_id'),
            'report_filename': report_path.name, 'markdown_sha256': sidecar['markdown_sha256'],
            'format': fmt, 'companion_sha256': digest(output), **source, 'human_review_required': True})
    except Exception:
        output.unlink()  # the companion was created by this call
        raise
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    commands = p.add_subparsers(dest='command', required=True)
    name = commands.add_parser('slug', help='Derive a safe fund label without creating files')
    name.add_argument('--name', required=True)
    filename = commands.add_parser('filename', help='Derive a safe Markdown basename without creating files')
    filename.add_argument('--family', required=True)
    filename.add_argument('--fund-name', required=True)
    filename.add_argument('--date', required=True)
    filename.add_argument('--qualifier', action='append', default=[])
    new = commands.add_parser('new-run')
    new.add_argument('--root', required=True)
    fund = new.add_mutually_exclusive_group(required=True)
    fund.add_argument('--fund', help='An already validated safe fund slug')
    fund.add_argument('--fund-name', help='Full legal name to derive a safe fund slug')
    new.add_argument('--input', action='append', default=[])
    check = commands.add_parser('validate')
    check.add_argument('report')
    write = commands.add_parser('write-report')
    for field in ('run', 'folder', 'filename', 'report', 'markdown'):
        write.add_argument('--' + field, required=True)
    companion = commands.add_parser('companion', help='Write an .xlsx or .csv of a written report\'s tables beside it')
    companion.add_argument('--report', required=True, help='The Markdown report written by write-report')
    source = companion.add_mutually_exclusive_group(required=True)
    source.add_argument('--spec', help='Table spec JSON (see docs/production/xlsx.md)')
    source.add_argument('--from-report', action='store_true', help="Use the report's own Markdown tables")
    companion.add_argument('--format', choices=['xlsx', 'csv'], default='xlsx')
    args = p.parse_args()
    try:
        if args.command == 'slug':
            print(safe_slug(args.name))
        elif args.command == 'filename':
            print(report_filename(args.family, args.fund_name, args.date, args.qualifier))
        elif args.command == 'new-run':
            print(create_run(args.root, safe_slug(args.fund_name) if args.fund_name is not None else args.fund, args.input))
        elif args.command == 'validate':
            validate(load(args.report))
            print('VALID: structure only; factual and professional review still required')
        elif args.command == 'companion':
            try:
                print(write_companion(args.report, args.spec, args.format))
            except RuntimeError as exc:  # openpyxl missing: say so, the skill falls back to CSV
                print(f'ERROR: {exc}', file=sys.stderr)
                return 3
        else:
            print(write_report(args.run, args.folder, args.filename, load(args.report), Path(args.markdown).read_text(encoding='utf-8')))
    except ReportInputError as exc:
        # Authored rule text only (see ReportInputError): names the field, never a value.
        print(f'ERROR: {exc}; no report approved', file=sys.stderr)
        return 2
    except FileExistsError:
        print('ERROR: output already exists and is never overwritten; no report approved', file=sys.stderr)
        return 2
    except (ValueError, OSError, TypeError, KeyError):
        # CLI errors must not leak file contents or personal identifiers.
        print('ERROR: invalid input, unsafe path, existing output or unavailable file; no report approved', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
