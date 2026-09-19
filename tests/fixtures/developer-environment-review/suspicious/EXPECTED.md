# Expected result

- Status: `HIGH-RISK FINDINGS`
- Severity: high for privileged host integration and download-and-execute
- Confidence: high for the observed static configuration
- Recommended action: `DO NOT ENABLE OR LAUNCH`

Expected indicators include mutable image tags, privileged mode, Docker socket
access, secret-shaped environment keys, and reserved-domain downloads. Nothing
in this fixture is to be built, pulled, or started.
