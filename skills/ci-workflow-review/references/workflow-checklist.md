# CI Workflow Checklist

Use this checklist as static evidence gathering. Never trigger a workflow or run a copied step while reviewing it.

## Locations and reachability

Inspect `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/config.yml`, `azure-pipelines.yml`, `.buildkite/`, and documented equivalents. Record push, pull-request, merge-request, issue, comment, schedule, dispatch, tag, release, and reusable-workflow triggers.

Ask who can cause each job to run and whether the event includes contributor-controlled text or code.

## Privilege and runners

Review:

- token and repository permissions
- `pull_request_target` or equivalent privileged triggers
- self-hosted, shared, privileged, or containerized runners
- deployment environments and approval gates
- release, publish, infrastructure, and repository-write permissions

## Commands and dependencies

Review shell steps, scripts, action/plugin references, mutable tags, unpinned dependencies, package installation, remote downloads, generated commands, and event data interpolated into shell. Treat every command as text; do not run it.

## Secrets and artifacts

Check whether secrets can reach forks, pull requests, logs, artifacts, caches, build outputs, issue comments, or deployment commands. Check whether artifacts and caches cross branches or trust boundaries.

## Decision guidance

CI configuration is not proof of malicious intent. High-risk recommendations are appropriate when a reachable untrusted trigger combines with privilege, secrets, command execution, or release/deployment effects without strong scoping and approval.
