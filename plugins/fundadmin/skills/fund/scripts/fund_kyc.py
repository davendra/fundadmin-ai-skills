#!/usr/bin/env python3
"""Score and route a KYC record against the firm's rules grid. Decides nothing.

The model reads the onboarding documents and writes a structured record (see
fund/references/kyc-record-schema.md). This helper checks that record, applies
the firm's rules grid and any supplied screening evidence, and returns a risk
rating, a document matrix, one outcome per rule and a routing disposition:

    ESCALATE FOR EDD | REQUEST DOCUMENTS | HOLD | PRELIMINARY READY FOR HUMAN REVIEW

A disposition routes work to a person. It is never an admission, a rejection,
sanctions clearance or a compliance determination. No network access.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fund_screening  # noqa: E402  (same directory, shipped together)

VERSION = 1
APPLICANT_TYPES = {'individual', 'corporate', 'partnership', 'trust', 'fund', 'pension',
                   'foundation_endowment', 'sovereign', 'nominee_intermediary', 'other'}
RISK_LEVELS = ('low', 'medium', 'high')
FUNDS_STATUS = {'documented', 'asserted', 'not_stated'}
PEP_DECLARED = {'yes', 'no', 'not_stated'}
DOC_STATUS = {'received', 'incomplete'}
ON_TRIGGER = {'request-docs', 'escalate-edd', 'hold'}
DISPOSITIONS = ('ESCALATE FOR EDD', 'REQUEST DOCUMENTS', 'HOLD', 'PRELIMINARY READY FOR HUMAN REVIEW')
READINESS = {'ESCALATE FOR EDD': 'ESCALATE', 'PRELIMINARY READY FOR HUMAN REVIEW': 'PRELIMINARY READY FOR HUMAN REVIEW'}
LIMITATIONS = [
    'RECORD EXTRACTED FROM UNTRUSTED DOCUMENTS; EXTRACTION NOT VERIFIED',
    'NO LIVE SCREENING PERFORMED BY THIS HELPER',
    'RULES ARE THE CALLER-SUPPLIED GRID, NOT A LEGAL STANDARD',
    'ROUTING ONLY: NOT AN ADMISSION, REJECTION, CLEARANCE OR COMPLIANCE DETERMINATION',
]
REF = re.compile(r'[a-z0-9][a-z0-9-]{0,63}')
SLUG = re.compile(r'[a-z][a-z0-9_]{0,63}')


def required(ok, code):
    if not ok:
        raise ValueError(code)


def text(value, limit=300):
    return isinstance(value, str) and bool(value.strip()) and len(value) <= limit


def iso(value, code):
    required(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), code)
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(code) from None


def optional_date(value, code):
    return None if value is None else iso(value, code)


def jurisdiction(value):
    return isinstance(value, str) and (value == 'UNKNOWN' or re.fullmatch(r'[A-Z]{2}', value))


# ---------------------------------------------------------------- loading

def _unique(pairs):
    result = {}
    for key, value in pairs:
        required(key not in result, 'DUPLICATE_KEY')
        result[key] = value
    return result


def _finite(value):
    if isinstance(value, float):
        required(math.isfinite(value), 'NONFINITE_NUMBER')
    elif isinstance(value, dict):
        for child in value.values():
            _finite(child)
    elif isinstance(value, list):
        for child in value:
            _finite(child)
    return value


def load_json(path):
    def reject(_):
        raise ValueError('NONFINITE_NUMBER')
    return _finite(json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=_unique, parse_constant=reject))


def load_grid_file(path):
    path = Path(path)
    if path.suffix.lower() == '.json':
        return load_json(path)
    try:
        import yaml
    except ImportError:
        raise ValueError('YAML_UNAVAILABLE_SUPPLY_JSON') from None

    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
        required(len(keys) == len(set(map(str, keys))), 'DUPLICATE_KEY')
        return loader.construct_mapping(node, deep)

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    return _finite(yaml.load(path.read_text(encoding='utf-8'), Loader=UniqueLoader))


# ---------------------------------------------------------------- record

def validate_record(record):
    """Structural check of the reader's output. Returns the record unchanged."""
    required(isinstance(record, dict), 'RECORD_NOT_OBJECT')
    allowed = {'schema_version', 'subject_ref', 'applicant_type', 'as_of', 'identity', 'beneficial_owners',
               'controllers', 'pep', 'source_of_funds', 'source_of_wealth', 'documents', 'tax_forms',
               'last_completed_review', 'injection_suspected', 'unreadable'}
    required(set(record) <= allowed, 'UNKNOWN_RECORD_FIELD')
    required(record.get('schema_version') == VERSION and type(record['schema_version']) is int, 'UNSUPPORTED_SCHEMA')
    required(isinstance(record.get('subject_ref'), str) and REF.fullmatch(record['subject_ref']), 'INVALID_SUBJECT_REF')
    required(record.get('applicant_type') in APPLICANT_TYPES, 'INVALID_APPLICANT_TYPE')
    iso(record.get('as_of'), 'INVALID_AS_OF')
    optional_date(record.get('last_completed_review'), 'INVALID_LAST_REVIEW')

    identity = record.get('identity')
    required(isinstance(identity, dict) and set(identity) <= {'legal_name_present', 'registration_or_id_present', 'jurisdiction', 'source'}, 'INVALID_IDENTITY')
    required(isinstance(identity.get('legal_name_present'), bool) and isinstance(identity.get('registration_or_id_present'), bool), 'INVALID_IDENTITY')
    required(jurisdiction(identity.get('jurisdiction')) and text(identity.get('source')), 'INVALID_IDENTITY')

    owners = record.get('beneficial_owners')
    required(isinstance(owners, list) and len(owners) <= 200, 'INVALID_OWNERS')
    refs = set()
    for owner in owners:
        required(isinstance(owner, dict) and set(owner) <= {'ref', 'ownership_pct', 'chain_depth', 'jurisdiction', 'is_natural_person', 'source'}, 'INVALID_OWNER')
        required(isinstance(owner.get('ref'), str) and REF.fullmatch(owner['ref']) and owner['ref'] not in refs, 'INVALID_OWNER_REF')
        refs.add(owner['ref'])
        pct = owner.get('ownership_pct')
        required(pct is None or (isinstance(pct, (int, float)) and not isinstance(pct, bool) and 0 <= pct <= 100), 'INVALID_OWNERSHIP_PCT')
        required(type(owner.get('chain_depth')) is int and 1 <= owner['chain_depth'] <= 20, 'INVALID_CHAIN_DEPTH')
        required(jurisdiction(owner.get('jurisdiction')) and isinstance(owner.get('is_natural_person'), bool) and text(owner.get('source')), 'INVALID_OWNER')

    controllers = record.get('controllers', [])
    required(isinstance(controllers, list) and all(isinstance(c, dict) and set(c) <= {'ref', 'role', 'source'} and isinstance(c.get('ref'), str) and REF.fullmatch(c['ref']) and text(c.get('role'), 80) and text(c.get('source')) for c in controllers), 'INVALID_CONTROLLERS')

    pep = record.get('pep')
    required(isinstance(pep, dict) and set(pep) <= {'declared', 'source'} and pep.get('declared') in PEP_DECLARED, 'INVALID_PEP')
    for field in ('source_of_funds', 'source_of_wealth'):
        value = record.get(field)
        required(isinstance(value, dict) and set(value) <= {'status', 'source'} and value.get('status') in FUNDS_STATUS, 'INVALID_' + field.upper())

    documents = record.get('documents')
    required(isinstance(documents, list) and len(documents) <= 500, 'INVALID_DOCUMENTS')
    for doc in documents:
        required(isinstance(doc, dict) and set(doc) <= {'type', 'status', 'issued', 'expires', 'source'}, 'INVALID_DOCUMENT')
        required(isinstance(doc.get('type'), str) and SLUG.fullmatch(doc['type']) and doc.get('status') in DOC_STATUS and text(doc.get('source')), 'INVALID_DOCUMENT')
        optional_date(doc.get('issued'), 'INVALID_DOCUMENT_DATE')
        optional_date(doc.get('expires'), 'INVALID_DOCUMENT_DATE')

    tax = record.get('tax_forms', [])
    required(isinstance(tax, list) and all(isinstance(t, dict) and set(t) <= {'form', 'status', 'signed', 'source'} and text(t.get('form'), 40) and t.get('status') in DOC_STATUS and optional_date(t.get('signed'), 'INVALID_TAX_FORM_DATE') is not False and text(t.get('source')) for t in tax), 'INVALID_TAX_FORMS')
    for field in ('injection_suspected', 'unreadable'):
        items = record.get(field, [])
        required(isinstance(items, list) and len(items) <= 50, 'INVALID_' + field.upper())
        for item in items:
            required(isinstance(item, dict) and set(item) <= {'source', 'summary'} and text(item.get('source')) and text(item.get('summary'), 300), 'INVALID_' + field.upper())
    return record


