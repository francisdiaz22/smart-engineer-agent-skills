import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "tools" / "repo-scan.py"
FIXTURES = ROOT / "tests" / "fixtures"


def scan(path: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCANNER), str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


class V05ReviewTests(unittest.TestCase):
    def test_skills_have_static_safety_contracts_and_reports(self):
        environment = (ROOT / "skills/developer-environment-review/SKILL.md").read_text()
        automation = (ROOT / "skills/local-automation-review/SKILL.md").read_text()
        for text in (environment, automation):
            self.assertIn("static", text.lower())
            self.assertIn("read-only", text.lower())
            self.assertIn("Never", text)
            self.assertIn("## Required report", text)
            self.assertIn("NO HIGH-RISK INDICATORS FOUND", text)

    def test_safe_v05_fixtures_have_no_high_risk_findings(self):
        environment = scan(FIXTURES / "developer-environment-review/safe")
        automation = scan(FIXTURES / "local-automation-review/safe")
        for report in (environment, automation):
            self.assertEqual(report["summary"]["high"], 0)
            self.assertEqual(report["summary"]["status"], "NO HIGH-RISK INDICATORS FOUND")
            self.assertTrue(report["safety"]["read_only"])
            self.assertFalse(report["safety"]["network_requests"])
            self.assertFalse(report["safety"]["executed_repository_code"])
        self.assertGreaterEqual(len(environment["developer_environments"]), 1)
        self.assertGreaterEqual(len(automation["local_automations"]), 1)

    def test_suspicious_v05_fixtures_have_expected_evidence(self):
        environment = scan(FIXTURES / "developer-environment-review/suspicious")
        automation = scan(FIXTURES / "local-automation-review/suspicious")
        self.assertEqual(environment["summary"]["status"], "HIGH-RISK FINDINGS")
        for kind in ("developer-environment-privilege", "developer-environment-bootstrap"):
            self.assertTrue(any(item["kind"] == kind for item in environment["findings"]), kind)
        self.assertEqual(automation["summary"]["status"], "HIGH-RISK FINDINGS")
        for kind in ("automation-lifecycle", "automation-high-risk-command", "automation-persistence"):
            self.assertTrue(any(item["kind"] == kind for item in automation["findings"]), kind)

    def test_v05_fixture_contracts_are_inert_and_have_expected_outputs(self):
        roots = (
            FIXTURES / "developer-environment-review",
            FIXTURES / "local-automation-review",
        )
        for root in roots:
            for variant in ("safe", "suspicious"):
                fixture = root / variant
                self.assertTrue((fixture / "EXPECTED.md").exists())
                text = "\n".join(path.read_text(errors="replace") for path in fixture.rglob("*") if path.is_file())
                self.assertIn("example.invalid", text) if variant == "suspicious" and root.name == "developer-environment-review" else None
                self.assertNotIn("curl https://", text.replace("curl -fsSL https://example.invalid", ""))

    def test_collector_exposes_backward_compatible_schema_and_no_side_effects(self):
        report = scan(FIXTURES / "developer-environment-review/suspicious")
        self.assertEqual(report["schema_version"], "0.2")
        self.assertIn("mcp_configurations", report)
        self.assertIn("ci_workflows", report)
        self.assertIn("developer_environments", report)
        self.assertIn("local_automations", report)
        self.assertFalse(report["safety"]["network_requests"])
        self.assertFalse(report["safety"]["executed_repository_code"])


if __name__ == "__main__":
    unittest.main()
