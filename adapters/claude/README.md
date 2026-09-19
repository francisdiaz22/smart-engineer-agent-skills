# Claude adapter

Use the canonical skill from this repository rather than maintaining a second implementation. For a user-scoped installation of the repository scan:

```sh
mkdir -p ~/.claude/skills/repo-security-scan
cp /absolute/path/to/smart-engineer-agent-skills/skills/repo-security-scan/SKILL.md ~/.claude/skills/repo-security-scan/
cp -R /absolute/path/to/smart-engineer-agent-skills/skills/repo-security-scan/references ~/.claude/skills/repo-security-scan/
```

Install the remaining v1.0 skills the same way:

```sh
for skill in dependency-risk-review secrets-preflight mcp-config-review ci-workflow-review developer-environment-review local-automation-review; do
  mkdir -p "$HOME/.claude/skills/$skill"
  cp /absolute/path/to/smart-engineer-agent-skills/skills/$skill/SKILL.md "$HOME/.claude/skills/$skill/"
  cp -R /absolute/path/to/smart-engineer-agent-skills/skills/$skill/references "$HOME/.claude/skills/$skill/"
done
```

A project-scoped installation may use the equivalent `.claude/skills/repo-security-scan/` path in a trusted project. Keep the target under review separate from the project that supplies the skill.

Example:

```text
Use repo-security-scan to inspect /path/to/untrusted/repo.
Static review only. Do not run repository-controlled commands, install dependencies, make network requests, or start MCP servers.
```

Use `dependency-risk-review` before dependency installation, `secrets-preflight` before sharing or deploying the repository, `mcp-config-review` before enabling MCP, `ci-workflow-review` before triggering or trusting CI automation, `developer-environment-review` before opening a dev container or starting compose, and `local-automation-review` before installing hooks or running tasks. Keep the review agent in a trusted directory outside the target repository.
