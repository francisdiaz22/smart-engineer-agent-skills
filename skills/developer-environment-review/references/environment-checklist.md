# Developer Environment Checklist

Review these fields without building, pulling, resolving, or starting anything.

| Area | Review indicators |
| --- | --- |
| Provenance | Mutable tags, unknown registries, remote Dockerfiles, unpinned images |
| Build | Remote contexts, `ADD`/`RUN` downloads, package installation, build secrets |
| Mounts | Host root, home directory, SSH directories, Docker socket, writable source mounts |
| Privilege | `privileged`, host networking, devices, added capabilities, root user |
| Secrets | Inline credentials, secret-to-environment mappings, broad environment passthrough |
| Startup | `entrypoint`, `command`, `postCreateCommand`, `onCreateCommand`, shell interpreters |
| Network | Exposed ports, unrestricted egress, proxy settings, remote bootstrap URLs |

These are review indicators, not proof of malicious intent. Verify provenance,
scope, trigger reachability, and least privilege manually.
