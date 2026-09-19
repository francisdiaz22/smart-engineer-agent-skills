# Suspicious pattern reference

These are static indicators for review, not proof of malicious intent. Interpret each indicator in context and record the file, trigger, behavior, severity, and confidence.

## Shell and interpreter execution

`bash`, `sh`, `zsh`, `cmd.exe`, `powershell`, `pwsh`, `node`, `python`, and other interpreters; `child_process`, `subprocess`, `os.system`, `Runtime.exec`, and `ProcessBuilder`.

## Download and remote content

`curl`, `wget`, `Invoke-WebRequest`, `Invoke-RestMethod`, remote scripts, package bootstrap commands, URLs, IP addresses, and upload or exfiltration calls.

## Dynamic execution

`eval`, `exec`, `node -e`, `python -c`, shell expansion, dynamically reconstructed commands, and runtime-loaded modules.

## Encoding and concealment

Base64, hex decoding, large encoded strings, compressed/encrypted blobs, dynamic string reconstruction, misleading extensions, hidden output, and commands that suppress prompts or reveal.

## Credential-related paths

`~/.ssh`, `~/.aws`, `~/.azure`, `.env`, `AppData`, `Library/Application Support`, credential stores, browser profiles, wallet files, tokens, cookies, and secret-management APIs.

## Persistence

Cron, systemd, scheduled tasks, launch agents, launch daemons, registry run keys, startup folders, shell profiles, login hooks, and workspace-open hooks.

## Editor and agent configuration

`.vscode/tasks.json`, `.vscode/settings.json`, `.vscode/launch.json`, `.vscode/extensions.json`, `AGENTS.md`, `CLAUDE.md`, `.mcp.json`, `.claude/`, and `.agents/`.
