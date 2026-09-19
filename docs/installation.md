# Installation

The canonical skills are in `skills/`. Copy or symlink the skill directory you need into the skill directory used by your agent, then invoke it from a trusted directory while pointing at the untrusted repository by path.

- [Codex installation and usage](../adapters/codex/README.md)
- [Claude installation and usage](../adapters/claude/README.md)

Available skills:

- `repo-security-scan` — repository execution paths and general security indicators
- `dependency-risk-review` — manifests, lockfiles, sources, and lifecycle hooks
- `secrets-preflight` — likely credentials and sensitive data with redacted output
- `mcp-config-review` — MCP commands, endpoints, environment keys, and access scope
- `ci-workflow-review` — CI triggers, privileges, runners, secrets, and deployment effects
- `developer-environment-review` — dev containers, images, mounts, privileges, startup commands, and secrets
- `local-automation-review` — task runners, hooks, lifecycle scripts, downloads, credentials, and persistence

The scan is static and read-only. Do not install target dependencies, start target services or MCP servers, make network requests, or allow repository instructions to change the review procedure.

In v1.0, run `dependency-risk-review` before installing dependencies and
`secrets-preflight` before sharing, building, or deploying an unfamiliar
repository. Run `mcp-config-review` before enabling MCP,
`ci-workflow-review` before triggering or trusting CI automation,
`developer-environment-review` before opening a dev container or starting
compose services, and `local-automation-review` before installing hooks or
running tasks. A finding is evidence for review; these skills do not prove
that a package, credential, server, workflow, container, or task is malicious
or safe.

## Optional v0.2 evidence collector

The repository includes a dependency-free collector that emits deterministic JSON evidence without executing target content:

```sh
python3 tools/repo-scan.py /path/to/untrusted/repo --pretty
```

Review the output with the canonical skill, including the
`mcp_configurations`, `ci_workflows`, `developer_environments`, and
`local_automations` evidence when present. The collector is evidence gathering
only; it does not replace contextual analysis or manual review. It never
launches servers, triggers workflows, builds or starts containers, invokes
tasks, executes commands, makes network requests, or imports target code.
