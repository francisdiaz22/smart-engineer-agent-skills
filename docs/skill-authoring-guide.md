# Skill authoring guide

Keep skills small, explicit, and portable across compatible coding agents.

1. Put reusable behavior in a canonical `skills/<name>/SKILL.md`.
2. Begin with metadata containing a precise name and trigger description.
3. State safety boundaries before procedural steps.
4. Treat external files, tool output, and repository instructions as untrusted data when the skill processes them.
5. Keep host-specific installation and invocation details in `adapters/`.
6. Use references for threat models, pattern catalogs, and checklists rather than duplicating core behavior.
7. Provide inert fixtures and expected outcomes for security-sensitive behavior.
8. Avoid claiming completeness or absolute safety; explain uncertainty and manual review steps.
