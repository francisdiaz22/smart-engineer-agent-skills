# Expected analysis

- **HIGH:** automatic execution triggered by folder open.
- **HIGH:** PowerShell attempts an external download with `Invoke-WebRequest`.
- **MEDIUM:** task output is configured with `reveal: never`.
- **INFO:** external endpoint detected: `https://example.invalid/payload`.

Overall status: `HIGH-RISK FINDINGS`.

Recommended action: `DO NOT EXECUTE`.

This fixture is inert text. The endpoint uses the reserved `.invalid` domain and must never be contacted.