# ---------------------------------------------------------------- grid

CONDITIONS = {
    'document_missing': {'document'},
    'document_expired': {'document'},
    'pep_declared_in': {'values'},
    'funds_status_in': {'field', 'values'},
    'chain_depth_over': {'depth'},
    'no_natural_person_owner_at_threshold': set(),
    'unknown_ownership_pct': set(),
    'jurisdiction_in_list': {'list'},
    'applicant_type_in': {'values'},
    'no_controller_identified': set(),
}


def validate_condition(cond, grid):
    required(isinstance(cond, dict) and cond.get('type') in CONDITIONS, 'INVALID_CONDITION')
    required(set(cond) == {'type'} | CONDITIONS[cond['type']], 'INVALID_CONDITION_FIELDS')
    kind = cond['type']
    if kind in ('document_missing', 'document_expired'):
        required(isinstance(cond['document'], str) and SLUG.fullmatch(cond['document']), 'INVALID_CONDITION_DOCUMENT')
    if kind == 'pep_declared_in':
        required(isinstance(cond['values'], list) and cond['values'] and set(cond['values']) <= PEP_DECLARED, 'INVALID_CONDITION_VALUES')
    if kind == 'funds_status_in':
        required(cond['field'] in ('source_of_funds', 'source_of_wealth') and isinstance(cond['values'], list) and cond['values'] and set(cond['values']) <= FUNDS_STATUS, 'INVALID_CONDITION_VALUES')
    if kind == 'chain_depth_over':
        required(type(cond['depth']) is int and 1 <= cond['depth'] <= 20, 'INVALID_CONDITION_DEPTH')
    if kind == 'jurisdiction_in_list':
        required(cond['list'] in grid.get('jurisdiction_lists', {}), 'UNKNOWN_JURISDICTION_LIST')
    if kind == 'applicant_type_in':
        required(isinstance(cond['values'], list) and cond['values'] and set(cond['values']) <= APPLICANT_TYPES, 'INVALID_CONDITION_VALUES')


