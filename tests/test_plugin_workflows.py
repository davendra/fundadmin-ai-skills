"""Synthetic helper-to-sidecar-to-Markdown-to-PDF integration, not model evaluation."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'plugins/fundadmin/skills/fund/scripts'
CONFIG = {'currency': 'GBP', 'decimal_places': 2, 'rounding': 'ROUND_HALF_EVEN'}
DISCLAIMER = 'Not financial, legal or tax advice. Qualified human review is required.'


def module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class WorkflowIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.reporter = module('fund_report')
        self.engine = module('fund_calculations')
        self.source = self.root / 'synthetic-evidence.txt'

    def calculate(self, operation, inputs):
        return self.engine.calculate(dict(operation=operation, config=CONFIG, inputs=inputs))

    def save(self, run, report_id, skill, title, body, workpaper, status='READY_FOR_REVIEW', gaps=None):
        sources = self.reporter.load(run / 'run.json')['sources']
        report = dict(schema_version='1.0', report_id=report_id, skill=skill, status=status,
                      sources=sources, human_review_required=True, assumptions=[], limitations=['Synthetic integration fixture; not model assessment.'],
                      checks_not_performed=gaps or [], findings=[
                          dict(id='source-fact', kind='DOCUMENT_FACT', text='Inputs supplied in synthetic fixture',
                               citations=[dict(source_id='source-1', locator='complete synthetic fixture')]),
                          dict(id='calculation', kind='CALCULATION', text=title, citations=[dict(source_id='source-1', locator='numeric inputs')],
                               workpaper=dict(method=skill, inputs=workpaper.get('request', {'dimensions': 'fixture'}), result=workpaper))])
        markdown = '# ' + title + '\n\n' + body + '\n\nSource: source-1, complete synthetic fixture.\n\n' + DISCLAIMER
        output = self.reporter.write_report(run, 'reports', 'REPORT-' + report_id + '.md', report, markdown)
        sidecar = self.reporter.load(str(output) + '.json')
        self.reporter.validate(sidecar)
        self.assertEqual(sidecar['markdown_sha256'], self.reporter.digest(output))
        self.assertEqual(sidecar['sources'], sources)
        self.assertEqual(sidecar['findings'][1]['workpaper']['result'], workpaper)
        with self.assertRaises(FileExistsError):
            self.reporter.write_report(run, 'reports', output.name, report, 'overwrite')
        pdf = output.with_suffix('.pdf')
        result = subprocess.run([sys.executable, str(SCRIPTS / 'generate_fund_pdf.py'), '--input', str(output), '--output', str(pdf)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        from pypdf import PdfReader
        text = '\n'.join(page.extract_text() for page in PdfReader(pdf).pages)
        for required in (title, body, 'source-1', DISCLAIMER):
            self.assertIn(required, text)
        return output, sidecar

    def run_for(self, text):
        self.source.write_text(text)
        return self.reporter.create_run(self.root, 'example-fund', [self.source])

    def test_lpa_supported_dimensions_preserved_to_pdf(self):
        data = {'dimensions': {name: dict(value=4 if name == 'risk' else 80, source_ids=['source-1'], rationale='Synthetic supported assessment input')
                               for name in ('terms', 'risk', 'compliance', 'obligations')}, 'coverage': {'assessed': 4, 'expected': 4}}
        run = self.run_for(json.dumps(data))
        result = module('fund_lpa_score').score_lpa(data)
        self.assertEqual(result['aggregate'], 75.83)
        self.save(run, 'lpa', 'fund-review-lpa', 'LPA methodology v2', 'Document favourability 75.83; coverage 100%; not a safety verdict.', result)

    def test_capital_draft_and_review_share_sources_and_preserve_rounding(self):
        inputs = {'total': '100.00', 'participants': [{'id': key, 'weight': '1000', 'reported_amount': amount} for key, amount in [('a','33.34'),('b','33.33'),('c','33.33')]]}
        run = self.run_for('Eligible a,b,c; d excused. ' + json.dumps(inputs))
        result = self.calculate('allocate', inputs)
        self.assertEqual([r['amount'] for r in result['result']['rows']], ['33.34','33.33','33.33'])
        self.assertEqual(result['result']['comparison_status'], 'pass')
        _, draft = self.save(run, 'capital-draft', 'fund-draft-capital-call', 'Capital call draft', 'GBP 33.34 / 33.33 / 33.33; total 100.00; d excused.', result, 'PARTIAL', ['Wire instructions unverified'])
        _, review = self.save(run, 'capital-review', 'fund-review-capital-call', 'Capital call review', 'Rounded allocation PASS. HOLD: wire instructions unverified.', result, 'PARTIAL', ['Wire instructions unverified'])
        self.assertEqual(draft['sources'], review['sources'])
        self.assertEqual(draft['run_id'], review['run_id'])

    def test_performance_and_signed_ytd_preserved_to_pdf(self):
        inputs = dict(valuation_date='2026-09-21', cashflows=[dict(date='2025-09-21', contribution='100', distribution='0', index='100')],
                      index_end='100', benchmark_id='synthetic-flat-total-return', benchmark_currency='GBP', cashflow_basis='net', nav_basis='net', nav='110')
        run = self.run_for(json.dumps(inputs) + '\nQ1 income -100; Q2 income +60; reported YTD -40.')
        pme = self.calculate('ks_pme', inputs)
        self.assertEqual(pme['result']['pme'], '1.1')
        self.save(run, 'performance', 'fund-performance-calc', 'Unrealised performance', 'KS-PME 1.1; NAV 110 included once; no peer benchmark claim.', pme)
        ytd = self.calculate('ytd_income', dict(year_start='2026-01-01', period_end='2026-07-01',
                             periods=[dict(start='2026-01-01', end='2026-04-01', income='-100'), dict(start='2026-04-01', end='2026-07-01', income='60')], reported_ytd='-40'))
        self.assertEqual(ytd['result']['status'], 'pass')
        self.save(run, 'capital-account', 'fund-review-capital-account', 'Signed YTD review', 'YTD -40; Q1 -100 plus Q2 60; no sign-based failure.', ytd)

    def test_high_score_cannot_remove_hold_in_saved_report(self):
        inputs = dict(scores=dict(calculation_accuracy=10, completeness=10, lpa_compliance=10, wire_quality=4),
                      high_risk_findings=['Changed beneficiary'], wire_changed=True, required_unknowns=[], failed_checks=[])
        run = self.run_for(json.dumps(inputs))
        result = self.calculate('capital_call_status', inputs)
        self.assertEqual(result['result']['score'], '9.1')
        self.assertEqual(result['result']['status'], 'blocked')
        self.assertFalse(result['result']['payment_approved'])
        self.save(run, 'wire', 'fund-review-capital-call', 'Wire readiness', 'Illustrative score 9.1. HOLD: changed beneficiary. No payment approval.', result, 'BLOCKED', ['Independent wire verification'])


if __name__ == '__main__':
    unittest.main()
