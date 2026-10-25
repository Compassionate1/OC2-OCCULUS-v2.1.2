# Repository protection activation

**Manual GitHub owner actions required:** Replace CODEOWNERS placeholders with an authorized team/user. Configure repository rulesets for default branch: pull request required, at least one independent review, CODEOWNERS review, conversation resolution, no force pushes/deletions, required checks (Python, Swift, BOM, integration), and signed-tag release policy. Configure secret scanning and Dependabot alerts, restrict Actions permissions, protect production environments with reviewers, and require OIDC provenance attestation verification. Do not enable public visibility until data rights and information-handling review is complete.

**Verification:** Record screenshot or GitHub API response for rulesets, repository visibility, workflow execution, branch restrictions, artifact attestation, and release tag. Local packaging is not publication.
