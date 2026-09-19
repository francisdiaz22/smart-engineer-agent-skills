# Fixture policy

Fixtures are inert text used to document expected static analysis. They must never be executed, installed, or contacted. Dangerous-looking commands use placeholders and reserved domains such as `example.invalid`.

The v0.4 fixture groups cover MCP configuration and CI workflows. The v0.5
fixture groups cover development environments and local automation. Their
configuration files are evidence only: do not launch an MCP server, trigger a
workflow, build or start a container, install an action or hook, expand a
secret, run a task, or contact a referenced URL.

Every safe and suspicious fixture includes `EXPECTED.md`. Evaluation inputs
must remain inert, use reserved domains and placeholders, and test contextual
review rather than keyword matching alone. The collector and test harness must
never execute fixture content.
