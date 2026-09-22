"""Deterministic, offline fund workpapers. See docs/production/calculations.md."""
import argparse
import hashlib
import json
import re
import sys
from datetime import date
from decimal import (Context, Decimal, DecimalException, localcontext, ROUND_DOWN,
                     ROUND_HALF_EVEN, ROUND_HALF_UP)

VERSION = "1.1.0"
ZERO = Decimal(0)
ONE = Decimal(1)
ROUNDINGS = {"ROUND_HALF_EVEN": ROUND_HALF_EVEN, "ROUND_HALF_UP": ROUND_HALF_UP,
             "ROUND_DOWN": ROUND_DOWN}


class CalculationError(ValueError):
    """Invalid or unsupported calculation input."""


def require(condition, message):
    if not condition:
        raise CalculationError(message)


def fields(obj, required, optional=()):
    require(isinstance(obj, dict), "Expected an object")
    require(all(isinstance(key, str) for key in obj), "Object keys must be strings")
    require(set(required) <= set(obj), "Missing fields: " + ", ".join(sorted(set(required) - set(obj))))
    require(set(obj) <= set(required) | set(optional), "Unknown fields: " + ", ".join(sorted(set(obj) - set(required) - set(optional))))


def number(value):
    # Strings prevent loss of precision before this library receives the input.
    require(type(value) in (str, int, Decimal), "Numbers must be decimal strings or integers; floats and booleans are rejected")
    text = str(value)
    require(len(text) <= 80 and re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", text), "Invalid decimal")
    try:
        result = Decimal(text)
    except DecimalException as exc:
        raise CalculationError("Invalid decimal") from exc
    require(result.is_finite() and len(result.as_tuple().digits) <= 28 and -18 <= result.as_tuple().exponent <= 18 and abs(result) <= Decimal("1e24"), "Decimal outside supported finite range (28 digits, exponent -18..18, magnitude <=1e24)")
    return result


def positive(value):
    result = number(value)
    require(result >= 0, "Expected a non-negative value")
    return result


def rate(value):
    result = positive(value)
    require(result <= 1, "Rate must be between 0 and 1")
    return result


def day(value):
    require(isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value), "Expected ISO date YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise CalculationError("Invalid calendar date") from exc


def rows(value):
    require(isinstance(value, list) and 0 < len(value) <= 1000, "Expected 1..1000 rows")
    return value


def label(value):
    require(isinstance(value, str) and 0 < len(value.strip()) <= 200, "Expected a non-empty label (<=200 characters)")
    return value


class Settings:
    def __init__(self, config):
        fields(config, ("currency", "decimal_places", "rounding"))
        require(isinstance(config["currency"], str) and re.fullmatch(r"[A-Z]{3}", config["currency"]), "Currency must be a three-letter code")
        require(type(config["decimal_places"]) is int and 0 <= config["decimal_places"] <= 8, "decimal_places must be an integer 0..8")
        require(isinstance(config["rounding"], str) and config["rounding"] in ROUNDINGS, "Unsupported rounding")
        self.quantum = ONE.scaleb(-config["decimal_places"])
        self.rounding = ROUNDINGS[config["rounding"]]
        self.currency = config["currency"]

    def money(self, value):
        result = value.quantize(self.quantum, rounding=self.rounding)
        return abs(result) if result == 0 else result

    def exact_money(self, value):
        result = positive(value)
        require(result == self.money(result), "Amount must already be in configured currency units")
        return result


def allocate(data, cfg):
    fields(data, ("total", "participants"))
    total = cfg.exact_money(data["total"])
    entries, ids, reported = [], set(), {}
    for row in rows(data["participants"]):
        fields(row, ("id", "weight"), ("reported_amount",))
        identity = label(row["id"])
        require(identity not in ids, "Duplicate participant id")
        ids.add(identity)
        entries.append((identity, positive(row["weight"])))
        reported[identity] = (cfg.exact_money(row["reported_amount"])
                              if row.get("reported_amount") is not None else None)
    weight = sum((v for _, v in entries), ZERO)
    require(weight > 0, "Total eligible weight must be positive")
    work = []
    for identity, value in entries:
        raw = total * value / weight
        base = raw.quantize(cfg.quantum, rounding=ROUND_DOWN)
        work.append({"id": identity, "weight": value, "raw": raw, "base": base,
                     "residual": ZERO, "amount": base})
    units = int((total - sum((r["base"] for r in work), ZERO)) / cfg.quantum)
    # Largest fractional remainder; ties broken by id, independent of input order.
    ranked = sorted(work, key=lambda r: (-(r["raw"] - r["base"]), r["id"]))
    for row in ranked[:units]:
        row["residual"] = cfg.quantum
        row["amount"] += cfg.quantum
    for row in work:
        actual = reported[row["id"]]
        row["reported_amount"] = actual
        row["difference"] = actual - row["amount"] if actual is not None else None
        row["comparison_status"] = ("unverifiable" if actual is None else
                                    "pass" if actual == row["amount"] else "fail")
    statuses = {row["comparison_status"] for row in work}
    return {"total": total, "allocated": sum((r["amount"] for r in work), ZERO),
            "residual_units": units, "method": "largest_remainder_id_tiebreak", "rows": work,
            "tolerance": ZERO, "comparison_status": "fail" if "fail" in statuses else
            "unverifiable" if "unverifiable" in statuses else "pass"}


def capital_call_status(data, cfg):
    """Descriptive scoring and independent review blockers; never payment authority."""
    fields(data, ("scores", "high_risk_findings", "wire_changed", "required_unknowns", "failed_checks"))
    weights = {"calculation_accuracy": Decimal("0.35"), "completeness": Decimal("0.25"),
               "lpa_compliance": Decimal("0.25"), "wire_quality": Decimal("0.15")}
    fields(data["scores"], weights)
    blockers = []
    for key in ("high_risk_findings", "required_unknowns", "failed_checks"):
        require(isinstance(data[key], list) and len(data[key]) <= 1000, "Expected 0..1000 findings")
        blockers.extend({"type": key, "detail": label(value)} for value in data[key])
    require(data["wire_changed"] is None or type(data["wire_changed"]) is bool,
            "wire_changed must be boolean or null (unknown)")
    if data["wire_changed"] is not False:
        blockers.append({"type": "wire_changed", "detail": "changed" if data["wire_changed"] else "unknown"})
    weighted, complete = [], True
    for name, weight in weights.items():
        score = data["scores"][name]
        if score is None:
            complete = False
            blockers.append({"type": "missing_score", "detail": name})
        else:
            score = number(score)
            require(1 <= score <= 10, "Dimension scores must be 1..10 or null")
        weighted.append({"dimension": name, "score": score, "weight": weight,
                         "weighted_score": score * weight if score is not None else None})
    raw = sum((row["weighted_score"] for row in weighted), ZERO) if complete else None
    return {"score": raw.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) if raw is not None else None,
            "raw_score": raw, "dimensions": weighted, "blockers": blockers,
            "status": "blocked" if blockers else "human_review_required",
            "payment_approved": False}


