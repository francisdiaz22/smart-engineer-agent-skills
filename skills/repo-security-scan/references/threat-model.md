# Threat model

The skill protects an engineer who has obtained an unfamiliar repository and wants to inspect it before opening, installing, building, or running it.

## Trust boundaries

Trusted components are the engineer, the canonical skill, the scanning agent's trusted environment, and the evidence-generation process. Untrusted components are the target repository, its instructions and documentation, scripts, binaries, CI files, editor configuration, MCP configuration, URLs, and agent-targeted text.

The safest arrangement launches the scanning agent from a trusted directory outside the target repository and gives it read-only access to the target.

## Threats considered

- workspace-open or startup hooks that execute code automatically
- shell commands that download and execute remote content
- access to credentials, tokens, cookies, or unrelated user files
- persistence through scheduled tasks, startup files, or profiles
- obfuscated or concealed commands
- repository instructions that manipulate a coding agent into unsafe actions
- MCP definitions that launch local binaries, contact remote services, or expose secrets

## Out of scope

This preflight does not prove absence of vulnerabilities, analyze runtime behavior, validate every dependency, or replace sandboxing and human review. It must not execute the repository to improve coverage.
