import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "tools" / "repo-scan.py"
FIXTURES = ROOT / "tests" / "fixtures" / "tasks-json-folder-open"


def scan(path: Path) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCANNER), str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


class RepoScanTests(unittest.TestCase):
    def test_safe_folder_open_task_is_low_risk(self):
        report = scan(FIXTURES / "safe")
        self.assertEqual(report["schema_version"], "0.2")
        self.assertEqual(report["summary"]["status"], "NO HIGH-RISK INDICATORS FOUND")
        self.assertEqual(len(report["automatic_execution_paths"]), 1)
        self.assertFalse(report["external_indicators"])

    def test_suspicious_folder_open_task_is_high_risk(self):
        report = scan(FIXTURES / "suspicious")
        self.assertEqual(report["summary"]["status"], "HIGH-RISK FINDINGS")
        self.assertGreaterEqual(report["summary"]["high"], 1)
        self.assertTrue(any("example.invalid" in item["url"] for item in report["external_indicators"]))
        self.assertTrue(any(item["kind"] == "concealment" for item in report["findings"]))


if __name__ == "__main__":
    unittest.main()
