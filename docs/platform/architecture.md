# Publication architecture

## Source flow

```text
curriculum.yml ───────────────┐
                              ├─ repository validator
AsciiDoc concept pages ───────┤
                              ├─ Antora + feelpp/antora-ui ── public site
Instructor notebooks ─ generator ─ student notebooks ────────┘
                      └────────── instructor notebooks ─ notebook execution
Dataset SOURCE.yml + snapshots ─ checksum and licence validation
```

Antora uses the vendored `feelpp/antora-ui` v0.53 bundle. The collector extension injects generated student notebooks as component attachments without writing generated files into the source tree.

## Validation layers

The fast pull-request gate checks:

- Python linting and formatting;
- unit tests;
- curriculum totals and references;
- page and notebook metadata;
- English language metadata;
- dataset and UI checksums;
- raw/private content boundaries;
- deterministic student-notebook generation;
- fast instructor-notebook execution;
- Antora build and local-link integrity.

Scheduled validation runs the full notebook profile. GitHub Pages deployment rebuilds from the lockfiles and publishes only `public/`.

Python dependency upgrades are prepared with `uv lock --upgrade` and reviewed with the full notebook gate. Dependabot manages npm and commit-pinned GitHub Actions; it does not manage Python because pip-style updates do not maintain `uv.lock` consistently.
