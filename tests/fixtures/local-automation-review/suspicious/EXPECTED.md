# Expected result

- Status: `HIGH-RISK FINDINGS`
- Severity: high for install-time download and hook-path modification
- Confidence: high for the observed static configuration
- Recommended action: `DO NOT EXECUTE`

Expected indicators include a package lifecycle hook, a reserved-domain
download, and Git hook persistence. The hook file is inert text and must never
be installed or run.
