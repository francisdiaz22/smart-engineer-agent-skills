# Security Policy

## Scope

This project provides documentation and skills for static repository security preflight reviews. It does not certify repositories as safe and does not replace sandboxing, code review, or organizational security controls.

## Reporting a vulnerability

Do not include secrets or live exploit payloads in a public issue. Report suspected vulnerabilities privately to the repository maintainers with a description, affected file or behavior, reproduction steps using inert data, and impact. If no private reporting channel is configured, open a minimal issue requesting one without including sensitive details.

## Fixture safety

Test fixtures must remain inert. Use reserved domains such as `example.invalid`, fake paths, and placeholder tokens. Never run fixture content as part of tests.
