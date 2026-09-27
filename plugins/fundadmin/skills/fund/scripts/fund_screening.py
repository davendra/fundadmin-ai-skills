#!/usr/bin/env python3
"""Validate supplied screening evidence. No network, name matching or clearance.

See docs/production/regulatory.md for the version 1 input contract. Dates and
freshness limits are caller-supplied; validation does not authenticate evidence.
Only generated references and fixed diagnostic codes leave this adapter.
"""

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timedelta, timezone


CHECKS = {"sanctions", "pep", "adverse_media"}
RESULTS = {"NO MATCH", "POTENTIAL MATCH", "CONFIRMED MATCH", "NOT PERFORMED", "INCOMPLETE"}
KEY_FIELDS = ("subject_ref", "check", "jurisdiction", "source")
REQUIRED_TEXT = ("provider", "source_version", "evidence_ref", "identity_fingerprint")
MAX_POLICY_DAYS = 3660
# Scope values that say the real value is missing. They are accepted as input so
# a file still validates, but a requirement built on them proves nothing: the
# check is INCOMPLETE, never NO MATCH REPORTED. Matched on word tokens, so
# "synthetic-list" or "EU" are unaffected.
PLACEHOLDER_WORDS = {"unknown", "placeholder", "unspecified", "tbd", "tbc", "todo", "unavailable",
                     "undefined", "redacted", "dummy"}
PLACEHOLDER_VALUES = {"na", "n a", "none", "null", "nil", "any", "all", "default", "x", "xx", "xxx",
                      "missing", "not applicable", "same"}
NEGATED_WORDS = {"supplied", "provided", "available", "specified", "known", "given", "stated",
                 "applicable", "set", "assessed"}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError("NONFINITE_JSON_NUMBER")


def _finite_tree(value):
    # Also reject exponent overflow (1e999), which parse_constant does not see,
    # and non-finite values passed directly by Python callers, even in extras.
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("NONFINITE_JSON_NUMBER")
    if isinstance(value, dict):
        for child in value.values():
            _finite_tree(child)
    elif isinstance(value, list):
        for child in value:
            _finite_tree(child)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _ref(value):
    """Do not echo identifiers, URLs, provider free text or personal data."""
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=True).encode("utf-8")
    return "ref-" + hashlib.sha256(encoded).hexdigest()[:16]


def _time(value):
    if not isinstance(value, str):
        raise ValueError("INVALID_TIMESTAMP")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("INVALID_TIMESTAMP") from None
    if result.tzinfo is None:
        raise ValueError("TIMEZONE_REQUIRED")
    return result.astimezone(timezone.utc)


def _placeholder(value):
    """True for text that stands in for a missing scope value (see PLACEHOLDER_WORDS)."""
    if not isinstance(value, str):
        return False
    words = [w for w in re.split(r"[^a-z0-9]+", value.lower()) if w]
    if not words or " ".join(words) in PLACEHOLDER_VALUES:
        return True
    if any(w in PLACEHOLDER_WORDS for w in words):
        return True
    return any(a in ("not", "no", "un") and b in NEGATED_WORDS for a, b in zip(words, words[1:]))


def _scope_issues(requirement):
    """Placeholder scope metadata is treated as missing, never as a satisfied requirement."""
    issues = []
    if any(_placeholder(requirement.get(field)) for field in ("subject_ref", "jurisdiction", "source")):
        issues.append("PLACEHOLDER_SCOPE")
    if _placeholder(requirement.get("identity_fingerprint")):
        issues.append("IDENTITY_LINK_NOT_ASSESSED")
    if any(requirement.get(field) == MAX_POLICY_DAYS for field in ("max_age_days", "max_source_age_days")):
        issues.append("FRESHNESS_NOT_ASSESSED")
    return issues


def _key(item):
    values = tuple(item.get(field) for field in KEY_FIELDS)
    if not all(_text(value) for value in values):
        return None
    return values


def _record_issues(record, requirement, as_of):
    issues = []
    if any(not _text(record.get(field)) for field in REQUIRED_TEXT):
        issues.append("MISSING_PROVENANCE")
    if record.get("identity_fingerprint") != requirement["identity_fingerprint"]:
        issues.append("IDENTITY_MISMATCH")
    if not isinstance(record.get("status"), str) or record["status"] not in RESULTS:
        issues.append("UNKNOWN_STATUS")
    if record.get("coverage_complete") is not True:
        issues.append("PARTIAL_COVERAGE")
    try:
        screened = _time(record.get("screened_at"))
        source_date = _time(record.get("source_as_of"))
        expires = _time(record.get("expires_at"))
        if not source_date <= screened <= as_of:
            issues.append("INVALID_DATE_ORDER")
        if expires < screened or expires <= as_of:
            issues.append("EXPIRED_EVIDENCE")
        if as_of - screened > timedelta(days=requirement["max_age_days"]):
            issues.append("STALE_SCREEN")
        if as_of - source_date > timedelta(days=requirement["max_source_age_days"]):
            issues.append("STALE_SOURCE")
    except ValueError:
        issues.append("INVALID_TIMESTAMP")
    return issues


