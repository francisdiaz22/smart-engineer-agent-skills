# MCP Configuration Checklist

Use this checklist as static evidence gathering. Never start a server while reviewing it.

## Configuration inventory

- `.mcp.json`
- `mcp.json`
- `.claude/settings.json`
- documented project or user configuration locations

For each server, record its name, command, arguments, working directory, transport, URL, environment variable names, and authentication method. Redact environment values and tokens.

## Command and source review

Review whether the command is:

- a repository-local script or binary
- a shell or interpreter such as `bash`, `sh`, `powershell`, `node`, or `python`
- a package runner or installer such as `npx`, `npm`, `pnpm`, `pip`, or `uv`
- downloaded, generated, mutable, or selected through an environment variable

Trace referenced files as text only. Do not execute them.

## Capability review

Check for:

- filesystem roots outside the intended workspace
- write access, deletion, or command execution tools
- network, proxy, browser, cloud, or credential-store access
- environment variables containing secret-shaped names
- authentication that has not been independently verified

## Decision guidance

Configuration is not proof of malicious intent. A server should remain disabled until its source, requested capabilities, trigger, and least-privilege settings are manually verified. Unknown remote endpoints, package installation at startup, broad access, and secret exposure justify a high-risk recommendation.
