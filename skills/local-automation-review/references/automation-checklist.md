# Local Automation Checklist

| Area | Review indicators |
| --- | --- |
| Triggers | Checkout, commit, push, install, prepare, scheduled, or folder-open execution |
| Lifecycle | `preinstall`, `install`, `postinstall`, `prepare`, `prepublish` |
| Shell | `bash`, `sh`, PowerShell, `eval`, shell interpolation, hidden output |
| Downloads | `curl`, `wget`, package runners, remote scripts, mutable URLs |
| Credentials | SSH, cloud credentials, tokens, cookies, environment passthrough |
| Persistence | Git hooks, Git config, shell profiles, startup files, scheduled jobs |
| Reachability | Who or what can invoke the task and whether a dependency is implicit |

A keyword is an indicator for contextual review, not proof of malicious intent.
