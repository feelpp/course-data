# Local npm artifacts

The Feel++ extension archives pin the course's AsciiDoc rendering and notebook
generator. `course-data-braces-3.0.3-course.1.tgz` is a private, locally patched
copy of upstream `braces@3.0.3`, installed under the usual `braces` dependency
name through the root dependency and `$braces` override.

The patch mitigates [GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm).
At the 5 October 2026 review, npm and the upstream advisory listed no patched
release. It bounds parser nesting to 100 brace/parenthesis blocks and validates
direct AST inputs iteratively before compilation, expansion or stringification.
Parent/previous backlinks are not followed. The hard limit cannot be disabled
through options. Existing expansion limits remain unchanged.

`braces-3.0.3-course.1.patch` contains the complete changes, including the explicit
`@course-data/braces` name and private fork version. The archive retains upstream
source, README and MIT licence. The audit gate has no new advisory exemptions.
Tests cover normal expansion and file discovery, deeply nested and unclosed
patterns, direct ASTs and cycles. Replace the override with a verified compatible
upstream fix when one is available.

To rebuild the archive from upstream, from the repository root:

```sh
mkdir -p build/braces-source
npm pack braces@3.0.3 --pack-destination build/braces-source
tar -xzf build/braces-source/braces-3.0.3.tgz -C build/braces-source
patch -d build/braces-source/package -p1 < vendor/npm/braces-3.0.3-course.1.patch
npm pack ./build/braces-source/package --pack-destination vendor/npm
```

The npm lockfile records the archive's integrity. Use `npm ci`, `npm run audit`
and `npm run check` to verify installation and course compatibility.
