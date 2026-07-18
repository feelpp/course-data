# Security policy

Report a suspected vulnerability privately to the course maintainers or through the Cemosis security contact. Do not publish credentials, personal data, private assessments, or a working exploit in a public issue.

## Build-input policy

Antora playbooks, component descriptors, notebook sources, and dataset metadata are reviewed repository inputs. Pull requests from untrusted contributors must not be built with write credentials or access to private assessment repositories.

CI fails when `npm audit` reports a high or critical advisory. On 2026-07-18, npm reported eight moderate dependency paths, all originating from Antora and the collector extension using `js-yaml` 4.1.1. The advisory concerns quadratic merge-key processing. The repository does not accept untrusted YAML at runtime, and the site build runs without deployment credentials on pull requests. This exception must be removed when a compatible Antora dependency resolves the advisory.

Python dependencies are fully locked. Dataset and UI archives are verified by SHA-256 before use. Generated output is never executed as a deployment script.

