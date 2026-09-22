"""Exercise the installed package, not an accidental source-checkout import."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'plugins/fundadmin/skills/fund/scripts'


def module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class InstalledRuntimeTests(unittest.TestCase):
    def test_all_helpers_shipped_and_runnable(self):
        for name in ('fund_report', 'fund_calculations', 'fund_lpa_score', 'fund_screening', 'fund_kyc', 'fund_xlsx', 'generate_fund_pdf'):
            with self.subTest(name=name):
                p = subprocess.run([sys.executable, str(SCRIPTS / (name + '.py')), '--help'], capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stderr)

    def test_installed_evidence_helper_and_no_overwrite(self):
        helper = module('fund_report')
        with tempfile.TemporaryDirectory() as directory:
            run = helper.create_run(Path(directory).resolve(), 'synthetic-fund', [])
            report = dict(schema_version='1.0', report_id='draft', skill='fund-review-lpa', status='PARTIAL', sources=[],
                          findings=[], assumptions=[], limitations=['No source'], checks_not_performed=['Review'], human_review_required=True)
            path = helper.write_report(run, 'reports', 'LPA-REVIEW-test.md', report, '# Synthetic draft')
            self.assertTrue(path.is_file())
            with self.assertRaises(FileExistsError):
                helper.write_report(run, 'reports', path.name, report, 'replacement')

    def test_score_missing_dimensions_not_zero(self):
        self.assertIsNone(module('fund_lpa_score').score_lpa({})['aggregate'])

    def test_pdf_really_renders(self):
        from pypdf import PdfReader
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'input.md'
            target = Path(directory) / 'report.pdf'
            source.write_text('# Reconciliation\n\nUnique fidelity sentinel\n\nMissing screening evidence.\n')
            p = subprocess.run([sys.executable, str(SCRIPTS / 'generate_fund_pdf.py'), '--input', str(source), '--output', str(target)], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn('Unique fidelity sentinel', '\n'.join(page.extract_text() for page in PdfReader(target).pages))


if __name__ == '__main__':
    unittest.main()
