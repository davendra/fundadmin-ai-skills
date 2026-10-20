#!/usr/bin/env python3
"""Read-only Markdown/PDF fidelity check for FundAdmin reports; requires pypdf.

Exit 0: supported text matched; 1: mismatch; 2: input/dependency/format error.
This checks content, not factual accuracy, visual layout or accessibility.
"""
import argparse
from bisect import bisect_right
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

SYMBOLS = {'🔴': 'HIGH', '🟠': 'ELEVATED', '🟡': 'MEDIUM', '🟢': 'LOW',
           '⬜': '[ ]', '☐': '[ ]', '☑': '[x]', '✅': '[x]', '❌': '[no]',
           '⚠': 'WARNING', '→': '->'}
RULE = re.compile(r'^ {0,3}([-*_])(?:[ \t]*\1){2,}[ \t]*$')
FOOTER = re.compile(r'(?:AI Fund Administration Assistant|CONFIDENTIAL|Page \d+ of \d+)')


def compact(text):
    """Ignore layout whitespace only: preserve case, signs, decimals and operators."""
    return re.sub(r'\s+', '', unicodedata.normalize('NFC', text))


def inline(text):
    # This intentionally does not import or execute the renderer being checked.
    codes = []
    def code(match):
        codes.append(match.group(1))
        return '\x00%d\x00' % (len(codes) - 1)
    text = re.sub(r'`([^`]+)`', code, text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', r'\1 (\2)', text)
    text = re.sub(r'\*\*(?=\S)(.+?)(?<=\S)\*\*', r'\1', text)
    text = re.sub(r'(?<![\w*])\*(?=\S)([^*]+?)(?<=\S)\*(?![\w*])', r'\1', text)
    text = re.sub(r'\x00(\d+)\x00', lambda m: codes[int(m.group(1))], text)
    for symbol, replacement in SYMBOLS.items():
        text = text.replace(symbol, replacement)
    return text


def cells(line):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|') and not line.endswith(r'\|'):
        line = line[:-1]
    return [c.strip().replace(r'\|', '|') for c in re.split(r'(?<!\\)\|', line)]


def markdown_blocks(markdown):
    """Parse the renderer's documented Markdown subset into source-linked units."""
    lines = markdown.splitlines()
    blocks, i, fence = [], 0, None
    while i < len(lines):
        line, number = lines[i], i + 1
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            fence = None if fence == marker[1][0] else marker[1][0]
            blocks.append({'kind': 'text', 'line': number, 'text': line})
            i += 1
            continue
        if not fence and RULE.fullmatch(line):
            i += 1
            continue
        if not fence and i + 1 < len(lines) and '|' in line and '|' in lines[i + 1]:
            headers, separators = cells(line), cells(lines[i + 1])
            if len(headers) == len(separators) and all(re.fullmatch(r':?-{3,}:?', s) for s in separators):
                rows, i = [], i + 2
                while i < len(lines) and '|' in lines[i] and lines[i].strip():
                    row = cells(lines[i])
                    if len(row) != len(headers):
                        break
                    rows.append({'line': i + 1, 'cells': row})
                    i += 1
                if len(headers) > 5 or any(len(c) > 1200 for r in rows for c in r['cells']):
                    for row in rows or [{'line': number, 'cells': [''] * len(headers)}]:
                        for h, c in zip(headers, row['cells']):
                            blocks.append({'kind': 'text', 'line': row['line'], 'text': inline(h) + ': ' + inline(c)})
                else:
                    blocks.append({'kind': 'table', 'line': number, 'headers': list(map(inline, headers)),
                                   'rows': [{'line': r['line'], 'cells': list(map(inline, r['cells']))} for r in rows]})
                continue
        if line.strip():
            if fence:
                text = line
            else:
                text = re.sub(r'^(#{1,6})\s+|^\s*>\s?', '', line)
                # Bullet markers are layout; checkbox contents remain an assessed unit.
                text = re.sub(r'^\s*[-*+]\s+', '', text)
                text = inline(text)
            blocks.append({'kind': 'text', 'line': number, 'text': text})
        i += 1
    if not blocks:
        raise ValueError('Markdown contains no assessable content')
    return blocks


def extract_pdf(path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ValueError('pypdf is required for fidelity checks') from exc
    reader = PdfReader(path)
    if reader.is_encrypted:
        raise ValueError('Encrypted PDF is not supported')
    spans, removed = [], []
    for page_number, page in enumerate(reader.pages, 1):
        if int(page.get('/Rotate', 0)) % 360:
            raise ValueError('Rotated pages require a separate layout-aware review')
        def visit(text, cm, tm, font, size):
            if not text.strip():
                return
            x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
            y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            entry = {'text': text, 'x': round(x, 3), 'y': round(y, 3), 'page': page_number}
            # Only the known generated footer in its footer region may be ignored.
            if 0 <= y < 40 and size <= 8 and FOOTER.fullmatch(text.strip()):
                removed.append(entry)
            else:
                spans.append(entry)
        page.extract_text(visitor_text=visit)
    if not spans:
        raise ValueError('PDF has no extractable text; OCR/visual review required')
    return spans, len(reader.pages), removed


def check_blocks(blocks, spans):
    """Match prose in order and table cells within their own row and column.

    PDF draw order interleaves other columns between split-cell fragments.
    Column position and consecutive first-column anchors bound each row instead
    of accepting an arbitrary subsequence or any matching text elsewhere.
    """
    chunks = [compact(s['text']) for s in spans]
    offsets, position = [], 0
    for chunk in chunks:
        offsets.append(position)
        position += len(chunk)
    full = ''.join(chunks)
    def span_at(offset):
        return min(len(spans) - 1, bisect_right(offsets, offset) - 1)
    def joined(indices):
        text, mapping = '', []
        for j in indices:
            text += chunks[j]
            mapping.extend([j] * len(chunks[j]))
        return text, mapping
    results, cursor = [], 0
    def record(line, expected, matched, indices=(), **extra):
        results.append(dict(line=line, expected=expected, matched=matched,
                            pages=sorted({spans[j]['page'] for j in indices}), **extra))
    for bindex, block in enumerate(blocks):
        if block['kind'] == 'text':
            expected = compact(block['text'])
            hit = full.find(expected, cursor)
            ok = hit >= 0
            indices = range(span_at(hit), span_at(hit + len(expected) - 1) + 1) if ok else []
            record(block['line'], block['text'], ok, indices, kind='text')
            if ok:
                cursor = hit + len(expected)
            continue
        headers = block['headers']
        if any(not compact(header) for header in headers):
            raise ValueError('Table headers must contain text to establish column positions')
        signature = ''.join(map(compact, headers))
        start = full.find(signature, cursor)
        if start < 0:
            record(block['line'], ' | '.join(headers), False, kind='table-header', reason='Header not found in source order')
            for row in block['rows']:
                for col, value in enumerate(row['cells']):
                    record(row['line'], value, False, kind='cell', column=col + 1, reason='Table header unavailable')
            continue
        lefts, header_offset = [], start
        for header in headers:
            j = span_at(header_offset)
            lefts.append(spans[j]['x'])
            record(block['line'], header, True, [j], kind='table-header')
            header_offset += len(compact(header))
        if any(b <= a for a, b in zip(lefts, lefts[1:])):
            record(block['line'], ' | '.join(headers), False, kind='table-layout', reason='Cannot establish column positions')
            continue
        end = len(full)
        if bindex + 1 < len(blocks):
            following = blocks[bindex + 1]
            anchor = compact(following['text']) if following['kind'] == 'text' else ''.join(map(compact, following['headers']))
            hit = full.find(anchor, header_offset)
            if hit >= 0:
                end = hit
        candidates = [j for j in range(span_at(start), len(spans)) if offsets[j] < end]
        ignored, search = set(), start
        while True:
            hit = full.find(signature, search, end)
            if hit < 0:
                break
            ids = list(range(span_at(hit), span_at(hit + len(signature) - 1) + 1))
            # Require a complete physical header row, not a scattered word match.
            offset, positioned = hit, True
            for left, header in zip(lefts, headers):
                positioned = positioned and abs(spans[span_at(offset)]['x'] - left) <= .5
                offset += len(compact(header))
            if positioned and len({spans[j]['page'] for j in ids}) == 1:
                ignored.update(ids)
            search = hit + len(signature)
        def column(j):
            if spans[j]['x'] < lefts[0] - .5:
                return -1
            return bisect_right([x - .5 for x in lefts], spans[j]['x']) - 1
        first, first_map = joined(j for j in candidates if j not in ignored and column(j) == 0)
        anchors, at = [], 0
        for row in block['rows']:
            value = compact(row['cells'][0])
            hit = first.find(value, at) if value else -1
            if hit < 0:
                anchors.append(None)
            else:
                anchors.append(first_map[hit])
                at = hit + len(value)
        for ri, row in enumerate(block['rows']):
            lo = anchors[ri]
            hi = next((a for a in anchors[ri + 1:] if a is not None), len(spans))
            for col, value in enumerate(row['cells']):
                ids = [j for j in candidates if lo is not None and lo <= j < hi and j not in ignored and column(j) == col]
                actual, _ = joined(ids)
                record(row['line'], value, lo is not None and actual == compact(value), ids,
                       kind='cell', column=col + 1, actual=actual,
                       continuation=len({spans[j]['page'] for j in ids}) > 1)
        cursor = end
    return results


def check_fidelity(markdown_path, pdf_path):
    """Check supplied files without modifying them; include hashes for audit."""
    markdown_path, pdf_path = Path(markdown_path), Path(pdf_path)
    if markdown_path.resolve() == pdf_path.resolve():
        raise ValueError('Markdown and PDF must be different files')
    markdown = markdown_path.read_text(encoding='utf-8')
    blocks = markdown_blocks(markdown)
    spans, count, footers = extract_pdf(pdf_path)
    units = check_blocks(blocks, spans)
    matched = sum(u['matched'] for u in units)
    return {'schema_version': '1.0', 'status': 'matched' if matched == len(units) else 'mismatch',
            'source_sha256': hashlib.sha256(markdown_path.read_bytes()).hexdigest(),
            'pdf_sha256': hashlib.sha256(pdf_path.read_bytes()).hexdigest(), 'pdf_pages': count,
            'assessed_units': len(units), 'matched_units': matched,
            'mismatches': [u for u in units if not u['matched']],
            'table_continuations': [u for u in units if u.get('continuation')],
            'ignored_footer_spans': len(footers),
            'limitations': ['Text fidelity only; no factual, visual-layout or accessibility certification.',
                            'Whitespace is normalised; case, punctuation, signs, decimal points and operators are preserved.',
                            'Supports the FundAdmin Markdown renderer and ordinary horizontal text; unsupported glyphs/layouts may need manual review.',
                            'Checks source content and table-row association, not arbitrary extra PDF prose.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--markdown', required=True)
    parser.add_argument('--pdf', required=True)
    args = parser.parse_args(argv)
    try:
        result = check_fidelity(args.markdown, args.pdf)
    except Exception as exc:
        # A broken/missing PDF or dependency must never look like a successful check.
        print(json.dumps({'status': 'error', 'error': str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return 0 if result['status'] == 'matched' else 1


if __name__ == '__main__':
    sys.exit(main())
