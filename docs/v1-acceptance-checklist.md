# v1.0 Acceptance Checklist

This is the release gate for the stable Engineer Security Skills Pack. A check
is complete only when the command or review evidence is available in the
release commit.

## Scope and documentation

- [x] All canonical skills have metadata, vendor-neutral instructions, static-only constraints, required reports, and bounded limitations.
- [x] README, installation docs, adapters, threat model, fixture policy, and security policy describe the v1 scope consistently.
- [x] No document claims that a repository is safe; conclusions use the documented limited-status language.

## Collector and evaluation

- [x] `python3 -m unittest discover -s tests -v` passes.
- [x] `python3 tools/evaluate.py` passes every case in `tests/evaluations/cases.json`.
- [x] Safe cases have zero high findings; suspicious cases have the required high-signal evidence.
- [x] Every evaluation report preserves `schema_version: "0.2"` and the read-only/no-network/no-execution safety contract.
- [x] Malformed configuration is bounded and does not execute, import, install, or contact anything.

## CI and release automation

- [x] CI runs the unit suite, deterministic evaluation harness, and fixture audit on supported Python versions.
- [x] CI workflow permissions are read-only and third-party actions are pinned to immutable commits.
- [x] Release checks do not run repository fixture commands, install project dependencies, or contact fixture URLs.

## Security and fixture audit

- [x] `python3 tools/release-audit.py` passes.
- [x] Fixtures contain no executable files, symlinks, private-key markers, live-target URLs, usable credentials, or malware payloads.
- [x] Suspicious commands remain inert text and use reserved domains/placeholders only.
- [x] Final working-tree diff has been reviewed for secrets, destructive samples, and unexpected generated files.

## Release decision

- [x] Full tests, evaluation, and audit pass from the release candidate checkout.
- [x] Known limitations are documented in the plan, skills, and review references.
- [x] The v1.0 commit is created and annotated with tag `v1.0.0`.
