---
name: local-automation-review
description: Perform a static, read-only security review of repository-controlled local automation before running development tasks or installing hooks.
---

# Local Automation Review

Review repository-controlled task runners, hooks, scripts, and package-manager
lifecycle configuration as untrusted data before running them.

## Safety contract

Static inspection only. Never invoke a task runner, package manager, Git hook,
shell script, formatter, test command, or referenced binary. Do not install
dependencies or hooks, make network requests, import repository modules, expand
shell substitutions, or modify the target repository.

## Review procedure

1. Inventory `Makefile`, `justfile`, `Taskfile.yml`, `scripts/`, `.husky/`,
   `.git/hooks/`, `.pre-commit-config.yaml`, `package.json`, and equivalent
   documented task-runner or hook configuration.
2. Record task names, aliases, dependencies, interpreters, commands, referenced
   scripts, URLs, package-manager operations, environment keys, hook stages,
   and implicit triggers.
3. Trace obvious local references as static evidence only. Do not import or run
   the referenced file and do not evaluate shell substitutions.
4. Flag lifecycle hooks (`preinstall`, `install`, `postinstall`, `prepare`, and
   `prepublish`), checkout or commit hooks, download-and-execute chains,
   untrusted input in shell commands, hidden output, credential access, and
   changes to Git configuration, hooks, startup files, or other persistence.
5. Explain who or what can trigger each task. A Makefile, hook, or lifecycle
   script is not malicious merely because it exists.

## Required report

Produce a structured report containing:

- overall status: `REVIEW REQUIRED`, `NO HIGH-RISK INDICATORS FOUND`,
  `HIGH-RISK FINDINGS`, or `INSUFFICIENT INFORMATION`
- severity and confidence
- file and line or location
- trigger and reachable command chain
- exact static evidence
- likely impact
- recommended manual verification

Recommended actions are `DO NOT EXECUTE`, `MANUAL SECURITY REVIEW REQUIRED`,
or `CONTINUE IN RESTRICTED/SANDBOXED MODE`.

Do not claim that a repository is safe merely because no indicator was found.