def ytd_income(data, cfg):
    """Reconcile signed income over a fully covered, comparable year-to-date window."""
    fields(data, ("year_start", "period_end", "periods", "reported_ytd"))
    start, end = day(data["year_start"]), day(data["period_end"])
    require(0 < (end - start).days <= 366, "YTD window must contain 1..366 days (end exclusive)")
    periods = []
    for row in rows(data["periods"]):
        fields(row, ("start", "end", "income"))
        left, right = day(row["start"]), day(row["end"])
        require(start <= left < right <= end, "Income period must lie within the YTD window")
        periods.append((left, right, number(row["income"]) if row["income"] is not None else None))
    periods.sort(key=lambda item: (item[0], item[1]))
    cursor, missing, unknown, observed = start, [], [], ZERO
    for left, right, income in periods:
        require(left >= cursor, "Income periods overlap")
        if left > cursor:
            missing.append({"start": cursor.isoformat(), "end": left.isoformat()})
        if income is None:
            unknown.append({"start": left.isoformat(), "end": right.isoformat()})
        else:
            observed += income
        cursor = right
    if cursor < end:
        missing.append({"start": cursor.isoformat(), "end": end.isoformat()})
    reported = number(data["reported_ytd"]) if data["reported_ytd"] is not None else None
    require(reported is None or reported == cfg.money(reported), "Reported YTD must be in configured currency units")
    expected = cfg.money(observed) if not missing and not unknown else None
    difference = reported - expected if reported is not None and expected is not None else None
    return {"observed_income": observed, "expected_ytd": expected, "reported_ytd": reported,
            "difference": difference, "missing_periods": missing, "unknown_periods": unknown,
            "status": "unverifiable" if difference is None else "pass" if difference == 0 else "fail"}


