"""Structural checks for shipped Claude plugin eval fixtures.

These assert the eval cases exist and are locally inspectable. They do **not**
run `claude plugin eval` (model/host cost) and do **not** certify production.
Behavioural host evidence remains a private, candidate-bound gate in
docs/production/README.md.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "plugins" / "fundadmin" / "evals"
# Candidate-bound smoke set documented for release evidence (18 prompt.md dirs).
EXPECTED_CASES = frozenset(
    {
        "ambiguous-reconcile",
        "capital-call-autotrigger",
        "capital-rounding",
        "injection-boundary",
        "kyc-disposition",
        "kyc-no-grid",
        "kyc-reader-injection",
        "kyc-tracker-xlsx",
        "menu",
        "performance-unrealised",
        "privacy-mask",
        "report-pdf-fallback",
        "review-lpa",
        "screening-unavailable",
        "signed-ytd",
        "source-conflict",
        "unknown-evidence",
        "wire-readiness",
    }
)
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
GRADER_TYPES = frozenset({"regex", "llm", "json", "model", "tool_used"})


def case_dirs():
    return sorted(p for p in EVALS.iterdir() if p.is_dir() and not p.name.startswith("."))


class EvalFixtureTests(unittest.TestCase):
    def test_evals_root_exists(self):
        self.assertTrue(EVALS.is_dir(), f"missing evals tree at {EVALS}")

    def test_expected_case_set(self):
        names = {p.name for p in case_dirs()}
        self.assertEqual(names, set(EXPECTED_CASES), f"unexpected={sorted(names - EXPECTED_CASES)} missing={sorted(EXPECTED_CASES - names)}")

    def test_each_case_has_prompt_and_graders(self):
        for case in case_dirs():
            with self.subTest(case=case.name):
                prompt = case / "prompt.md"
                self.assertTrue(prompt.is_file(), f"{case.name}: missing prompt.md")
                text = prompt.read_text(encoding="utf-8")
                match = FRONTMATTER.match(text)
                self.assertIsNotNone(match, f"{case.name}: prompt.md needs YAML frontmatter")
                meta = match.group(1)
                self.assertRegex(meta, r"(?m)^max_turns:\s*\d+")
                self.assertIn("allowed_tools:", meta)
                body = text[match.end() :].strip()
                self.assertTrue(body, f"{case.name}: prompt body empty")

                graders = case / "graders"
                self.assertTrue(graders.is_dir(), f"{case.name}: missing graders/")
                grader_files = sorted(graders.glob("*.md"))
                self.assertGreaterEqual(len(grader_files), 1, f"{case.name}: no graders")
                for g in grader_files:
                    with self.subTest(case=case.name, grader=g.name):
                        gtext = g.read_text(encoding="utf-8")
                        gm = FRONTMATTER.match(gtext)
                        self.assertIsNotNone(gm, f"{g}: grader needs YAML frontmatter")
                        gmeta = gm.group(1)
                        self.assertRegex(gmeta, r"(?m)^type:\s*\S+")
                        self.assertRegex(gmeta, r"(?m)^name:\s*\S+")
                        gtype = re.search(r"(?m)^type:\s*(\S+)", gmeta).group(1)
                        self.assertIn(gtype, GRADER_TYPES, f"{g}: unexpected type {gtype}")
                        if gtype == "regex":
                            self.assertRegex(gmeta, r"(?m)^pattern:")


if __name__ == "__main__":
    unittest.main()
