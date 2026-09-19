# Expected CI Workflow Review

Status: `HIGH-RISK FINDINGS`

Expected findings:

- HIGH: `pull_request_target` provides a privileged pull-request trigger.
- HIGH: A self-hosted runner is used.
- HIGH: The workflow requests write-all permissions.
- HIGH: A remote helper is downloaded and piped to a shell.
- MEDIUM: A release secret is referenced by a publish step.
- MEDIUM: An artifact is uploaded and the workflow appears to affect production.
- MEDIUM: The third-party checkout reference is mutable (`@main`).

Recommended action: `DO NOT TRIGGER OR TRUST THE WORKFLOW`

This fixture is inert text. The endpoint uses the reserved `.invalid` domain;
the workflow must never be triggered and the command must never be run.