def ks_pme(data, cfg):
    """NAV-inclusive Kaplan–Schoar PME; supplied total-return index levels only."""
    fields(data, ("valuation_date", "cashflows", "index_end", "benchmark_id", "benchmark_currency",
                  "cashflow_basis", "nav_basis"), ("nav",))
    terminal = day(data["valuation_date"])
    label(data["benchmark_id"])
    require(data["benchmark_currency"] == cfg.currency, "Benchmark and cash flows must use the configured currency")
    require(data["cashflow_basis"] in ("gross", "net") and data["nav_basis"] == data["cashflow_basis"],
            "Cash flows and NAV must share an explicit gross/net basis")
    index_end = positive(data["index_end"])
    require(index_end > 0, "Index levels must be positive")
    levels, work, paid, distributed = {terminal: index_end}, [], ZERO, ZERO
    for row in rows(data["cashflows"]):
        fields(row, ("date", "contribution", "distribution", "index"))
        when, index = day(row["date"]), positive(row["index"])
        require(when <= terminal, "Cash flows cannot follow the valuation date")
        require(index > 0, "Index levels must be positive")
        require(when not in levels or levels[when] == index, "Conflicting index levels on the same date")
        levels[when] = index
        contribution, distribution = positive(row["contribution"]), positive(row["distribution"])
        factor = index_end / index
        # Multiply before dividing to avoid rounding a repeating factor prematurely.
        c_fv, d_fv = contribution * index_end / index, distribution * index_end / index
        paid += c_fv
        distributed += d_fv
        work.append({"date": row["date"], "index": index, "factor": factor,
                     "contribution_fv": c_fv, "distribution_fv": d_fv})
    nav = positive(data["nav"]) if data.get("nav") is not None else None
    numerator = distributed + nav if nav is not None else None
    return {"method": "kaplan_schoar_nav_inclusive", "valuation_date": data["valuation_date"],
            "contributions_fv": paid, "distributions_fv": distributed, "nav": nav,
            "numerator": numerator, "rows": work,
            "pme": numerator / paid if numerator is not None and paid > 0 else None,
            "status": "unknown_nav" if nav is None else "undefined_no_contributions" if paid == 0 else "calculated"}


def rollforward(data, cfg):
    fields(data, ("opening", "contributions", "income", "gains", "fees", "distributions"), ("reported_closing",))
    values = {key: (number(data[key]) if key in ("opening", "income", "gains") else positive(data[key]))
              for key in ("opening", "contributions", "income", "gains", "fees", "distributions")}
    raw = values["opening"] + values["contributions"] + values["income"] + values["gains"] - values["fees"] - values["distributions"]
    result = {"components": values, "formula": "opening + contributions + income + gains - fees - distributions", "raw_closing": raw, "closing": cfg.money(raw)}
    if "reported_closing" in data:
        result["difference"] = cfg.money(number(data["reported_closing"]) - result["closing"])
    return result


