# Secrets Detection Guide

These are review patterns, not a credential validator. Keep matches redacted.

## High-signal formats

- PEM private-key blocks: `-----BEGIN ... PRIVATE KEY-----`
- cloud access key and secret-key assignments
- bearer tokens, basic-auth headers, and CI job tokens
- database URLs containing a username and password
- webhook URLs with embedded signing or authorization material
- JWT-like values (`header.payload.signature`) only when context indicates a credential
- assignments such as `API_KEY=`, `TOKEN=`, `PASSWORD=`, `CLIENT_SECRET=` with a non-placeholder value

## Context that lowers confidence

- `example`, `sample`, `test`, `dummy`, `placeholder`, or `redacted`
- reserved domains such as `example.invalid`
- public keys, checksums, lockfile integrity hashes, and non-secret identifiers
- values intentionally documented as fake in an inert fixture

## Files needing special care

`.env`, `.env.*`, CI workflows, deployment manifests, Docker/Kubernetes configuration, Terraform variables/state, cloud credentials, SSH directories, certificates, logs, database dumps, notebooks, archives, and generated frontend assets.

Do not rely on extensions alone. A secret can be stored in a source file, JSON, YAML, TOML, XML, Markdown example, or binary artifact.
