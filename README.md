# Smart Engineer Agent Skills

Reusable, security-first Agent Skills for software engineers using Codex, Claude Code, and compatible coding agents.

## Skills

### `repo-security-scan`

`repo-security-scan` performs a static, read-only security preflight of an unfamiliar source repository before you trust, install, build, or execute it. It helps identify automatic execution paths, suspicious commands, downloads, credential access, persistence, MCP configuration, and instructions aimed at coding agents.

The target repository is untrusted input. Repository files are evidence to analyze, never instructions that override the engineer, the agent, or the canonical skill.

Recommended workflow:

```text
CLONE
  ↓
ISOLATE
  ↓
READ-ONLY AGENT SCAN
  ↓
MANUAL REVIEW
  ↓
OPEN RESTRICTED
  ↓
UNDERSTAND
  ↓
TRUST
  ↓
RUN
```

The flagship v0.1 scenario is `.vscode/tasks.json`, especially tasks using `"runOn": "folderOpen"`. Such a task is an automatic execution path, not proof of malware; the command and referenced files require contextual review.

## Scope and non-goals

The first release is static inspection only. It does not execute repository code, install dependencies, start containers or MCP servers, run lifecycle scripts, make network requests, or modify the target repository. It is a preflight review, not proof that a repository is harmless.

See the [security model](docs/security-model.md), [installation guide](docs/installation.md), and [implementation plan](docs/PLAN.md).

### v0.3 review skills

- `dependency-risk-review` statically reviews manifests, lockfiles, dependency sources, and install-time hooks before packages are installed.
- `secrets-preflight` statically reviews likely credentials and sensitive data, with redacted reporting and rotation guidance.

Both skills are read-only and vendor-neutral. They do not validate packages or credentials over the network, and they do not replace manual review.

### v0.4 review skills

- `mcp-config-review` statically reviews MCP server commands, URLs, environment keys, and requested filesystem/network capabilities before a server is enabled.
- `ci-workflow-review` statically reviews CI triggers, permissions, runners, actions, secrets, artifacts, and deployment effects before a workflow is trusted or triggered.

Both v0.4 skills treat configuration as untrusted input. They never launch MCP servers, trigger CI, install actions or dependencies, contact referenced URLs, or expand secrets.

### v0.5 review skills

- `developer-environment-review` statically reviews dev containers, Dockerfiles, compose files, images, mounts, privileges, startup commands, and secret or network exposure before a development environment is enabled.
- `local-automation-review` statically reviews task runners, hooks, package lifecycle scripts, shell commands, downloads, credential access, and persistence before local automation is run.

Both v0.5 skills are read-only. They never build or start containers, pull images, install hooks or dependencies, invoke task runners, execute lifecycle scripts, contact registries or URLs, or expand secrets. v0.5 also defines inert automated evaluation fixtures so contextual findings can be regression-tested without executing fixture content.

## Repository layout

- `skills/` — canonical, vendor-neutral skills and references
- `adapters/` — host-specific installation and usage notes
- `tests/fixtures/` — inert examples used to validate expected analysis
- `docs/` — security, installation, and authoring documentation

## License

Apache-2.0. See [LICENSE](LICENSE).