def fraction(start, end, convention):
    require(end > start, "Period end must follow start (end exclusive)")
    if convention in ("ACT/365F", "ACT/360"):
        return Decimal((end - start).days) / (365 if convention == "ACT/365F" else 360)
    require(convention == "ACT/ACT", "Supported day counts: ACT/365F, ACT/360, ACT/ACT")
    result = ZERO
    while start < end:
        stop = min(end, date(start.year + 1, 1, 1)) if start.year < 9999 else end
        leap = start.year % 4 == 0 and (start.year % 100 != 0 or start.year % 400 == 0)
        result += Decimal((stop - start).days) / (366 if leap else 365)
        start = stop
    return result


def fees(data, cfg):
    fields(data, ("periods", "opening_offset", "offset_policy"))
    require(data["offset_policy"] in ("carry_forward", "expire"), "Unsupported offset policy")
    balance, output, previous = positive(data["opening_offset"]), [], None
    for row in rows(data["periods"]):
        fields(row, ("start", "end", "basis", "annual_rate", "day_count", "offset_generated", "offset_rate"))
        start, end = day(row["start"]), day(row["end"])
        require(previous is None or start >= previous, "Fee periods must be ordered and non-overlapping")
        elapsed = fraction(start, end, row["day_count"])
        gross = positive(row["basis"]) * rate(row["annual_rate"]) * elapsed
        available = balance + positive(row["offset_generated"]) * rate(row["offset_rate"])
        applied = min(gross, available)
        excess = available - applied
        balance = excess if data["offset_policy"] == "carry_forward" else ZERO
        output.append({"start": row["start"], "end": row["end"], "year_fraction": elapsed,
                       "gross_raw": gross, "offset_available": available, "offset_applied": applied,
                       "offset_expired": excess - balance, "offset_carried": balance,
                       "net_raw": gross - applied, "net": cfg.money(gross - applied)})
        previous = end
    return {"periods": output, "net_total": sum((r["net"] for r in output), ZERO), "closing_offset": balance}


def waterfall(data, cfg):
    fields(data, ("model", "proceeds", "unreturned_capital", "preferred_due", "carry_rate", "catch_up"))
    require(data["model"] == "whole_fund_single_event", "Only whole_fund_single_event is supported")
    require(data["catch_up"] in ("none", "full"), "Only none or full (100% GP) catch-up is supported")
    remaining = cfg.exact_money(data["proceeds"])
    capital, pref, carry = positive(data["unreturned_capital"]), positive(data["preferred_due"]), rate(data["carry_rate"])
    require(carry < 1, "Carry must be less than 1")
    capital_paid = min(remaining, capital)
    remaining -= capital_paid
    pref_paid = min(remaining, pref)
    remaining -= pref_paid
    target = pref_paid * carry / (1 - carry) if data["catch_up"] == "full" else ZERO
    catch = min(remaining, target)
    remaining -= catch
    gp_raw = catch + remaining * carry
    gp = cfg.money(gp_raw)
    lp = number(data["proceeds"]) - gp
    return {"capital_paid": capital_paid, "capital_unpaid": capital - capital_paid,
            "preferred_paid": pref_paid, "preferred_unpaid": pref - pref_paid,
            "catch_up_target": target, "catch_up_paid": catch, "residual_pool": remaining,
            "residual_gp_raw": remaining * carry, "gp_raw": gp_raw, "lp_raw": number(data["proceeds"]) - gp_raw,
            "gp": gp, "lp": lp, "lp_rounding_residual": lp - cfg.money(number(data["proceeds"]) - gp_raw),
            "distributed": gp + lp}


def metrics(data, cfg):
    fields(data, ("paid_in", "distributions", "nav", "invested_capital"))
    paid, distributed, nav, invested = (positive(data[k]) for k in ("paid_in", "distributions", "nav", "invested_capital"))
    return {"dpi": distributed / paid if paid else None, "rvpi": nav / paid if paid else None,
            "tvpi": (distributed + nav) / paid if paid else None,
            "moic": (distributed + nav) / invested if invested else None,
            "undefined": [k for k, denominator in (("dpi", paid), ("rvpi", paid), ("tvpi", paid), ("moic", invested)) if not denominator]}


