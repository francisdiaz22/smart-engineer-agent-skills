import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class V03SkillTests(unittest.TestCase):
    def test_dependency_skill_has_static_safety_contract_and_report(self):
        text = (ROOT / "skills/dependency-risk-review/SKILL.md").read_text()
        self.assertIn("name: dependency-risk-review", text)
        self.assertIn("Do not install or restore packages", text)
        self.assertIn("Do not execute commands copied", text)
        self.assertIn("## Required report", text)
        self.assertIn("DO NOT INSTALL", text)

    def test_secrets_skill_requires_redaction_and_rotation_guidance(self):
        text = (ROOT / "skills/secrets-preflight/SKILL.md").read_text()
        self.assertIn("name: secrets-preflight", text)
        self.assertIn("Never print, copy, validate, decode, upload, or use", text)
        self.assertIn("Redact matched values", text)
        self.assertIn("rotate/revoke", text)
        self.assertIn("STOP DISTRIBUTION AND ROTATE EXPOSED CREDENTIALS", text)

    def test_dependency_fixtures_are_valid_json_and_inert(self):
        for path in (ROOT / "tests/fixtures/dependency-risk-review").rglob("package*.json"):
            json.loads(path.read_text())
        suspicious = (ROOT / "tests/fixtures/dependency-risk-review/suspicious/package.json").read_text()
        self.assertIn("example.invalid", suspicious)
        self.assertNotIn("npm install", suspicious)

    def test_secrets_fixture_values_are_explicitly_non_live(self):
        safe = (ROOT / "tests/fixtures/secrets-preflight/safe/config.env.example").read_text()
        suspicious = (ROOT / "tests/fixtures/secrets-preflight/suspicious/config.env").read_text()
        self.assertIn("TOKEN_PLACEHOLDER", safe)
        self.assertIn("REDACTED_FIXTURE_ONLY", suspicious)
        self.assertIn("example.invalid", suspicious)


if __name__ == "__main__":
    unittest.main()
