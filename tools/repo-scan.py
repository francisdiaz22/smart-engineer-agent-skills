#!/usr/bin/env python3
"""Deterministic, read-only repository security evidence collector.

This tool only reads files under the supplied repository root. It never imports,
executes, installs, or contacts anything from the target repository.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MAX_FILE_BYTES = 1_000_000
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}

URL_RE = re.compile(r"https?://[^\s\"'<>`]+")
PROMPT_RE = re.compile(
    r"(?:ignore|disregard|override)\s+(?:all\s+)?(?:previous|prior|earlier)\s+instructions?"
    r"|disable\s+(?:security|safety)\s+(?:checks|constraints)"
    r"|reveal\s+(?:secrets?|tokens?|credentials?)"
    r"|do\s+not\s+(?:tell|show|disclose)\s+the\s+user",
    re.IGNORECASE,
)

INDICATORS = [
    ("download", re.compile(r"\b(?:curl|wget|Invoke-WebRequest|Invoke-RestMethod)\b", re.I), "HIGH"),
    ("shell", re.compile(r"\b(?:bash|sh|zsh|cmd\.exe|powershell|pwsh)\b", re.I), "MEDIUM"),
    ("dynamic-execution", re.compile(r"\b(?:eval|exec|node\s+-e|python\s+-c|child_process|subprocess|os\.system|Runtime\.exec|ProcessBuilder)\b", re.I), "MEDIUM"),
    ("obfuscation", re.compile(r"\b(?:base64|frombase64string|hex\s+decod|encodedcommand)\b", re.I), "MEDIUM"),
    ("credential-access", re.compile(
        r"(?:~[/\\]\.ssh|~[/\\]\.aws|~[/\\]\.azure|(?:^|[/\\])\.env(?:$|[/\\])|"
        r"credential(?:s)?|browser\s+profile|cookies?|"
        r"(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|private[_-]?key|signing[_-]?secret)"
        r"\s*[:=]\s*(?![\"']?(?:replace[-_ ]?me|token[_-]?placeholder|redacted|dummy|example|sample)\b)[^\s,;]+)",
        re.I,
    ), "HIGH"),
    ("persistence", re.compile(r"\b(?:cron|systemd|scheduled\s+tasks?|launch\s+(?:agent|daemon)s?|registry\s+run\s+keys?|startup\s+folders?)\b", re.I), "HIGH"),
]

MCP_CONFIG_NAMES = {".mcp.json", "mcp.json"}
MCP_CONFIG_RELATIVE = {".claude/settings.json"}
CI_WORKFLOW_SUFFIXES = {".yml", ".yaml"}
CI_WORKFLOW_FILES = {
    ".gitlab-ci.yml",
    ".gitlab-ci.yaml",
    "azure-pipelines.yml",
    "azure-pipelines.yaml",
    ".circleci/config.yml",
    ".circleci/config.yaml",
}
SECRET_KEY_RE = re.compile(r"(?:secret|token|password|private[_-]?key|api[_-]?key|credential)", re.I)
MCP_COMMAND_RE = re.compile(r"(?:^|\s)(?:bash|sh|zsh|cmd(?:\.exe)?|powershell|pwsh|node|python(?:3)?|ruby|perl|java)(?:\s|$)", re.I)
PACKAGE_INSTALL_RE = re.compile(r"\b(?:npm|pnpm|yarn|pip|pip3|poetry|cargo|gem)\s+(?:install|add|exec)\b", re.I)
REMOTE_URL_RE = re.compile(r"https?://[^\s\"'<>`]+", re.I)
CI_SECRET_RE = re.compile(r"(?:\$\{\{\s*secrets\.|\$[A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|KEY)|secrets\.[A-Za-z0-9_-]+)", re.I)
DEV_CONFIG_NAMES = {
    "dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml",
}
DEV_CONFIG_RELATIVE = {".devcontainer/devcontainer.json"}
DEV_HIGH_RISK_RE = re.compile(
    r"(?:privileged\s*:\s*true|/var/run/docker\.sock|network_mode\s*:\s*host|--privileged|--cap-add|devices\s*:|ADD\s+https?://|RUN\s+.*(?:curl|wget|Invoke-WebRequest))",
    re.I,
)
DEV_SECRET_RE = re.compile(r"(?:password|token|secret|private[_-]?key|api[_-]?key|credential)", re.I)
DEV_STARTUP_RE = re.compile(r"(?:entrypoint|command|postCreateCommand|onCreateCommand|updateContentCommand|initializeCommand)\s*[:=]", re.I)
AUTOMATION_NAMES = {"makefile", "justfile", "taskfile.yml", "taskfile.yaml", "package.json", ".pre-commit-config.yaml", ".pre-commit-config.yml"}
AUTOMATION_DIRS = ("scripts/", ".husky/", ".git/hooks/")
LIFECYCLE_RE = re.compile(r"(?:preinstall|install|postinstall|prepare|prepublish)", re.I)
HOOK_RE = re.compile(r"(?:\.husky/|\.git/hooks/|pre-commit|post-merge|post-checkout|pre-push)", re.I)
AUTOMATION_HIGH_RE = re.compile(r"(?:curl|wget|Invoke-WebRequest|Invoke-RestMethod)\b|(?:eval|exec)\s|(?:~[/\\]\.ssh|~[/\\]\.aws|credential|token|cookie)", re.I)
PERSISTENCE_RE = re.compile(r"(?:git\s+config|core\.hooksPath|\.bashrc|\.zshrc|\.profile|launch\s+agent|cron|systemd)", re.I)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def finding(kind: str, severity: str, confidence: str, file: str, line: int | None, message: str, evidence: str) -> dict[str, Any]:
    return {
        "kind": kind,
        "severity": severity,
        "confidence": confidence,
        "file": file,
        "line": line,
        "message": message,
        "evidence": evidence,
    }


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for directory, dirnames, filenames in __import__("os").walk(root, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            path = Path(directory) / name
            if path.is_symlink():
                continue
            files.append(path)
    return sorted(files, key=lambda p: rel(root, p))


def is_mcp_config(relative: str, path: Path) -> bool:
    return path.name in MCP_CONFIG_NAMES or relative in MCP_CONFIG_RELATIVE


def is_ci_workflow(relative: str, path: Path) -> bool:
    if path.suffix.lower() not in CI_WORKFLOW_SUFFIXES:
        return False
    if relative.startswith(".github/workflows/"):
        return True
    if relative in CI_WORKFLOW_FILES:
        return True
    return relative.startswith(".buildkite/")


def add_line_findings(
    findings: list[dict[str, Any]],
    text: str,
    relative: str,
    pattern: re.Pattern[str],
    kind: str,
    severity: str,
    confidence: str,
    message: str,
) -> None:
    for match in pattern.finditer(text):
        findings.append(finding(kind, severity, confidence, relative, line_number(text, match.start()), message, match.group(0).strip()))


def collect_mcp_evidence(relative: str, text: str, findings: list[dict[str, Any]], commands: list[dict[str, Any]]) -> dict[str, Any]:
    servers: list[dict[str, Any]] = []
    try:
        document = json.loads(text)
    except json.JSONDecodeError:
        document = None

    if isinstance(document, dict):
        candidates = []
        for key in ("mcpServers", "servers"):
            value = document.get(key)
            if isinstance(value, dict):
                candidates.extend((str(name), config) for name, config in value.items())
        for name, config in candidates:
            if not isinstance(config, dict):
                continue
            server = {"name": name}
            for key in ("command", "args", "url", "transport", "env", "cwd"):
                if key in config:
                    server[key] = config[key]
            servers.append(server)

    if not servers:
        servers.append({"name": None, "configuration": "structured server definitions not parsed; inspect file manually"})

    findings.append(finding("mcp-config", "INFO", "High", relative, 1, "MCP configuration is present and requires static review; no server was launched", "server definitions present"))
    commands.append({"file": relative, "line": 1, "command": "MCP server definitions present; inspect command, args, URL, env, and access scope"})

    add_line_findings(findings, text, relative, PACKAGE_INSTALL_RE, "mcp-package-install", "HIGH", "High", "MCP startup configuration includes a package installation or package runner")
    for server in servers:
        command = str(server.get("command", ""))
        args = server.get("args", [])
        args_text = " ".join(str(arg) for arg in args) if isinstance(args, list) else str(args)
        if PACKAGE_INSTALL_RE.search(f"{command} {args_text}") or (command.lower() in {"npx", "npm", "pnpm", "yarn", "pip", "pip3", "poetry", "cargo", "gem"} and re.search(r"\b(?:install|add|exec)\b", args_text, re.I)):
            findings.append(finding("mcp-package-install", "HIGH", "High", relative, 1, "MCP startup configuration includes a package installation or package runner", f"{command} {args_text}".strip()))
        if MCP_COMMAND_RE.search(command) or command.lower() in {"bash", "sh", "zsh", "cmd", "cmd.exe", "powershell", "pwsh", "node", "python", "python3", "ruby", "perl", "java"}:
            findings.append(finding("mcp-command", "MEDIUM", "Medium", relative, 1, "MCP configuration invokes an interpreter or shell; inspect the referenced command and arguments", command))
        if command.startswith(("./", ".\\", "/", "\\")) or command.startswith("$"):
            findings.append(finding("mcp-local-executable", "MEDIUM", "Medium", relative, 1, "MCP configuration launches a repository-local or environment-selected executable", command))
    add_line_findings(findings, text, relative, MCP_COMMAND_RE, "mcp-command", "MEDIUM", "Medium", "MCP configuration invokes an interpreter or shell; inspect the referenced command and arguments")
    add_line_findings(findings, text, relative, REMOTE_URL_RE, "mcp-remote-endpoint", "MEDIUM", "Medium", "MCP configuration references a remote endpoint; verify ownership and transport security manually")
    add_line_findings(findings, text, relative, SECRET_KEY_RE, "mcp-secret-environment", "MEDIUM", "Medium", "MCP configuration contains a secret-shaped environment key; do not expand or disclose its value")
    add_line_findings(findings, text, relative, re.compile(r"(?:filesystem|file[_-]?system|read[_-]?write|root|network|proxy)", re.I), "mcp-access-scope", "MEDIUM", "Low", "MCP configuration contains an access-scope indicator requiring manual least-privilege review")
    return {"file": relative, "servers": servers}


def collect_ci_evidence(relative: str, text: str, findings: list[dict[str, Any]], commands: list[dict[str, Any]]) -> dict[str, Any]:
    triggers = re.findall(r"^[ \t]*(?:on|trigger|triggers|schedule|workflow_dispatch|pull_request_target|pull_request|push|repository_dispatch|issue_comment)[ \t]*:", text, re.I | re.MULTILINE)
    runners = re.findall(r"runs-on\s*:\s*([^\s#]+)|pool:\s*\n(?:\s+.*\n)*?\s*name:\s*([^\s#]+)", text, re.I)
    actions = re.findall(r"(?:uses|plugin)\s*:\s*([^\s#]+)", text, re.I)
    secret_refs = CI_SECRET_RE.findall(text)
    workflow = {"file": relative, "triggers": triggers, "runners": [next((part for part in item if part), "") for item in runners], "actions": actions, "secret_references": secret_refs}
    findings.append(finding("ci-workflow", "LOW", "High", relative, 1, "CI or automation workflow is present and requires static trigger and privilege review", "workflow configuration present"))
    commands.append({"file": relative, "line": 1, "command": "CI workflow present; inspect triggers, permissions, runners, steps, secrets, artifacts, and deployments"})

    patterns = [
        (re.compile(r"\bpull_request_target\b", re.I), "ci-privileged-trigger", "HIGH", "Workflow can run with privileged repository context for pull-request events"),
        (re.compile(r"(?:self-hosted|privileged|docker-in-docker)", re.I), "ci-runner-privilege", "HIGH", "Workflow references a privileged or self-hosted runner"),
        (re.compile(r"permissions\s*:\s*(?:write-all|\n(?:\s+[^\n]+:\s*write))", re.I), "ci-write-permission", "HIGH", "Workflow requests write-capable permissions; verify least privilege"),
        (re.compile(r"(?:curl|wget|Invoke-WebRequest|Invoke-RestMethod)\b", re.I), "ci-remote-download", "HIGH", "Workflow step includes a remote download utility"),
        (re.compile(r"(?:secrets\.|\$\{\{\s*secrets\.)", re.I), "ci-secret-reference", "MEDIUM", "Workflow references secrets; verify they cannot reach logs, artifacts, forks, or untrusted commands"),
        (re.compile(r"(?:upload-artifact|download-artifact|cache|artifacts?:)", re.I), "ci-artifact-cache", "MEDIUM", "Workflow transfers or caches artifacts; inspect trust boundaries and retention"),
        (re.compile(r"\buses\s*:\s*[^\n@]+@(?:main|master|latest|dev)\b", re.I), "ci-unpinned-action", "MEDIUM", "Workflow references a mutable third-party action ref; prefer a verified immutable commit"),
        (re.compile(r"(?:deploy|release|publish|production|prod)", re.I), "ci-deployment-effect", "MEDIUM", "Workflow appears to affect a release or deployment environment; verify approvals and permissions"),
        (re.compile(r"\b(?:run|script|command)\s*:\s*[^\n]*(?:github\.event|merge_request|pull_request|issue|comment)", re.I), "ci-untrusted-input", "HIGH", "Workflow may interpolate event-controlled input into a command; review quoting and validation"),
    ]
    for pattern, kind, severity, message in patterns:
        add_line_findings(findings, text, relative, pattern, kind, severity, "Medium", message)
    return workflow


def is_dev_environment(relative: str, path: Path) -> bool:
    name = path.name.lower()
    return name in DEV_CONFIG_NAMES or relative in DEV_CONFIG_RELATIVE or relative.startswith(".devcontainer/")


def is_local_automation(relative: str, path: Path) -> bool:
    return path.name.lower() in AUTOMATION_NAMES or any(relative.startswith(prefix) for prefix in AUTOMATION_DIRS)


def collect_developer_environment_evidence(relative: str, text: str, findings: list[dict[str, Any]], commands: list[dict[str, Any]]) -> dict[str, Any]:
    images = re.findall(r"(?:^|\n)\s*(?:image|FROM)\s*:?\s*([^\s#]+)", text, re.I)
    mounts = re.findall(r"(?:^|\n)\s*(?:-\s*)?(?:volumes?|mounts?)\s*:\s*([^\n]+)", text, re.I)
    startup = [match.group(0).strip() for match in DEV_STARTUP_RE.finditer(text)]
    environment = [match.group(0).strip() for match in DEV_SECRET_RE.finditer(text)]
    evidence = {
        "file": relative,
        "images": images,
        "mount_indicators": mounts,
        "startup_keys": startup,
        "secret_key_indicators": sorted(set(environment)),
    }
    findings.append(finding("developer-environment", "INFO", "High", relative, 1, "Container or development-environment configuration is present and requires static review", "configuration present"))
    commands.append({"file": relative, "line": 1, "command": "Inspect image provenance, build inputs, mounts, privileges, secrets, networking, and startup commands"})

    for pattern, kind, severity, message in (
        (DEV_HIGH_RISK_RE, "developer-environment-privilege", "HIGH", "Development-environment configuration contains a privileged, host-integrated, or download-and-execute capability"),
        (re.compile(r"(?:^|\n)\s*(?:image|FROM)\s*:?\s*[^\s#]+:(?:latest|main|master|dev)\b", re.I), "developer-environment-mutable-image", "MEDIUM", "Development environment references a mutable image tag; verify provenance and pinning manually"),
        (DEV_SECRET_RE, "developer-environment-secret", "MEDIUM", "Development-environment configuration contains a secret-shaped key; do not expand or disclose its value"),
        (re.compile(r"(?:/workspace|/workspaces?|/home|/Users|/root|source=|target=)[^\n]*", re.I), "developer-environment-mount", "MEDIUM", "Development-environment configuration references a host or broad filesystem mount; verify scope"),
    ):
        add_line_findings(findings, text, relative, pattern, kind, severity, "Medium", message)
    add_line_findings(findings, text, relative, re.compile(r"(?:curl|wget|Invoke-WebRequest|docker\s+login|apt-get\s+install|npm\s+install)\b", re.I), "developer-environment-bootstrap", "HIGH", "Medium", "Container or development-environment setup includes a download, authentication, or package-install step")
    for match in DEV_STARTUP_RE.finditer(text):
        commands.append({"file": relative, "line": line_number(text, match.start()), "command": match.group(0).strip()})
    return evidence


def collect_local_automation_evidence(relative: str, text: str, findings: list[dict[str, Any]], commands: list[dict[str, Any]]) -> dict[str, Any]:
    tasks = re.findall(r"^\s*([A-Za-z0-9_.:/@-]+)\s*:\s*(?:[^#\n]*)", text, re.MULTILINE)
    lifecycle_keys: list[str] = []
    if relative.endswith("package.json"):
        try:
            document = json.loads(text)
        except json.JSONDecodeError:
            document = None
        if isinstance(document, dict) and isinstance(document.get("scripts"), dict):
            lifecycle_keys = [str(key) for key in document["scripts"] if LIFECYCLE_RE.fullmatch(str(key))]
            tasks.extend(lifecycle_keys)
            for key, value in document["scripts"].items():
                commands.append({"file": relative, "line": 1, "command": f"{key}: {value}"})
    evidence = {"file": relative, "tasks": sorted(set(tasks)), "lifecycle_hooks": lifecycle_keys, "hook_indicators": bool(HOOK_RE.search(text))}
    findings.append(finding("local-automation", "INFO", "High", relative, 1, "Local automation configuration is present and requires static trigger review", "automation configuration present"))
    commands.append({"file": relative, "line": 1, "command": "Inspect triggers, lifecycle hooks, shell commands, downloads, credentials, and persistence"})

    if LIFECYCLE_RE.search(text):
        add_line_findings(findings, text, relative, LIFECYCLE_RE, "automation-lifecycle", "HIGH", "High", "Package-manager lifecycle configuration can execute repository-controlled commands during installation or preparation")
    if HOOK_RE.search(text):
        add_line_findings(findings, text, relative, HOOK_RE, "automation-hook", "MEDIUM", "High", "Repository-controlled hook or hook trigger requires static review before installation or invocation")
    if AUTOMATION_HIGH_RE.search(text):
        add_line_findings(findings, text, relative, AUTOMATION_HIGH_RE, "automation-high-risk-command", "HIGH", "Medium", "Local automation contains a download, dynamic execution, or credential-access indicator")
    if PERSISTENCE_RE.search(text):
        add_line_findings(findings, text, relative, PERSISTENCE_RE, "automation-persistence", "HIGH", "Medium", "Local automation may alter hooks, startup files, or other persistence points")
    add_line_findings(findings, text, relative, re.compile(r"(?:npm|pnpm|yarn|pip|poetry|cargo|gem)\s+(?:install|add|exec)\b", re.I), "automation-package-command", "MEDIUM", "Medium", "Local automation invokes a package manager; verify inputs and lifecycle effects before running")
    return evidence


def collect(root: Path) -> dict[str, Any]:
    files = iter_files(root)
    findings: list[dict[str, Any]] = []
    urls: list[dict[str, Any]] = []
    commands: list[dict[str, Any]] = []
    automatic_paths: list[dict[str, Any]] = []
    mcp_configurations: list[dict[str, Any]] = []
    ci_workflows: list[dict[str, Any]] = []
    developer_environments: list[dict[str, Any]] = []
    local_automations: list[dict[str, Any]] = []
    skipped_large: list[str] = []

    for path in files:
        relative = rel(root, path)
        text = read_text(path)
        if text is None:
            skipped_large.append(relative)
            continue

        for match in URL_RE.finditer(text):
            urls.append({"file": relative, "line": line_number(text, match.start()), "url": match.group(0).rstrip(".,;)")})

        for pattern_name, pattern, severity in INDICATORS:
            match = pattern.search(text)
            if match:
                findings.append(finding("indicator", severity, "Medium", relative, line_number(text, match.start()), f"{pattern_name} indicator requires review", match.group(0)))

        prompt = PROMPT_RE.search(text)
        if prompt:
            findings.append(finding("agent-instruction", "HIGH", "High", relative, line_number(text, prompt.start()), "Agent-targeted instruction attempts to weaken safeguards or expose sensitive data", prompt.group(0)))

        if path.name == "tasks.json" and relative.startswith(".vscode/"):
            try:
                document = json.loads(text)
            except json.JSONDecodeError as error:
                findings.append(finding("parse-error", "LOW", "High", relative, error.lineno, "Could not parse VS Code tasks configuration", str(error)))
                document = {}
            for task in document.get("tasks", []) if isinstance(document, dict) else []:
                if not isinstance(task, dict) or task.get("runOptions", {}).get("runOn") != "folderOpen":
                    continue
                command = task.get("command", "")
                args = task.get("args", [])
                command_text = " ".join([str(command), *(str(arg) for arg in args)]).strip()
                path_info = {"file": relative, "trigger": "folderOpen", "label": task.get("label"), "command": command_text}
                automatic_paths.append(path_info)
                run_on_offset = text.find('"runOn"')
                findings.append(finding("automatic-execution", "LOW", "High", relative, line_number(text, run_on_offset) if run_on_offset >= 0 else None, "VS Code task can execute automatically when the folder opens", command_text or "task command unavailable"))
                command_offset = text.find('"command"')
                commands.append({"file": relative, "line": line_number(text, command_offset) if command_offset >= 0 else None, "command": command_text})
                if str(task.get("presentation", {}).get("reveal", "")).lower() == "never":
                    reveal_offset = text.find('"reveal"')
                    findings.append(finding("concealment", "MEDIUM", "High", relative, line_number(text, reveal_offset) if reveal_offset >= 0 else None, "Task output is configured not to reveal automatically", "reveal: never"))

        if is_mcp_config(relative, path):
            mcp_configurations.append(collect_mcp_evidence(relative, text, findings, commands))

        if is_ci_workflow(relative, path):
            ci_workflows.append(collect_ci_evidence(relative, text, findings, commands))

        if is_dev_environment(relative, path):
            developer_environments.append(collect_developer_environment_evidence(relative, text, findings, commands))

        if is_local_automation(relative, path):
            local_automations.append(collect_local_automation_evidence(relative, text, findings, commands))

    high = sum(1 for item in findings if item["severity"] == "HIGH")
    medium = sum(1 for item in findings if item["severity"] == "MEDIUM")
    status = "HIGH-RISK FINDINGS" if high else "REVIEW REQUIRED" if medium else "NO HIGH-RISK INDICATORS FOUND"
    return {
        "schema_version": "0.2",
        "repository": str(root),
        "inventory": {"file_count": len(files), "files": [rel(root, path) for path in files], "skipped_large_files": skipped_large},
        "automatic_execution_paths": automatic_paths,
        "commands": commands,
        "external_indicators": urls,
        "mcp_configurations": mcp_configurations,
        "ci_workflows": ci_workflows,
        "developer_environments": developer_environments,
        "local_automations": local_automations,
        "findings": findings,
        "summary": {"high": high, "medium": medium, "status": status},
        "safety": {"read_only": True, "network_requests": False, "executed_repository_code": False},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect static security evidence from a repository without executing it.")
    parser.add_argument("repository", type=Path, help="Path to the repository to inspect")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()
    root = args.repository.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {args.repository}")
    json.dump(collect(root), sys.stdout, indent=2 if args.pretty else None, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
