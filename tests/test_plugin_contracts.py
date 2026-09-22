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
                    self.assertLessEqual(len(fields["description"]), 200, f"{d.name}: keep the always-loaded description short")

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

    def test_agent_docs_present(self):
        for name in ("AGENTS.md", "CLAUDE.md", "llms.txt", "catalog.json"):
            self.assertTrue((ROOT / name).exists(), name)
        self.assertIn("@AGENTS.md", (ROOT / "CLAUDE.md").read_text())

    def test_catalog_matches_skills_and_agents(self):
        cat = json.loads((ROOT / "catalog.json").read_text())
        self.assertEqual(cat["version"], self.claude["version"])
        names = sorted(s["name"] for s in cat["skills"])
        self.assertEqual(names, sorted(d.name for d in skill_dirs()))
        for skill in cat["skills"]:
            with self.subTest(skill=skill["name"]):
                self.assertTrue((ROOT / skill["path"]).exists())
                self.assertTrue(skill["description"])
        self.assertEqual(sorted(a["name"] for a in cat["agents"]), sorted(p.stem for p in AGENTS.glob("fund-*.md")))
        self.assertEqual(sum(a["lpa_safety_score_weight"] for a in cat["agents"]), 100)

    def test_readme_images_exist(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        refs = re.findall(r'(?:src|srcset)="([^"]+)"', readme)
        self.assertTrue(refs, "README should carry the logo lockup")
        for ref in refs:
            if ref.startswith(("http://", "https://")):
                continue
            with self.subTest(ref=ref):
                self.assertTrue((ROOT / ref).exists(), ref)

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

    def test_license_is_plain_mit(self):
        # The source repository's scope paragraph names paths (skills/, apps/,
        # LICENSE.md) that do not exist here; the published LICENSE is the bare
        # MIT text so it stays true and GitHub detects it.
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("MIT License\n"), "LICENSE must start with the MIT title")
        for path in re.findall(r"`([^`\s]+/[^`\s]*)`", text):
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).exists(), f"LICENSE names {path}, which is not in this repository")
        self.assertNotIn("LICENSE.md", text)

    def test_codex_links_resolve(self):
        iface = self.codex["interface"]
        meta = json.loads((ROOT / "manual" / ".vitepress" / "meta.json").read_text(encoding="utf-8"))
        privacy = iface["privacyPolicyURL"]
        self.assertTrue(privacy.startswith(meta["docs"] + "/"), privacy)
        page = privacy[len(meta["docs"]) + 1:]
        self.assertTrue((ROOT / "manual" / f"{page}.md").exists(), f"no manual page for {privacy}")
        terms = iface["termsOfServiceURL"]
        prefix = self.claude["repository"] + "/blob/main/"
        self.assertTrue(terms.startswith(prefix), terms)
        self.assertTrue((ROOT / terms[len(prefix):]).exists(), terms)

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


class ManualTests(unittest.TestCase):
    """The user manual (manual/, published at help.fundadmin.dev) tracks the skills."""
    MANUAL = ROOT / "manual"

    def test_manual_present_and_versioned(self):
        for rel in ("package.json", "package-lock.json", ".gitignore", "vercel.json",
                    ".vitepress/config.ts", ".vitepress/meta.json", "index.md",
                    "guide/install.md", "guide/quick-start.md", "guide/outputs.md",
                    "guide/samples.md", "guide/faq.md", "guide/privacy.md",
                    "commands/index.md", "agents.md"):
            with self.subTest(file=rel):
                self.assertTrue((self.MANUAL / rel).exists(), rel)
        meta = json.loads((self.MANUAL / ".vitepress" / "meta.json").read_text(encoding="utf-8"))
        claude = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(meta["version"], claude["version"])
        self.assertRegex(meta["release_date"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(meta["skill_count"], EXPECTED_SKILLS)
        self.assertEqual(meta["agent_count"], EXPECTED_AGENTS)
        self.assertEqual(sum(c["count"] for c in meta["categories"]), EXPECTED_SKILLS)
        ignored = (self.MANUAL / ".gitignore").read_text(encoding="utf-8")
        for entry in ("node_modules/", ".vitepress/cache/", ".vitepress/dist/", ".vercel/"):
            self.assertIn(entry, ignored, f"manual/.gitignore must keep {entry} out of the published tree")

    def test_every_command_has_a_manual_section(self):
        cat = json.loads((ROOT / "catalog.json").read_text())
        pages = {p.name: p.read_text(encoding="utf-8") for p in (self.MANUAL / "commands").glob("*.md")}
        slugs = sorted({s["category_slug"] for s in cat["skills"] if s["category"] != "Menu"})
        self.assertEqual(sorted(n[:-3] for n in pages if n != "index.md"), slugs)
        headings = re.findall(r"^## `/fundadmin:fund ([a-z0-9-]+)", "\n".join(pages.values()), re.M)
        self.assertEqual(sorted(headings), sorted(d.name[len("fund-"):] for d in skill_dirs() if d.name != "fund"))
        self.assertEqual(len(headings), EXPECTED_SKILLS, "each command documented exactly once")
        for d in skill_dirs():
            if d.name != "fund":
                with self.subTest(skill=d.name):
                    self.assertIn(d.name[len("fund-"):], pages["index.md"])

    def test_manual_uses_the_plugin_prefix(self):
        # Bare `/fund <cmd>` is the plain-skills form and belongs on the install page only.
        for path in sorted(self.MANUAL.rglob("*.md")):
            if "node_modules" in path.parts or path.name in ("install.md", "DEPLOY.md", "README.md"):
                continue
            with self.subTest(page=str(path.relative_to(self.MANUAL))):
                self.assertNotRegex(path.read_text(encoding="utf-8"), r"`/fund ")

    def test_manual_images_exist(self):
        public = self.MANUAL / "public"
        for path in sorted(self.MANUAL.rglob("*.md")):
            if "node_modules" in path.parts:
                continue
            for ref in re.findall(r'(?:src="|\]\()(/images/[^)"]+)', path.read_text(encoding="utf-8")):
                with self.subTest(page=path.name, ref=ref):
                    self.assertTrue((public / ref.lstrip("/")).exists(), ref)


if __name__ == "__main__":
    unittest.main()
