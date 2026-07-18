# Platform validation record

**Validated:** 2026-07-18  
**Status:** pass

## Tested baseline

| Layer | Pin or result |
|---|---|
| Python | CPython 3.12.9; project contract 3.12 |
| Python resolver | `uv.lock`, 52 resolved packages |
| Node.js | 22.23.1 |
| npm | 10.9.8 |
| Antora CLI and generator | 3.1.15 |
| Antora collector | 1.0.3 |
| Feel++ Antora extensions | 1.0.0-rc.3 |
| Feel++ Asciidoctor extensions | 1.0.0-rc.15 |
| Feel++ UI | v0.53, vendored and checksum-pinned |
| Unit tests | 4 passed |
| Reference notebooks | 1 fast notebook executed successfully |
| Generated student notebooks | 1, output-free and solution-free |
| Rendered HTML pages | 9 |
| Curriculum register | 55 concepts and 11 outcomes validated |
| Dataset snapshots | 3 checksums and licences validated |
| High or critical npm advisories | 0 |
| Clean-clone reproduction | Pass from a local clone with fresh Python and Node installs |

## UI compatibility adjustments

The v0.53 bundle was tested rather than used through a moving `latest` URL. Two references to absent tab JavaScript files were removed through a supplemental `head-meta.hbs`; the bundle's `site.js` remains active. Footer policy links were changed to Antora page references and four English policy pages were added.

## Visual smoke test

The course home and data-lifecycle lab were inspected in a browser at a 1280×720 viewport. Navigation, breadcrumbs, table of contents, P0/D1 badges, typography, footer policy links, and the generated notebook attachment rendered correctly. The browser console reported no warnings or errors. The P0 badge computed to `rgb(139, 30, 30)` as specified by the supplemental stylesheet.

## Commands

```sh
uv sync --locked --all-groups
npm ci
npm audit --audit-level=high
npm run check
```

The same gate is used by pull-request CI. Scheduled validation executes the full notebook profile, and the Pages workflow rebuilds from both lockfiles before deployment.
