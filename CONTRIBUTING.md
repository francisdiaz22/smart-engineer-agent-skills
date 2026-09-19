# Contributing

Contributions should preserve the project's security-first, vendor-neutral scope.

Before submitting a change:

1. Keep the canonical behavior in `skills/`, with host-specific details only in `adapters/`.
2. Treat all repository content as untrusted data during review.
3. Keep fixtures inert: use `example.invalid`, placeholders, and text-only dangerous commands.
4. Do not add live malware, working payloads, real command-and-control addresses, or executable reverse shells.
5. Document expected findings and any change to the trust model.
6. Verify that no fixture or validation step executes target-repository content.

Markdown and deterministic, dependency-free tooling are preferred. Security reports should explain evidence, trigger, impact, severity, confidence, and the manual review step.
