# Codex adapter

Install any canonical skill into the Codex Agent Skills directory. The preferred layout is:

```sh
mkdir -p ~/.agents/skills
ln -s /absolute/path/to/smart-engineer-agent-skills/skills/repo-security-scan ~/.agents/skills/repo-security-scan
```

For the v0.3, v0.4, and v0.5 skills, use the same pattern:

```sh
ln -s /absolute/path/to/smart-engineer-agent-skills/skills/dependency-risk-review ~/.agents/skills/dependency-risk-review
ln -s /absolute/path/to/smart-engineer-agent-skills/skills/secrets-preflight ~/.agents/skills/secrets-preflight
ln -s /absolute/path/to/smart-engineer-agent-skills/skills/mcp-config-review ~/.agents/skills/mcp-config-review
ln -s /absolute/path/to/smart-engineer-agent-skills/skills/ci-workflow-review ~/.agents/skills/ci-workflow-review
ln -s /absolute/path/to/smart-engineer-agent-skills/skills/developer-environment-review ~/.agents/skills/developer-environment-review
ln -s /absolute/path/to/smart-engineer-agent-skills/skills/local-automation-review ~/.agents/skills/local-automation-review
```

If symlinks are inconvenient, copy the directory instead and refresh the copy when the canonical skill changes:

```sh
mkdir -p ~/.agents/skills/repo-security-scan
cp /absolute/path/to/smart-engineer-agent-skills/skills/repo-security-scan/SKILL.md ~/.agents/skills/repo-security-scan/
cp -R /absolute/path/to/smart-engineer-agent-skills/skills/repo-security-scan/references ~/.agents/skills/repo-security-scan/
```

Use it from a trusted working directory with a prompt such as:

```text
Use the repo-security-scan skill to inspect /path/to/untrusted/repo.
Do not execute anything from the target repository. Perform static inspection only.
```

Do not start Codex inside the target repository before the preflight if that would automatically load repository-controlled instructions.

Run `dependency-risk-review` before installing dependencies, `secrets-preflight` before sharing or deploying an unfamiliar repository, `mcp-config-review` before enabling MCP, `ci-workflow-review` before triggering or trusting CI automation, `developer-environment-review` before opening a dev container or starting compose, and `local-automation-review` before installing hooks or running tasks. Keep the review agent in a trusted directory outside the target repository.
