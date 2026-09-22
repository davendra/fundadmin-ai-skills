#!/usr/bin/env python3
"""Deterministic methodology-v2 LPA document favourability; standard library only."""

import argparse
import json
import math
import sys
from decimal import Decimal, ROUND_HALF_UP


WEIGHTS = {"terms": 20, "risk": 25, "compliance": 20, "obligations": 15}


def number(value, low, high, label):
    if (type(value) not in (int, float) or not math.isfinite(value)
            or not low <= value <= high):
        raise ValueError("{} must be a finite number in [{}, {}]".format(label, low, high))
    return Decimal(str(value))


def rounded(value):
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def score_lpa(data):
    """Validate evidence-bearing dimension inputs; never impute missing values."""
    if not isinstance(data, dict) or set(data) - {"dimensions", "coverage"}:
        raise ValueError("input must be an object with dimensions and optional coverage")
    dimensions = data.get("dimensions", {})
    if not isinstance(dimensions, dict) or set(dimensions) - set(WEIGHTS):
        raise ValueError("dimensions accepts only terms, risk, compliance, obligations")
    coverage = data.get("coverage")
    coverage_result = None
    if coverage is not None:
        if not isinstance(coverage, dict) or set(coverage) != {"assessed", "expected"}:
            raise ValueError("coverage requires assessed and expected counts")
        assessed, expected = coverage["assessed"], coverage["expected"]
        if (type(assessed) is not int or type(expected) is not int
                or expected <= 0 or not 0 <= assessed <= expected):
            raise ValueError("coverage requires integer counts: 0 <= assessed <= expected, expected > 0")
        coverage_result = dict(coverage, percent=rounded(Decimal(assessed) * 100 / expected))
    missing, rows, total = [], {}, Decimal(0)
    for name, weight in WEIGHTS.items():
        entry = dimensions.get(name)
        if entry is None:
            missing.append(name)
            rows[name] = {"status": "unavailable", "weight": weight}
            continue
        if not isinstance(entry, dict) or set(entry) != {"value", "source_ids", "rationale"}:
            raise ValueError(name + " requires value, source_ids and rationale")
        sources = entry["source_ids"]
        if (not isinstance(sources, list) or not sources
                or any(not isinstance(s, str) or not s.strip() for s in sources)
                or len(set(sources)) != len(sources)):
            raise ValueError(name + " requires non-empty, unique source identifiers")
        if not isinstance(entry["rationale"], str) or not entry["rationale"].strip():
            raise ValueError(name + " requires a non-empty rationale")
        value = number(entry["value"], 1 if name == "risk" else 0,
                       10 if name == "risk" else 100, name)
        normalised = (10 - value) * 100 / 9 if name == "risk" else value
        contribution = normalised * weight / 80
        total += contribution
        rows[name] = dict(entry, status="available", weight=weight,
                          normalised=rounded(normalised), contribution=rounded(contribution))
    return {
        "methodology_version": 2,
        "label": "LPA document favourability (heuristic, not a safety verdict)",
        "status": "unavailable" if missing else "available",
        "aggregate": None if missing else rounded(total),
        "missing_dimensions": missing,
        "weight_denominator": 80,
        "dimensions": rows,
        "coverage": coverage_result,
    }


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("non-finite JSON number: " + value)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="-", help="JSON path, or - for stdin (default)")
    args = parser.parse_args(argv)
    try:
        if args.input == "-":
            raw = sys.stdin.read()
        else:
            with open(args.input, encoding="utf-8") as handle:
                raw = handle.read()
        data = json.loads(raw, object_pairs_hook=unique_object, parse_constant=reject_constant)
        result = score_lpa(data)
    except (ValueError, OSError, OverflowError, RecursionError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
