# context-auditor (Offline Edition — root‑level workflow)

This package audits prompt & contextual-data changes **without external APIs**.  
The CI workflow file is now at the repo root (`context-auditor.yml`) for easy discovery.

## Setup
1. Copy everything into your repo root.
2. GitHub Actions will automatically pick up `context-auditor.yml`.

No keys, no outbound network calls—perfect for air‑gapped or strict OSS projects.