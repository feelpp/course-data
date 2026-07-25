# Bounded npm security exception

## Status

Active from 2026-07-22 and reviewed on every Antora dependency update.

## Scope

Antora `3.1.15` and Collector `1.0.3` require `js-yaml` version 4 APIs. The currently available fixed `js-yaml` release is `5.2.1`, whose schema and merge-type APIs are incompatible with this Antora release. An attempted transitive override fails before the playbook can be loaded. The audit tool's automatic remedy instead proposes an unsupported breaking downgrade to Antora `2.3.4`.

The temporary exception is restricted to these advisories:

- `GHSA-52cp-r559-cp3m`: quadratic CPU consumption through YAML merge-key chains;
- `GHSA-h67p-54hq-rp68`: repeated-alias quadratic complexity.

No other high or critical vulnerability is permitted by `npm run audit`. The audit script matches the package name, indirect-dependency status, severity, and exact advisory URLs; a new advisory fails the gate.

## Controls

- Course releases use reviewed repository YAML rather than runtime user-supplied YAML.
- GitHub build jobs have explicit time limits to bound resource consumption from malicious or accidental YAML.
- Pull requests remain untrusted input and receive no publishing credentials.
- The exception does not apply to a deployed service because YAML parsing occurs during the static build.
- The exception must be removed as soon as a stable compatible Antora release consumes a corrected parser.

This is a transparent compatibility exception, not evidence that the vulnerable parser has been repaired.
