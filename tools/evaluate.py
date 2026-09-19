#!/usr/bin/env python3
"""Run the inert, deterministic release evaluation corpus."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "tools" / "repo-scan.py"
CASES = ROOT / "tests" / "evaluations" / "cases.json"
FIXTURES = ROOT / "tests" / "fixtures"


def scan_fixture(source: Path) -> dict:
    # EXPECTED.md is evaluation metadata, not target-repository evidence.
    with tempfile.TemporaryDirectory(prefix="repo-scan-eval-") as directory:
        target = Path(directory) / source.name
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("EXPECTED.md"))
        result = subprocess.run(
            [sys.executable, str(SCANNER), str(target)],
            check=True,
            capture_output=True,
            text=True,
        )
    return json.loads(result.stdout)


def evaluate(case: dict) -> list[str]:
    fixture = FIXTURES / case["fixture"]
    errors: list[str] = []
    if not (fixture / "EXPECTED.md").is_file():
        return [f"{case['name']}: missing EXPECTED.md"]
    report = scan_fixture(fixture)
    prefix = case["name"]
    if report["summary"]["status"] != case["status"]:
        errors.append(f"{prefix}: status {report['summary']['status']!r} != {case['status']!r}")
    high = report["summary"]["high"]
    if "min_high" in case and high < case["min_high"]:
        errors.append(f"{prefix}: high findings {high} < {case['min_high']}")
    if "max_high" in case and high > case["max_high"]:
        errors.append(f"{prefix}: high findings {high} > {case['max_high']}")
    kinds = {item["kind"] for item in report["findings"]}
    for kind in case.get("required_kinds", []):
        if kind not in kinds:
            errors.append(f"{prefix}: missing finding kind {kind!r}")
    if report["safety"] != {"read_only": True, "network_requests": False, "executed_repository_code": False}:
        errors.append(f"{prefix}: safety contract changed: {report['safety']!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=CASES, help="Evaluation case manifest")
    args = parser.parse_args()
    manifest = json.loads(args.cases.read_text(encoding="utf-8"))
    errors = [error for case in manifest["cases"] for error in evaluate(case)]
    if errors:
        print("Evaluation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Evaluation passed: {len(manifest['cases'])} inert cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
