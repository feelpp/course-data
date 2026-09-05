# Bounded npm security exception

## Status

Retired on 2026-09-05. No high or critical advisory is exempted by the audit gate.

The fixed 4.x parser is now available. A scoped npm override resolves consumers
of `js-yaml` 4.x to `4.3.2`, preserving their major-version API while fixing the
merge-key and ordered-map advisories. The override does not replace consumers
of other major versions. Reconsider it when all upstream 4.x dependency ranges
admit a patched release. The lock also updates PostCSS's `nanoid` dependency
to `3.3.18`, within its existing compatible range.

References: [ordered-map advisory](https://github.com/advisories/GHSA-5p4m-2wfm-xmqj)
and [nanoid advisory](https://github.com/advisories/GHSA-2v37-7h3g-55p8).

`npm run audit` fails for any high or critical finding and for an incomplete or
failed audit response. Normal and full course checks verify parser compatibility;
the absence of an advisory alone does not establish build compatibility.

## Historical scope (22 July–5 September 2026)

Antora `3.1.15` and Collector `1.0.3` require `js-yaml` version 4 APIs. At the July review, the available fixed `js-yaml` release was `5.2.1`, whose schema and merge-type APIs were incompatible with that Antora release. An attempted transitive override failed before the playbook could be loaded. The audit tool's automatic remedy instead proposed an unsupported breaking downgrade to Antora `2.3.4`.

The temporary exception was restricted to these advisories:

- `GHSA-52cp-r559-cp3m`: quadratic CPU consumption through YAML merge-key chains;
- `GHSA-h67p-54hq-rp68`: repeated-alias quadratic complexity.

The historical audit script matched the package name, indirect-dependency status,
severity, and exact advisory URLs; a new advisory failed the gate. Its exception
has now been removed.

## Historical controls

- Course releases use reviewed repository YAML rather than runtime user-supplied YAML.
- GitHub build jobs have explicit time limits to bound resource consumption from malicious or accidental YAML.
- Pull requests remain untrusted input and receive no publishing credentials.
- The exception does not apply to a deployed service because YAML parsing occurs during the static build.
- The exception must be removed as soon as a stable compatible Antora release consumes a corrected parser.

These controls documented the temporary compatibility exception; the current
gate instead requires patched dependencies and has no advisory allowlist.