def dated_irr(data, cfg):
    fields(data, ("cashflows", "day_count", "lower_rate", "upper_rate"))
    require(data["day_count"] == "ACT/365F", "IRR supports ACT/365F only")
    low, high = number(data["lower_rate"]), number(data["upper_rate"])
    require(-1 < low < high <= Decimal("1e6"), "IRR bounds must satisfy -1 < lower < upper <= 1e6")
    grouped = {}
    for row in rows(data["cashflows"]):
        fields(row, ("date", "amount"))
        when = day(row["date"])
        grouped[when] = grouped.get(when, ZERO) + number(row["amount"])
    flows = sorted((d, amount) for d, amount in grouped.items() if amount != 0)
    result = {"rate": None, "day_count": "ACT/365F", "bounds": [low, high],
              "cashflows": [{"date": d.isoformat(), "amount": amount} for d, amount in flows]}
    if not flows:
        return dict(result, status="indeterminate_all_zero")
    changes = sum(a * b < 0 for (_, a), (_, b) in zip(flows, flows[1:]))
    result["sign_changes"] = changes
    if changes == 0:
        return dict(result, status="undefined_no_sign_change")
    if changes > 1:
        return dict(result, status="ambiguous_multiple_sign_changes")
    origin = flows[0][0]
    powers = [(Decimal((d - origin).days) / 365, amount) for d, amount in flows]

    def npv(r):
        return sum((amount / ((ONE + r) ** t) for t, amount in powers), ZERO)

    left, right = npv(low), npv(high)
    result["endpoint_npvs"] = [left, right]
    if left * right > 0:
        return dict(result, status="root_outside_bounds")
    trace = []
    # Both interval and scaled NPV tolerance must pass; never present an unconverged rate.
    scale = sum((abs(a) for _, a in flows), ZERO)
    for iteration in range(256):
        midpoint = low if left == 0 else high if right == 0 else (low + high) / 2
        value = npv(midpoint)
        trace.append({"iteration": iteration, "rate": midpoint, "npv": value})
        if value == 0 or (high - low <= Decimal("1e-24") and abs(value) <= scale * Decimal("1e-24")):
            return dict(result, status="unique", rate=midpoint, npv=value, iterations=trace)
        if left * value <= 0:
            high, right = midpoint, value
        else:
            low, left = midpoint, value
    return dict(result, status="not_converged", iterations=trace)


def forecast(data, cfg):
    fields(data, ("opening_nav", "unfunded", "periods", "assumptions"))
    label(data["assumptions"])
    nav, unfunded, previous, output = positive(data["opening_nav"]), positive(data["unfunded"]), None, []
    for row in rows(data["periods"]):
        fields(row, ("date", "contribution", "growth_rate", "distribution_rate", "fees"))
        when = day(row["date"])
        require(previous is None or when > previous, "Forecast dates must increase")
        contribution, charge = positive(row["contribution"]), positive(row["fees"])
        growth, payout = number(row["growth_rate"]), rate(row["distribution_rate"])
        require(growth >= -1, "Period growth cannot be below -100%")
        require(contribution <= unfunded, "Contributions exceed unfunded commitment")
        gain = nav * growth
        available = nav + gain + contribution - charge
        require(available >= 0, "Fees exceed available NAV; provide an explicit funding assumption")
        distribution = available * payout
        closing = available - distribution
        unfunded -= contribution
        output.append({"date": row["date"], "opening_nav": nav, "contribution": contribution,
                       "growth": gain, "fees": charge, "distribution": distribution, "closing_nav": closing,
                       "unfunded": unfunded, "net_lp_cashflow": distribution - contribution,
                       "display_nav": cfg.money(closing), "display_distribution": cfg.money(distribution)})
        nav, previous = closing, when
    return {"assumptions": data["assumptions"], "timing": "growth on opening NAV; contribution then fees then distribution; period rates, no annualisation",
            "periods": output, "closing_nav": nav, "unfunded": unfunded}


def scenario(data, cfg):
    fields(data, ("scenarios",))
    output, names = [], set()
    for row in rows(data["scenarios"]):
        fields(row, ("name", "forecast"))
        name = label(row["name"])
        require(name not in names, "Duplicate scenario name")
        names.add(name)
        output.append({"name": name, "result": forecast(row["forecast"], cfg)})
    return {"scenarios": output, "probabilities": "not modelled"}


