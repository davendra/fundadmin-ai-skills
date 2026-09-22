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
MAX_FILENAME = 180
SLUG_HASH_LENGTH = 12


def required(ok, message):
    if not ok:
        raise ValueError(message)


def slug(value):
    required(isinstance(value, str) and re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}', value), 'Invalid safe identifier')
    return value


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
    date.fromisoformat(report_date)
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
        raise ValueError('Non-finite JSON number')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            required(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), parse_constant=reject_constant, object_pairs_hook=unique)


def create_run(root, fund, inputs):
    root = no_symlinks(root)
    required(root.is_dir(), 'Output root must already exist')
    slug(fund)
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
    required(isinstance(report, dict), 'Report must be an object')
    required(report.get('schema_version') == VERSION, 'Unsupported report schema')
    slug(report.get('report_id'))
    required(nonempty(report.get('skill')) and report['skill'].startswith('fund'), 'Missing skill')
    required(report.get('status') in {'DRAFT', 'PARTIAL', 'BLOCKED', 'READY_FOR_REVIEW'}, 'Invalid report status')
    required(report.get('human_review_required') is True, 'Human review must remain required')
    for key in ('sources', 'findings', 'assumptions', 'limitations', 'checks_not_performed'):
        required(isinstance(report.get(key), list), f'{key} must be a list')
    for key in ('assumptions', 'limitations', 'checks_not_performed'):
        required(all(nonempty(v) for v in report[key]), f'{key} entries must be nonempty strings')
    ids = set()
    for source in report['sources']:
        required(isinstance(source, dict), 'Invalid source')
        sid = slug(source.get('id'))
        required(sid not in ids, 'Duplicate source ID')
        ids.add(sid)
        required(isinstance(source.get('sha256'), str) and re.fullmatch(r'[0-9a-f]{64}', source['sha256']), 'Invalid source hash')
        required(type(source.get('size_bytes')) is int and source['size_bytes'] >= 0, 'Invalid source size')
    findings = set()
    unknown = False
    for finding in report['findings']:
        required(isinstance(finding, dict), 'Finding must be an object')
        fid = slug(finding.get('id'))
        required(fid not in findings, 'Duplicate finding ID')
        findings.add(fid)
        kind = finding.get('kind')
        required(kind in KINDS and nonempty(finding.get('text')), 'Invalid finding kind/text')
        required(isinstance(finding.get('citations'), list), 'Citations must be a list')
        for citation in finding['citations']:
            required(isinstance(citation, dict) and citation.get('source_id') in ids and nonempty(citation.get('locator')), 'Unresolved citation')
        if kind == 'DOCUMENT_FACT':
            required(bool(finding['citations']), 'Document fact requires source citation')
        if kind == 'CALCULATION':
            w = finding.get('workpaper')
            required(isinstance(w, dict) and nonempty(w.get('method')) and isinstance(w.get('inputs'), (list, dict)) and bool(w['inputs']) and w.get('result') is not None, 'Calculation requires inputs and a non-null result; use UNKNOWN when unavailable')
        if kind == 'EXTERNAL_EVIDENCE':
            e = finding.get('external_source')
            required(isinstance(e, dict) and all(nonempty(e.get(k)) for k in ('url', 'retrieved_at', 'scope')), 'External evidence requires provenance')
            required(e['url'].startswith(('https://', 'http://')), 'External source must be an HTTP(S) URL')
            try:
                datetime.fromisoformat(e['retrieved_at'].replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Invalid external evidence timestamp') from None
        if kind == 'UNKNOWN':
            unknown = True
            required('result' not in finding, 'Unknown cannot carry a definitive result')
    required(not (report['status'] == 'READY_FOR_REVIEW' and (unknown or report['checks_not_performed'])), 'Incomplete evidence cannot be ready for review')
    if 'human_decision' in report:
        decision = report['human_decision']
        required(isinstance(decision, dict) and all(nonempty(decision.get(k)) for k in ('author', 'recorded_at', 'decision', 'evidence')), 'Human decision requires attribution')
    # Reject nested NaN/Infinity even when called directly rather than through load().
    json.dumps(report, allow_nan=False)
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
        else:
            print(write_report(args.run, args.folder, args.filename, load(args.report), Path(args.markdown).read_text(encoding='utf-8')))
    except (ValueError, OSError, TypeError, KeyError):
        # CLI errors must not leak file contents or personal identifiers.
        print('ERROR: invalid input, unsafe path, existing output or unavailable file; no report approved', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
