#!/usr/bin/env python3
"""Audit release fixtures for accidental execution or live-target material."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
URL_RE = re.compile(r"https?://([^/\s\"'<>`]+)", re.I)
FORBIDDEN_MARKERS = ("-----BEGIN PRIVATE KEY-----", "-----BEGIN RSA PRIVATE KEY-----")


def main() -> int:
    errors: list[str] = []
    expected_count = 0
    for path in sorted(FIXTURES.rglob("*")):
        if path.is_symlink():
            errors.append(f"symlink fixture: {path.relative_to(ROOT)}")
            continue
        if path.is_dir():
            continue
        relative = path.relative_to(ROOT)
        if path.name == "EXPECTED.md":
            expected_count += 1
        if path.stat().st_mode & 0o111:
            errors.append(f"executable fixture: {relative}")
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                errors.append(f"private-key marker in fixture: {relative}")
        for host in URL_RE.findall(text):
            if not host.lower().endswith(".invalid") and host.lower() not in {"localhost", "127.0.0.1"}:
                errors.append(f"non-reserved URL host {host!r} in fixture: {relative}")

    fixture_pairs = [
        path for path in FIXTURES.iterdir()
        if path.is_dir() and all((path / variant / "EXPECTED.md").is_file() for variant in ("safe", "suspicious"))
    ]
    if expected_count != len(fixture_pairs) * 2:
        errors.append("every safe/suspicious fixture pair must have EXPECTED.md")
    if errors:
        print("Fixture audit failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Fixture audit passed: {expected_count} expected-output files; no executable or live-target fixture material found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
