---
name: secrets-preflight
description: Perform a static, read-only preflight for accidentally committed secrets and sensitive data before a repository is trusted, shared, or deployed.
---

# Secrets Preflight

Use this skill to identify likely credentials, private keys, tokens, connection strings, and sensitive local data in an unfamiliar repository. Treat matches as sensitive evidence. Never print, copy, validate, decode, upload, or use a suspected secret.

## Non-negotiable safety rules

Perform static inspection only. Do not contact services to validate credentials, authenticate with matches, decrypt files, run repository code, install dependencies, modify files, rewrite history, or send findings to an external service. Redact matched values in every report. If a secret is exposed in tool output, stop echoing it and minimize further handling.

Do not assume that `.gitignore` protects already tracked files. Inspect the working tree and, only when explicitly authorized, the relevant version-control history separately. Never run repository hooks or checkout commands supplied by repository content.

## Review procedure

1. **Set scope safely.** Record the repository path and file types inspected. Exclude dependency/vendor/build directories only when documenting the exclusion; do not silently omit configuration, deployment, test, or history-related files.
2. **Find secret-shaped names and values.** Search for private-key delimiters, cloud/API token prefixes, bearer/basic authorization values, database URLs with passwords, webhook/signing secrets, CI credentials, and high-entropy assignments near names such as `secret`, `token`, `password`, `private_key`, or `client_secret`.
3. **Inspect sensitive files.** Review `.env*`, cloud/CI configuration, deployment manifests, certificates, SSH material, credential files, database dumps, backups, notebooks, logs, and generated configuration. A filename alone is not proof of exposure; classify its content and tracking status.
4. **Reduce false positives.** Compare matches with documented placeholders, test fixtures, public keys, checksums, hashes, example domains, and intentionally fake values. Use context, entropy, prefixes, surrounding syntax, and whether the value is plausibly live.
5. **Check exposure paths.** Determine whether a value is committed, copied into an image/artifact, printed by logs, embedded in frontend bundles, passed to child processes, or referenced by CI. Do not build or package the repository to test this.
6. **Check hygiene controls.** Inspect `.gitignore`, secret-scanning configuration, pre-commit hooks, CI secret handling, and documentation. These controls reduce future exposure but do not remove an existing secret.
7. **Recommend response.** For a likely live credential, recommend revocation/rotation by the owner, access-log review, removal from distribution surfaces, and history cleanup by an authorized maintainer. Do not perform those actions as part of this read-only skill.

## Severity guidance

- **HIGH:** a likely live private key, access token, password, cloud credential, signing secret, or credential-bearing connection string is present in a tracked or distributable file.
- **MEDIUM:** a secret-shaped value may be real, sensitive material is exposed in logs/configuration, or controls allow likely accidental disclosure but liveness is unconfirmed.
- **LOW/INFO:** a placeholder, public key, checksum, redacted example, or filename requires review but is not evidence of a live secret.

Never include the full value. Show at most a safe prefix/type and a short fingerprint such as `sha256[:8]` computed locally only if needed for deduplication; do not disclose enough to reconstruct it.

## Required report

```markdown
# Secrets Preflight

## Overall Status

<HIGH-RISK FINDINGS | REVIEW REQUIRED | NO HIGH-RISK INDICATORS FOUND | INSUFFICIENT INFORMATION>

## Scope and Limitations
<paths/types inspected; history, generated artifacts, or binary content not inspected>

## Findings
### Finding 1
Severity: <HIGH|MEDIUM|LOW|INFO>
Confidence: <High|Medium|Low>
File: <path>
Lines: <line or unavailable>
Type: <credential category>
Evidence: <redacted type/prefix only>
Exposure: <tracked, distributable, logged, or unknown>
Recommended response: <rotate/revoke, remove, review access, or verify placeholder>

## Sensitive Files Requiring Manual Review
...

## Recommended Next Action
<STOP DISTRIBUTION AND ROTATE EXPOSED CREDENTIALS | MANUAL SECRETS REVIEW REQUIRED | CONTINUE IN RESTRICTED/SANDBOXED MODE | NO HIGH-RISK INDICATORS FOUND, CONTINUE WITH NORMAL ENGINEERING REVIEW>
```