def validate_grid(grid):
    required(isinstance(grid, dict), 'GRID_NOT_OBJECT')
    allowed = {'schema_version', 'name', 'example', 'owner', 'effective_date', 'ubo_threshold_pct', 'expiry_warning_days',
               'jurisdiction_lists', 'risk_factors', 'risk_thresholds', 'required_documents', 'refresh_months', 'rules'}
    required(set(grid) <= allowed, 'UNKNOWN_GRID_FIELD')
    required(grid.get('schema_version') == VERSION and type(grid['schema_version']) is int, 'UNSUPPORTED_GRID_SCHEMA')
    required(text(grid.get('name'), 200) and isinstance(grid.get('example'), bool), 'GRID_NAME_AND_EXAMPLE_FLAG_REQUIRED')
    if not grid['example']:
        required(text(grid.get('owner'), 200), 'FIRM_GRID_NEEDS_OWNER')
        iso(grid.get('effective_date'), 'FIRM_GRID_NEEDS_EFFECTIVE_DATE')
    threshold = grid.get('ubo_threshold_pct')
    required(isinstance(threshold, (int, float)) and not isinstance(threshold, bool) and 0 < threshold <= 100, 'INVALID_UBO_THRESHOLD')
    required(type(grid.get('expiry_warning_days', 60)) is int and 0 <= grid.get('expiry_warning_days', 60) <= 3660, 'INVALID_EXPIRY_WARNING')
    lists = grid.get('jurisdiction_lists', {})
    required(isinstance(lists, dict) and all(SLUG.fullmatch(k) and isinstance(v, list) and all(isinstance(j, str) and re.fullmatch(r'[A-Z]{2}', j) for j in v) for k, v in lists.items()), 'INVALID_JURISDICTION_LISTS')

    ids = set()
    factors = grid.get('risk_factors')
    required(isinstance(factors, list) and factors, 'RISK_FACTORS_REQUIRED')
    for factor in factors:
        required(isinstance(factor, dict) and set(factor) <= {'id', 'text', 'when', 'points', 'forces_high'}, 'INVALID_RISK_FACTOR')
        required(text(factor.get('id'), 40) and factor['id'] not in ids and text(factor.get('text')), 'INVALID_RISK_FACTOR')
        ids.add(factor['id'])
        required(type(factor.get('points')) is int and 0 <= factor['points'] <= 100 and isinstance(factor.get('forces_high', False), bool), 'INVALID_RISK_FACTOR')
        validate_condition(factor.get('when'), grid)
    thresholds = grid.get('risk_thresholds')
    required(isinstance(thresholds, dict) and set(thresholds) == {'medium', 'high'} and all(type(v) is int for v in thresholds.values()) and 0 < thresholds['medium'] < thresholds['high'], 'INVALID_RISK_THRESHOLDS')

    docs = grid.get('required_documents')
    required(isinstance(docs, dict) and docs and set(docs) <= APPLICANT_TYPES | {'default'}, 'INVALID_REQUIRED_DOCUMENTS')
    for tiers in docs.values():
        required(isinstance(tiers, dict) and set(tiers) <= set(RISK_LEVELS) and 'low' in tiers, 'INVALID_REQUIRED_DOCUMENTS')
        required(all(isinstance(v, list) and all(isinstance(d, str) and SLUG.fullmatch(d) for d in v) for v in tiers.values()), 'INVALID_REQUIRED_DOCUMENTS')
    months = grid.get('refresh_months')
    required(isinstance(months, dict) and set(months) == set(RISK_LEVELS) and all(type(v) is int and 1 <= v <= 120 for v in months.values()), 'INVALID_REFRESH_MONTHS')

    rules = grid.get('rules')
    required(isinstance(rules, list) and rules, 'RULES_REQUIRED')
    for rule in rules:
        required(isinstance(rule, dict) and set(rule) <= {'id', 'text', 'applies_to', 'min_risk', 'when', 'on_trigger'}, 'INVALID_RULE')
        required(text(rule.get('id'), 40) and rule['id'] not in ids and text(rule.get('text'), 500), 'INVALID_RULE_ID')
        ids.add(rule['id'])
        applies = rule.get('applies_to', 'all')
        required(applies == 'all' or (isinstance(applies, list) and applies and set(applies) <= APPLICANT_TYPES), 'INVALID_RULE_SCOPE')
        required(rule.get('min_risk', 'low') in RISK_LEVELS and rule.get('on_trigger') in ON_TRIGGER, 'INVALID_RULE')
        validate_condition(rule.get('when'), grid)
    return grid


