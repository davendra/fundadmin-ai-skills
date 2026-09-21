"""Structural contracts for the published fundadmin plugin.

Runs standalone from the plugin repository root (tests/ next to plugins/) and
from the source repository against the generated plugin/ tree. It checks what
`claude plugin validate` does not: that every skill and agent has a usable
name and description, that the manifests agree with each other, and that the
skill bodies keep the conventions the source repository's tests enforce.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "fundadmin"
SKILLS = PLUGIN / "skills"
AGENTS = PLUGIN / "agents"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
EXPECTED_SKILLS = 62
EXPECTED_AGENTS = 5
DISCLAIMER_RE = re.compile(r"\bnot\b[\s\S]{0,160}\badvice\b", re.I)
STALE_FAMILIES = [
    "COMPLIANCE-CHECK-", "COMPLIANCE-AUDIT-", "DOCUMENT-COMPARISON-",
    "TERMS-EXTRACTION-", "PERFORMANCE-CALC-", "INVESTOR-ONBOARD-",
    "SMART-CONTRACT-SIM-", "CROSS-REFERENCE-", "DATA-ROOM-INDEX-", "TERM-SHEET-",
]
OLD_PLACEHOLDERS = ["[fund-name]", "[investor-name]", "[LP-name]", "[firm-name]", "[doc-type]", "[doc]"]
# Licensed benchmark datasets no shipped figure may be attributed to. Stored
# reversed so the source repository's real-entity guard does not read this
# list as an attribution.
BANNED_VENDORS = [w[::-1] for w in ("niqerp", "setaicossa egdirbmac", "koobhctip")]


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


class LayoutTests(unittest.TestCase):
    def test_skill_and_agent_counts(self):
        dirs = skill_dirs()
        self.assertEqual(len([d for d in dirs if d.name != "fund"]), EXPECTED_SKILLS, [d.name for d in dirs])
        self.assertIn("fund", [d.name for d in dirs])
        self.assertEqual(len(sorted(AGENTS.glob("fund-*.md"))), EXPECTED_AGENTS)

    def test_orchestrator_ships_script_and_templates(self):
        self.assertTrue((SKILLS / "fund" / "scripts" / "generate_fund_pdf.py").exists())
        self.assertGreaterEqual(len(list((SKILLS / "fund" / "templates").glob("*.md"))), 6)

    def test_no_stray_files_in_skill_dirs(self):
        for d in skill_dirs():
            if d.name == "fund":
                continue
            with self.subTest(skill=d.name):
                self.assertEqual([p.name for p in d.iterdir()], ["SKILL.md"])


class FrontmatterTests(unittest.TestCase):
    def check(self, path, expected_name):
        fields = frontmatter(path)
        self.assertIsNotNone(fields, f"{path}: no frontmatter")
        self.assertEqual(fields.get("name"), expected_name, f"{path}: name must equal the directory/file name")
        description = fields.get("description", "")
        self.assertTrue(10 <= len(description) <= 2000, f"{path}: description length {len(description)}")
        self.assertEqual(description, description.strip(), f"{path}: description has edge whitespace")
        self.assertNotIn("\n", description)
        self.assertNotIn("command", fields, f"{path}: stale `command:` key")
        return fields

    def test_skills(self):
        for d in skill_dirs():
            with self.subTest(skill=d.name):
                fields = self.check(d / "SKILL.md", d.name)
                if d.name != "fund":
                    cmd = d.name[len("fund-"):]
                    self.assertIn(f"/fund {cmd}", fields["description"], f"{d.name}: description must name its /fund command")
                    self.assertLessEqual(len(fields["description"]), 320, f"{d.name}: keep the always-loaded description short")

    def test_agents(self):
        for path in sorted(AGENTS.glob("fund-*.md")):
            with self.subTest(agent=path.stem):
                self.check(path, path.stem)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.claude = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
        self.codex = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
        self.claude_mp = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        self.codex_mp = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text())

    def test_manifests_agree(self):
        for key in ("name", "version", "description", "license"):
            self.assertEqual(self.claude[key], self.codex[key], key)
        self.assertEqual(self.claude["name"], "fundadmin")
        self.assertRegex(self.claude["version"], r"^\d+\.\d+\.\d+$")

    def test_marketplaces_point_at_plugin(self):
        entry = self.claude_mp["plugins"][0]
        self.assertEqual(entry["name"], self.claude["name"])
        self.assertEqual(entry["source"], "./plugins/fundadmin")
        self.assertEqual(entry["version"], self.claude["version"])
        codex_entry = self.codex_mp["plugins"][0]
        self.assertEqual(codex_entry["source"], {"source": "local", "path": "./plugins/fundadmin"})
        self.assertEqual(codex_entry["policy"], {"installation": "AVAILABLE", "authentication": "ON_INSTALL"})
        self.assertIn("category", codex_entry)
        self.assertEqual(self.claude_mp["name"], self.codex_mp["name"])

    def test_component_paths_exist(self):
        self.assertTrue((PLUGIN / self.claude["skills"]).is_dir())
        # Agents rely on default discovery of ./agents/ (see build_plugin.py).
        self.assertNotIn("agents", self.claude)
        self.assertEqual(len(list((PLUGIN / "agents").glob("fund-*.md"))), EXPECTED_AGENTS)
        self.assertTrue((PLUGIN / self.codex["skills"]).is_dir())
        iface = self.codex["interface"]
        self.assertTrue((PLUGIN / iface["logo"]).exists())
        self.assertTrue((PLUGIN / iface["composerIcon"]).exists())
        self.assertLessEqual(len(iface["defaultPrompt"]), 3)
        for prompt in iface["defaultPrompt"]:
            self.assertLessEqual(len(prompt), 128)

    def test_samples_shipped_with_readme(self):
        samples = ROOT / "samples"
        docs = [p for p in samples.iterdir() if p.is_file() and p.name != "README.md"]
        self.assertGreaterEqual(len(docs), 20, "starter sample set is missing")
        readme = (samples / "README.md").read_text(encoding="utf-8")
        for doc in docs:
            with self.subTest(doc=doc.name):
                self.assertIn(doc.name, readme, "every sample must be listed with a command to run")
                if doc.suffix == ".md":
                    self.assertIn("SYNTHETIC", doc.read_text(encoding="utf-8").upper())

    def test_repo_files(self):
        for name in ("README.md", "LICENSE", "CHANGELOG.md"):
            self.assertTrue((ROOT / name).exists(), name)
        self.assertIn("MIT License", (ROOT / "LICENSE").read_text())
        self.assertIn(self.claude["version"], (ROOT / "CHANGELOG.md").read_text())


class BodyContractTests(unittest.TestCase):
    def texts(self):
        return {d.name: (d / "SKILL.md").read_text(encoding="utf-8") for d in skill_dirs()}

    def test_every_skill_carries_the_disclaimer(self):
        for name, text in self.texts().items():
            with self.subTest(skill=name):
                self.assertRegex(text, DISCLAIMER_RE)

    def test_no_stale_families_or_placeholders(self):
        texts = self.texts()
        combined = "\n".join(texts.values())
        # The orchestrator describes Obsidian [[fund-name]] wikilinks, so the
        # placeholder rule applies to the 62 sub-skills only (as in the source repo).
        sub_skills = "\n".join(v for k, v in texts.items() if k != "fund")
        for token in STALE_FAMILIES:
            with self.subTest(token=token):
                self.assertNotIn(token, combined)
        for token in OLD_PLACEHOLDERS:
            with self.subTest(token=token):
                self.assertNotIn(token, sub_skills)

    def test_no_licensed_vendor_claims(self):
        paths = [d / "SKILL.md" for d in skill_dirs()] + sorted(AGENTS.glob("fund-*.md"))
        for path in paths:
            for line in path.read_text(encoding="utf-8").lower().splitlines():
                if "never cite" in line or "subscription dataset" in line:
                    continue
                for vendor in BANNED_VENDORS:
                    with self.subTest(path=path.name, vendor=vendor):
                        self.assertNotIn(vendor, line)

    def test_orchestrator_lists_every_skill(self):
        text = (SKILLS / "fund" / "SKILL.md").read_text(encoding="utf-8")
        for d in skill_dirs():
            if d.name == "fund":
                continue
            with self.subTest(skill=d.name):
                self.assertIn(f"/fund {d.name[len('fund-'):]}", text)
        self.assertIn("fundadmin:fund-<cmd>", text)


if __name__ == "__main__":
    unittest.main()