def validate_evidence(payload):
    """Return a privacy-minimised operational assessment, never an admission decision.

    A requirement is one subject/check/jurisdiction/source combination. The caller
    must establish the complete required scope separately. Duplicates cannot erase
    a hit, stale records cannot clear it, and unrequested records are not ignored.
    """
    _finite_tree(payload)
    if not isinstance(payload, dict) or type(payload.get("schema_version")) is not int or payload["schema_version"] != 1:
        raise ValueError("UNSUPPORTED_SCHEMA")
    as_of = _time(payload.get("as_of"))
    requirements = payload.get("requirements")
    records = payload.get("records")
    if not isinstance(requirements, list) or not isinstance(records, list):
        raise ValueError("LISTS_REQUIRED")
    required = {}
    for item in requirements:
        if not isinstance(item, dict):
            raise ValueError("INVALID_REQUIREMENT")
        key = _key(item)
        if key is None or item["check"] not in CHECKS or not _text(item.get("identity_fingerprint")):
            raise ValueError("INVALID_REQUIREMENT")
        for field in ("max_age_days", "max_source_age_days"):
            if type(item.get(field)) is not int or not 0 <= item[field] <= MAX_POLICY_DAYS:
                raise ValueError("INVALID_FRESHNESS_POLICY")
        if key in required:
            raise ValueError("DUPLICATE_REQUIREMENT")
        required[key] = item

    grouped = {key: [] for key in required}
    issues = [] if required else ["EMPTY_SCOPE"]
    unmatched_hit = False
    for record in records:
        if not isinstance(record, dict):
            issues.append("MALFORMED_RECORD")
            continue
        key = _key(record)
        if key not in required:
            issues.append("UNEXPECTED_RECORD")
            if record.get("status") in ("POTENTIAL MATCH", "CONFIRMED MATCH"):
                unmatched_hit = True
            continue
        grouped[key].append(record)

    checks = []
    for key, requirement in required.items():
        supplied = grouped[key]
        check_issues = _scope_issues(requirement)
        statuses = []
        references = []
        for record in supplied:
            check_issues.extend(_record_issues(record, requirement, as_of))
            statuses.append(record.get("status"))
            if _text(record.get("evidence_ref")):
                references.append(_ref(record["evidence_ref"]))
        if len(supplied) > 1:
            check_issues.append("DUPLICATE_RECORDS_REQUIRE_REVIEW")
        if any(status in ("POTENTIAL MATCH", "CONFIRMED MATCH") for status in statuses):
            status = "POTENTIAL MATCH"
            check_issues.append("HUMAN_MATCH_REVIEW_REQUIRED")
        elif not supplied or all(status == "NOT PERFORMED" for status in statuses):
            status = "NOT PERFORMED"
        elif check_issues or any(status != "NO MATCH" for status in statuses):
            status = "INCOMPLETE"
        else:
            status = "NO MATCH REPORTED"
        checks.append({
            "requirement_ref": _ref(key),
            "check": requirement["check"],
            "status": status,
            "evidence_refs": sorted(set(references)),
            "issues": sorted(set(check_issues)),
        })

    statuses = [check["status"] for check in checks]
    if unmatched_hit or "POTENTIAL MATCH" in statuses:
        overall = "POTENTIAL MATCH"
    elif issues or "INCOMPLETE" in statuses:
        overall = "INCOMPLETE"
    elif "NOT PERFORMED" in statuses:
        overall = "NOT PERFORMED" if all(s == "NOT PERFORMED" for s in statuses) else "INCOMPLETE"
    else:
        overall = "NO MATCH REPORTED"
    return {
        "schema_version": 1,
        "as_of": as_of.isoformat(),
        "mode": "SUPPLIED EVIDENCE VALIDATION ONLY",
        "status": overall,
        "operational_readiness": (
            "ESCALATE" if overall == "POTENTIAL MATCH" else
            "PRELIMINARY READY FOR HUMAN REVIEW" if overall == "NO MATCH REPORTED" else "HOLD"
        ),
        "issues": sorted(set(issues)),
        "checks": checks,
        "limitations": [
            "NO LIVE SCREENING PERFORMED",
            "EVIDENCE AUTHENTICITY NOT VERIFIED",
            "REQUIRED SCOPE IS CALLER SUPPLIED",
            "NOT AN ADMISSION OR PAYMENT DECISION",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Local version 1 JSON evidence file")
    args = parser.parse_args(argv)
    try:
        with open(args.input, encoding="utf-8") as handle:
            payload = json.load(handle, object_pairs_hook=_unique_object,
                                parse_constant=_reject_constant)
        result = validate_evidence(payload)
    except (OSError, ValueError, TypeError, OverflowError, RecursionError):
        # Parser diagnostics, filenames and supplied values can contain personal data.
        print(json.dumps({"status": "INCOMPLETE", "operational_readiness": "HOLD",
                          "error": "INVALID_OR_UNREADABLE_EVIDENCE"}))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "NO MATCH REPORTED" else 1


if __name__ == "__main__":
    sys.exit(main())