# ---------------------------------------------------------------- evaluation

def add_months(day, months):
    month = day.month - 1 + months
    year, month = day.year + month // 12, month % 12 + 1
    last = [31, 29 if year % 4 == 0 and (year % 100 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    return date(year, month, min(day.day, last))


def document_state(record, doc_type, as_of, warning_days):
    """RECEIVED / EXPIRING / EXPIRED / INCOMPLETE / MISSING for one document type."""
    matches = [d for d in record['documents'] if d['type'] == doc_type]
    if not matches:
        return 'MISSING', []
    states = []
    for doc in matches:
        expires = optional_date(doc.get('expires'), 'INVALID_DOCUMENT_DATE')
        if doc['status'] == 'incomplete':
            states.append('INCOMPLETE')
        elif expires is not None and expires < as_of:
            states.append('EXPIRED')
        elif expires is not None and (expires - as_of).days <= warning_days:
            states.append('EXPIRING')
        else:
            states.append('RECEIVED')
    best = next(s for s in ('RECEIVED', 'EXPIRING', 'INCOMPLETE', 'EXPIRED') if s in states)
    return best, [d['source'] for d in matches]


def condition_hit(cond, record, grid, as_of):
    """Return (triggered, evidence). triggered is True, False or None (cannot evaluate)."""
    kind = cond['type']
    owners = record['beneficial_owners']
    if kind == 'document_missing':
        state, sources = document_state(record, cond['document'], as_of, grid.get('expiry_warning_days', 60))
        return state in ('MISSING', 'INCOMPLETE'), f"{cond['document']}: {state}" + (f" ({'; '.join(sources)})" if sources else '')
    if kind == 'document_expired':
        state, sources = document_state(record, cond['document'], as_of, grid.get('expiry_warning_days', 60))
        return state == 'EXPIRED', f"{cond['document']}: {state}" + (f" ({'; '.join(sources)})" if sources else '')
    if kind == 'pep_declared_in':
        return record['pep']['declared'] in cond['values'], f"pep declared: {record['pep']['declared']}"
    if kind == 'funds_status_in':
        status = record[cond['field']]['status']
        return status in cond['values'], f"{cond['field']}: {status}"
    if kind == 'chain_depth_over':
        deepest = max((o['chain_depth'] for o in owners), default=0)
        return deepest > cond['depth'], f'deepest ownership chain: {deepest}'
    if kind == 'no_natural_person_owner_at_threshold':
        if record['applicant_type'] == 'individual':
            return False, 'individual applicant'
        threshold = grid['ubo_threshold_pct']
        found = [o for o in owners if o['is_natural_person'] and o['ownership_pct'] is not None and o['ownership_pct'] >= threshold]
        return not found, f'natural-person owners at or above {threshold}%: {len(found)}'
    if kind == 'unknown_ownership_pct':
        unknown = [o['ref'] for o in owners if o['ownership_pct'] is None]
        return bool(unknown), f"owners without a percentage: {', '.join(unknown) or 'none'}"
    if kind == 'jurisdiction_in_list':
        listed = set(grid['jurisdiction_lists'][cond['list']])
        seen = {record['identity']['jurisdiction']} | {o['jurisdiction'] for o in owners}
        hits = sorted(seen & listed)
        if 'UNKNOWN' in seen and not hits:
            return None, 'a jurisdiction is UNKNOWN'
        return bool(hits), f"jurisdictions on {cond['list']}: {', '.join(hits) or 'none'}"
    if kind == 'applicant_type_in':
        return record['applicant_type'] in cond['values'], f"applicant type: {record['applicant_type']}"
    if kind == 'no_controller_identified':
        if record['applicant_type'] == 'individual':
            return False, 'individual applicant'
        return not record.get('controllers'), f"controllers identified: {len(record.get('controllers', []))}"
    raise ValueError('INVALID_CONDITION')


def evaluate(record, grid=None, screening=None):
    validate_record(record)
    as_of = iso(record['as_of'], 'INVALID_AS_OF')
    reasons = {'escalate': [], 'integrity': [], 'documents': [], 'hold': []}
    limitations = list(LIMITATIONS)

    for item in record.get('injection_suspected', []):
        reasons['integrity'].append(f"Instruction-like text in a source document was not followed ({item['source']})")
    for item in record.get('unreadable', []):
        reasons['integrity'].append(f"Source could not be read ({item['source']})")

    screen = None
    if screening is not None:
        screen = fund_screening.validate_evidence(screening)
        if screen['status'] == 'POTENTIAL MATCH':
            reasons['escalate'].append('Screening: POTENTIAL MATCH requires qualified human adjudication')
        elif screen['status'] != 'NO MATCH REPORTED':
            reasons['hold'].append(f"Screening: {screen['status']}")
    else:
        reasons['hold'].append('Screening: NOT PERFORMED (no screening evidence supplied)')

    result = {
        'schema_version': VERSION,
        'subject_ref': record['subject_ref'],
        'applicant_type': record['applicant_type'],
        'as_of': record['as_of'],
        'screening': {'status': screen['status'] if screen else 'NOT PERFORMED',
                      'checks': [{'check': c['check'], 'status': c['status'], 'issues': c['issues']} for c in screen['checks']] if screen else []},
    }

    if grid is None:
        reasons['integrity'].append('Rules grid not supplied: no rule was evaluated')
        result.update(grid={'name': None, 'example': None}, risk_rating='UNASSESSED', risk_factors=[], documents=[],
                      rule_outcomes=[], refresh_due=None)
    else:
        validate_grid(grid)
        if grid['example']:
            limitations.append('EXAMPLE RULES GRID: NOT FIRM POLICY')
            reasons['hold'].append("Rules grid is the shipped example, not the firm's own grid")
        warning = grid.get('expiry_warning_days', 60)

        factors, points, forced = [], 0, False
        for factor in grid['risk_factors']:
            hit, evidence = condition_hit(factor['when'], record, grid, as_of)
            outcome = 'NOT EVALUATED' if hit is None else 'PRESENT' if hit else 'ABSENT'
            if hit:
                points += factor['points']
                forced = forced or factor.get('forces_high', False)
            elif hit is None:
                reasons['hold'].append(f"Risk factor {factor['id']} could not be evaluated: {evidence}")
            factors.append({'id': factor['id'], 'text': factor['text'], 'outcome': outcome, 'points': factor['points'] if hit else 0, 'evidence': evidence})
        th = grid['risk_thresholds']
        rating = 'high' if forced or points >= th['high'] else 'medium' if points >= th['medium'] else 'low'
        if rating == 'high':
            reasons['escalate'].append(f'Risk rating high ({points} points' + (', forced by a factor' if forced else '') + ')')

        tiers = grid['required_documents'].get(record['applicant_type']) or grid['required_documents'].get('default')
        needed = []
        if tiers is None:
            reasons['hold'].append(f"Rules grid lists no required documents for applicant type {record['applicant_type']}")
        else:
            for level in RISK_LEVELS[:RISK_LEVELS.index(rating) + 1]:
                needed += [d for d in tiers.get(level, []) if d not in needed]
        documents = []
        for doc_type in needed:
            state, sources = document_state(record, doc_type, as_of, warning)
            documents.append({'document': doc_type, 'state': state, 'sources': sources})
            if state in ('MISSING', 'INCOMPLETE', 'EXPIRED'):
                reasons['documents'].append(f'{doc_type}: {state}')

        outcomes = []
        for rule in grid['rules']:
            scope = rule.get('applies_to', 'all')
            if scope != 'all' and record['applicant_type'] not in scope:
                outcomes.append({'rule_id': rule['id'], 'text': rule['text'], 'outcome': 'NOT APPLICABLE', 'on_trigger': rule['on_trigger'], 'evidence': 'applicant type out of scope'})
                continue
            if RISK_LEVELS.index(rating) < RISK_LEVELS.index(rule.get('min_risk', 'low')):
                outcomes.append({'rule_id': rule['id'], 'text': rule['text'], 'outcome': 'NOT APPLICABLE', 'on_trigger': rule['on_trigger'], 'evidence': f'applies from {rule["min_risk"]} risk'})
                continue
            hit, evidence = condition_hit(rule['when'], record, grid, as_of)
            outcome = 'NOT EVALUATED' if hit is None else 'TRIGGERED' if hit else 'NOT TRIGGERED'
            outcomes.append({'rule_id': rule['id'], 'text': rule['text'], 'outcome': outcome, 'on_trigger': rule['on_trigger'], 'evidence': evidence})
            if hit is None:
                reasons['hold'].append(f"Rule {rule['id']} could not be evaluated: {evidence}")
            elif hit:
                bucket = {'escalate-edd': 'escalate', 'request-docs': 'documents', 'hold': 'hold'}[rule['on_trigger']]
                reasons[bucket].append(f"Rule {rule['id']}: {evidence}")

        last = optional_date(record.get('last_completed_review'), 'INVALID_LAST_REVIEW')
        result.update(
            grid={'name': grid['name'], 'example': grid['example'], 'effective_date': grid.get('effective_date')},
            risk_rating=rating, risk_points=points, risk_factors=factors, documents=documents, rule_outcomes=outcomes,
            refresh_due=add_months(last, grid['refresh_months'][rating]).isoformat() if last else None,
        )

    if reasons['escalate']:
        disposition = 'ESCALATE FOR EDD'
    elif reasons['integrity']:
        disposition = 'HOLD'
    elif reasons['documents']:
        disposition = 'REQUEST DOCUMENTS'
    elif reasons['hold']:
        disposition = 'HOLD'
    else:
        disposition = 'PRELIMINARY READY FOR HUMAN REVIEW'
    result.update(
        disposition=disposition,
        operational_readiness=READINESS.get(disposition, 'HOLD'),
        reasons=[r for key in ('escalate', 'integrity', 'documents', 'hold') for r in reasons[key]],
        limitations=limitations,
        human_review_required=True,
    )
    return result


# ---------------------------------------------------------------- spreadsheet spec

def _col(key, label, kind='text'):
    return {'key': key, 'label': label, 'type': kind}


def xlsx_spec(evaluations, title=None):
    """Table spec for scripts/fund_xlsx.py: one investor in detail, or a tracker for several."""
    required(isinstance(evaluations, list) and evaluations, 'NO_EVALUATIONS')
    notes = ['Dispositions route work to a person; none is an admission, rejection or clearance.']
    if len(evaluations) == 1:
        e = evaluations[0]
        sheets = [
            {'name': 'Summary', 'columns': [_col('field', 'Field'), _col('value', 'Value')], 'rows': [
                {'field': 'Subject', 'value': e['subject_ref']}, {'field': 'Applicant type', 'value': e['applicant_type']},
                {'field': 'As of', 'value': e['as_of']}, {'field': 'Disposition', 'value': e['disposition']},
                {'field': 'Risk rating', 'value': e['risk_rating']}, {'field': 'Screening', 'value': e['screening']['status']},
                {'field': 'Rules grid', 'value': str(e['grid']['name'])}, {'field': 'Refresh due', 'value': e['refresh_due'] or 'UNKNOWN'},
            ], 'autofilter': False},
            {'name': 'Reasons', 'columns': [_col('reason', 'Reason')], 'rows': [{'reason': r} for r in e['reasons']]},
            {'name': 'Documents', 'columns': [_col('document', 'Document'), _col('state', 'State'), _col('sources', 'Sources')],
             'rows': [{'document': d['document'], 'state': d['state'], 'sources': '; '.join(d['sources'])} for d in e['documents']]},
            {'name': 'Rules', 'columns': [_col('rule_id', 'Rule'), _col('text', 'Rule text'), _col('outcome', 'Outcome'), _col('on_trigger', 'On trigger'), _col('evidence', 'Evidence')],
             'rows': [{k: o[k] for k in ('rule_id', 'text', 'outcome', 'on_trigger', 'evidence')} for o in e['rule_outcomes']]},
            {'name': 'Risk factors', 'columns': [_col('id', 'Factor'), _col('text', 'Description'), _col('outcome', 'Outcome'), _col('points', 'Points', 'integer'), _col('evidence', 'Evidence')],
             'rows': [{k: f[k] for k in ('id', 'text', 'outcome', 'points', 'evidence')} for f in e['risk_factors']]},
        ]
        title = title or f"KYC review — {e['subject_ref']} — {e['as_of']}"
    else:
        doc_types = sorted({d['document'] for e in evaluations for d in e['documents']})
        columns = [_col('subject', 'Subject'), _col('applicant_type', 'Type'), _col('disposition', 'Disposition'),
                   _col('risk', 'Risk'), _col('screening', 'Screening'), _col('refresh_due', 'Refresh due'), _col('open_items', 'Open items', 'integer')]
        doc_types = doc_types[:53]  # fund_xlsx allows 60 columns; 7 are fixed
        columns += [_col(f'doc_{i}', d.replace('_', ' ').capitalize()) for i, d in enumerate(doc_types)]
        rows = []
        for e in evaluations:
            states = {d['document']: d['state'] for d in e['documents']}
            row = {'subject': e['subject_ref'], 'applicant_type': e['applicant_type'], 'disposition': e['disposition'],
                   'risk': e['risk_rating'], 'screening': e['screening']['status'], 'refresh_due': e['refresh_due'] or 'UNKNOWN',
                   'open_items': len(e['reasons'])}
            row.update({f'doc_{i}': states.get(d, 'N/A') for i, d in enumerate(doc_types)})
            rows.append(row)
        outstanding = [{'subject': e['subject_ref'], 'reason': r} for e in evaluations for r in e['reasons']]
        sheets = [
            {'name': 'Investors', 'columns': columns, 'rows': rows},
            {'name': 'Open items', 'columns': [_col('subject', 'Subject'), _col('reason', 'Reason')], 'rows': outstanding},
        ]
        title = title or f'KYC tracker — {len(evaluations)} investors'
    return {'schema_version': '1', 'title': title[:200], 'sheets': sheets, 'notes': notes,
            'provenance': {'helper': 'fund_kyc.py', 'grid': str(evaluations[0]['grid']['name'])}}


# ---------------------------------------------------------------- CLI

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('validate-record', help='Check a reader record against the schema')
    check.add_argument('--record', required=True)
    grid_check = commands.add_parser('validate-grid', help='Check a rules grid')
    grid_check.add_argument('--grid', required=True)
    run = commands.add_parser('evaluate', help='Rate, check documents and rules, and route one record')
    run.add_argument('--record', required=True)
    run.add_argument('--grid', help='Firm rules grid (.yaml or .json). Without it nothing is evaluated and the result is HOLD')
    run.add_argument('--screening', help='Screening evidence, fund_screening.py version 1 input')
    spec = commands.add_parser('xlsx-spec', help='Table spec for fund_xlsx.py from one or more evaluate outputs')
    spec.add_argument('--evaluation', action='append', required=True)
    spec.add_argument('--title')
    args = parser.parse_args(argv)
    try:
        if args.command == 'validate-record':
            validate_record(load_json(args.record))
            print('VALID: structure only; the extraction itself still needs human review')
        elif args.command == 'validate-grid':
            grid = validate_grid(load_grid_file(args.grid))
            print('VALID' + (' (EXAMPLE GRID: NOT FIRM POLICY)' if grid['example'] else ''))
        elif args.command == 'evaluate':
            result = evaluate(load_json(args.record), load_grid_file(args.grid) if args.grid else None,
                              load_json(args.screening) if args.screening else None)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(xlsx_spec([load_json(p) for p in args.evaluation], args.title), indent=2, ensure_ascii=False))
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        # Fixed codes only: parser messages can echo personal data from the documents.
        code = str(exc) if isinstance(exc, ValueError) and re.fullmatch(r'[A-Z_]+', str(exc)) else type(exc).__name__.upper()
        print(json.dumps({'error': code, 'disposition': 'HOLD', 'operational_readiness': 'HOLD'}))
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
