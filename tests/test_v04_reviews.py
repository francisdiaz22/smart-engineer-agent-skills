import json
import subprocess
import sys
import tempfile
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


class V04ReviewTests(unittest.TestCase):
    def test_mcp_skill_has_static_safety_contract_and_report(self):
        text = (ROOT / "skills/mcp-config-review/SKILL.md").read_text()
        self.assertIn("name: mcp-config-review", text)
        self.assertIn("Do not launch MCP servers", text)
        self.assertIn("Do not", text)
        self.assertIn("## Required report", text)
        self.assertIn("DO NOT ENABLE OR LAUNCH MCP SERVERS", text)

    def test_ci_skill_has_static_safety_contract_and_report(self):
        text = (ROOT / "skills/ci-workflow-review/SKILL.md").read_text()
        self.assertIn("name: ci-workflow-review", text)
        self.assertIn("Do not trigger workflows", text)
        self.assertIn("Do not", text)
        self.assertIn("## Required report", text)
        self.assertIn("DO NOT TRIGGER OR TRUST THE WORKFLOW", text)

    def test_safe_v04_fixtures_have_no_high_risk_findings(self):
        mcp = scan(FIXTURES / "mcp-config/safe")
        ci = scan(FIXTURES / "ci-workflow-review/safe")
        for report in (mcp, ci):
            self.assertEqual(report["summary"]["high"], 0)
            self.assertEqual(report["summary"]["status"], "NO HIGH-RISK INDICATORS FOUND")
            self.assertTrue(report["safety"]["read_only"])
            self.assertFalse(report["safety"]["network_requests"])
            self.assertFalse(report["safety"]["executed_repository_code"])
        self.assertEqual(len(mcp["mcp_configurations"]), 1)
        self.assertEqual(len(ci["ci_workflows"]), 1)

    def test_suspicious_v04_fixtures_have_expected_evidence(self):
        mcp = scan(FIXTURES / "mcp-config/suspicious")
        ci = scan(FIXTURES / "ci-workflow-review/suspicious")
        self.assertEqual(mcp["summary"]["status"], "HIGH-RISK FINDINGS")
        self.assertTrue(any(item["kind"] == "mcp-package-install" for item in mcp["findings"]))
        self.assertTrue(any(item["kind"] == "mcp-secret-environment" for item in mcp["findings"]))
        self.assertTrue(any("example.invalid" in item["url"] for item in mcp["external_indicators"]))
        self.assertEqual(ci["summary"]["status"], "HIGH-RISK FINDINGS")
        for kind in ("ci-privileged-trigger", "ci-runner-privilege", "ci-write-permission", "ci-remote-download", "ci-unpinned-action"):
            self.assertTrue(any(item["kind"] == kind for item in ci["findings"]), kind)
        self.assertTrue(any("example.invalid" in item["url"] for item in ci["external_indicators"]))

    def test_v04_fixture_values_are_inert_placeholders(self):
        suspicious_files = list((FIXTURES / "mcp-config/suspicious").rglob("*")) + list((FIXTURES / "ci-workflow-review/suspicious").rglob("*"))
        text = "\n".join(path.read_text(errors="replace") for path in suspicious_files if path.is_file())
        self.assertIn("example.invalid", text)
        self.assertIn("TOKEN_PLACEHOLDER", text)
        self.assertNotIn("curl https://", text)

    def test_v04_configuration_files_are_present_and_structurally_bounded(self):
        mcp_text = (FIXTURES / "mcp-config/safe/.mcp.json").read_text()
        json.loads(mcp_text)
        for relative in (
            "ci-workflow-review/safe/.github/workflows/check.yml",
            "ci-workflow-review/suspicious/.github/workflows/publish.yml",
        ):
            text = (FIXTURES / relative).read_text()
            self.assertIn("name:", text)
            self.assertIn("jobs:", text)
            self.assertIn("steps:", text)

    def test_malformed_mcp_configuration_is_reported_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".mcp.json").write_text('{"mcpServers": ')
            report = scan(root)
        self.assertEqual(report["summary"]["status"], "NO HIGH-RISK INDICATORS FOUND")
        self.assertEqual(len(report["mcp_configurations"]), 1)
        self.assertFalse(report["safety"]["network_requests"])


if __name__ == "__main__":
    unittest.main()
