# v0.5 Evaluation Corpus

The v0.5 evaluation corpus is composed of the safe and suspicious fixture
directories under:

- `tests/fixtures/developer-environment-review/`
- `tests/fixtures/local-automation-review/`

Each variant contains `EXPECTED.md` with the expected status, severity,
confidence, and recommended action. The corpus intentionally includes benign
near-misses (ordinary images, ports, task definitions, and shell-like text)
alongside high-risk capabilities such as privileged host integration and
install-time downloads.

Run the deterministic evaluation harness from the repository root:

```text
python3 tools/evaluate.py
python3 -m unittest discover -s tests -v
python3 tools/release-audit.py
```

The harness reads `cases.json`, invokes only `tools/repo-scan.py` against a
temporary copy of each fixture with `EXPECTED.md` removed, and compares the
expected status, evidence categories, and safety metadata without starting a
container, invoking a task, installing a hook, importing repository code,
contacting a URL, or expanding a secret.

`release-audit.py` separately checks that fixture files are non-executable,
non-symlinked, contain no private-key markers, and reference only reserved
fixture hosts.

When adding a case, use `example.invalid`, `TOKEN_PLACEHOLDER`, fake paths, and
text-only commands. Document accepted false positives and uncertainty in the
case's `EXPECTED.md`; do not require a binary verdict where the evidence only
supports manual review.