def arithmetic(data, cfg):
    """Small explicit workpaper expressions; no eval, code or implicit tax rules."""
    fields(data, ("steps",))
    values, output = {}, []
    for row in rows(data["steps"]):
        fields(row, ("id", "operator", "operands"), ("round",))
        name = label(row["id"])
        require(name not in values, "Duplicate step id")
        require(row["operator"] in ("add", "subtract", "multiply", "divide"), "Unsupported arithmetic operator")
        require(type(row.get("round", False)) is bool, "round must be boolean")
        args = []
        for operand in rows(row["operands"]):
            if isinstance(operand, dict):
                fields(operand, ("ref",))
                ref = label(operand["ref"])
                require(ref in values, "Reference must name an earlier step")
                args.append(values[ref])
            else:
                args.append(number(operand))
        require(len(args) == 2 or row["operator"] in ("add", "multiply"), "Subtract/divide require two operands")
        value = args[0]
        for arg in args[1:]:
            if row["operator"] == "add":
                value += arg
            elif row["operator"] == "subtract":
                value -= arg
            elif row["operator"] == "multiply":
                value *= arg
            else:
                require(arg != 0, "Division by zero")
                value /= arg
            require(value.is_finite() and abs(value) <= Decimal("1e48"), "Arithmetic result out of range")
        raw = value
        if row.get("round", False):
            value = cfg.money(value)
        values[name] = value
        output.append({"id": name, "operator": row["operator"], "operands": args, "raw": raw, "value": value})
    return {"steps": output}


OPERATIONS = {"allocate": allocate, "rollforward": rollforward, "fees": fees,
              "waterfall": waterfall, "metrics": metrics, "dated_irr": dated_irr,
              "forecast": forecast, "scenario": scenario, "arithmetic": arithmetic,
              "ks_pme": ks_pme, "ytd_income": ytd_income, "capital_call_status": capital_call_status}


def serialise(value):
    if isinstance(value, Decimal):
        require(value.is_finite(), "Non-finite result")
        return format(value, "f")
    if isinstance(value, dict):
        return {k: serialise(v) for k, v in value.items()}
    if isinstance(value, list):
        return [serialise(v) for v in value]
    return value


def calculate(request):
    """Return a JSON-safe reproducible workpaper; raise CalculationError on invalid input."""
    fields(request, ("operation", "inputs", "config"))
    operation = request["operation"]
    require(isinstance(operation, str) and operation in OPERATIONS, "Unsupported operation")
    try:
        with localcontext(Context(prec=64, rounding=ROUND_HALF_EVEN, Emax=9999, Emin=-9999)):
            config = Settings(request["config"])
            result = OPERATIONS[operation](request["inputs"], config)
            normalised = serialise(request)
            canonical = json.dumps(normalised, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
            return serialise({"schema_version": 1, "engine_version": VERSION,
                              "request_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
                              "request": normalised, "precision": 64, "result": result})
    except DecimalException as exc:
        raise CalculationError("Decimal computation exceeded supported precision or range") from exc


def reject_constant(value):
    raise CalculationError("Non-finite JSON number: " + value)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="-", help="JSON request file, or - for stdin")
    args = parser.parse_args(argv)
    try:
        if args.input == "-":
            raw = sys.stdin.read(1000001)
        else:
            with open(args.input, encoding="utf-8") as source:
                raw = source.read(1000001)
        require(len(raw) <= 1000000, "Request exceeds 1,000,000 characters")
        request = json.loads(raw, parse_float=Decimal, parse_constant=reject_constant, object_pairs_hook=unique_object)
        print(json.dumps(calculate(request), sort_keys=True, indent=2, allow_nan=False))
        return 0
    except (CalculationError, DecimalException, ValueError, OSError, RecursionError, TypeError) as exc:
        print(json.dumps({"error": {"type": "invalid_request", "message": str(exc)}}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
