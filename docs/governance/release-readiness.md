# Release readiness and approval

## Current state

The repository can build a deterministic student bundle, validate its manifest and public/private boundary, execute the complete notebook suite, build the Antora site, and publish both artifacts from a Git-tag workflow. The GitHub Pages workflow publishes `main`; immutable course bundles are attached to GitHub Releases.

The current state is **candidate tooling complete; human pilot and approval pending**. No `v0.9-pilot.N` or `v1.0-2026` tag is authorised by this technical record alone.

## Approval gates

|Gate |Evidence owner |Status |
|---|---|---|
|P0/P1 curriculum and mathematical review |Course lead and academic moderator |Pending named sign-off |
|Assessment equivalence and privacy boundary |Academic moderator and assessment custodian |Pending named sign-off |
|Accessibility and English review |Independent reviewer |Pending named sign-off |
|Colleague plus two representative-user pilot |Pilot coordinator |Pending physical/human execution |
|Dataset licence, checksum, and provenance audit |Data steward |Automated checks pass; annual human review pending |
|Fast and full clean-environment CI |Release workflow |Implemented |
|Student bundle manifest and private-content scan |Release workflow |Implemented |
|Site link, mathematics, landmark, and image checks |Release workflow |Implemented |

## Technical rehearsal — 2026-07-18

The integrated candidate completed `npm run release:prepare` locally:

- Ruff lint and formatting checks passed;
- 19 repository tests passed;
- the curriculum validator covered 55 concepts and 11 outcomes;
- 10 fast-profile and 18 full-profile notebooks executed successfully;
- 44 generated HTML pages passed link, mathematics, landmark, and image checks;
- the student bundle contained 86 manifest-verified files and no instructor, solution, hidden-test, private assessment, or course-operations path.

This rehearsal demonstrates technical readiness only. The immutable bundle checksum is recorded by the tagged release workflow after the human gates below are signed.

## Public-exercise rehearsal — 2026-07-23

The AsciiDoc-first specimen and student-notebook contract completed the full local gate:

- 21 Python tests and both AsciiDoc contract suites passed;
- repository validation covered 55 concepts, 11 outcomes, four public specimens, and 22 stable task IDs;
- 14 fast-profile and 22 full-profile notebooks executed successfully;
- 49 generated HTML pages passed notebook, link, mathematics, landmark, image, task-equivalence, and manifest checks;
- the student bundle contained 98 manifest-verified files, including four public specimen notebooks, and passed its private-path, private-tag, solution-free metadata, prompt-inventory, output-state, and checksum checks;
- the reusable `@feelpp/antora-extensions` exercise-metadata candidate passed all seven extension tests.

This additional rehearsal does not replace assessment-custodian review. The named academic, accessibility, ambiguity, boundary, retake, and lower-spec timing decisions remain pending.

## Optional-extension rehearsal — 2026-07-24

The optional-source and dependency-isolation contract completed the full local gate:

- 24 Python tests and both AsciiDoc contract suites passed;
- repository validation covered all seven P2 extension pages, four AsciiDoc/notebook sources, one notebook-native exception, and two page-only exceptions;
- 14 required fast-profile notebooks remained unchanged, while all 26 full-profile notebooks executed successfully;
- 49 generated HTML pages passed notebook, link, mathematics, landmark, image, extension-content, and manifest checks;
- kernel, calibration, tracking, and drift pages rendered real STEM blocks and semantic evidence tables; the three graphical lessons rendered accessible offline SVG results;
- the student bundle contained 102 manifest-verified files, including the four new generated extension notebooks and the notebook-native JAX artifact.

Optional dependencies remain confined to the locked `extensions` extra. No optional runtime is imported by a required P0/P1 source, and failure to install JAX or Polars does not block the 14-notebook required fast profile.

This rehearsal does not approve the optional mathematical exposition or ownership boundaries. Named academic, downstream-owner, accessibility, and representative-student review remain pending.

## Reproducibility qualification — 2026-07-25

The decommissioned AsciiDoc-first pipeline completed two consecutive full
preparations from empty `build/` and `public/` directories:

- all 26 Python tests and both AsciiDoc conversion/execution suites passed in
  each preparation;
- 14 required notebooks and all 26 public notebooks executed in each
  preparation;
- 49 course HTML pages passed local-link, document-language, accessibility
  structure, local-runtime, notebook-manifest, and executable-evidence checks;
- pinned KaTeX accepted all 779 rendered `stem` expressions;
- the release contained 25 AsciiDoc-generated notebooks and the one declared
  JAX notebook-native exception;
- the exact 102-file student bundle passed source-kind, output-state,
  solution-leak, private-boundary, inventory, and checksum validation;
- the full 237-file public tree, notebook manifest, student bundle, source
  fingerprint, and locked inputs matched across both preparations.

The resulting student bundle SHA-256 is
`2a2c0e872d42a61a9e83f97edfb948955837101fe10d9312c7f14a5d8816e081`;
the public-site tree SHA-256 is
`581261604217149d8b418826e3230fe157ea61355540577e02cf469290d1b88a`.
The machine-readable record is
`build/release/reproducibility-report.json`.

This local report identifies a dirty working tree through its source
fingerprint and therefore does not authorise a tag. A release candidate still
requires a clean committed checkout, successful GitHub checks, the
representative-user pilot, and every named approval.

## Version progression

The September revision and its remaining human gates are recorded in
[`teaching-candidate-20260905.md`](teaching-candidate-20260905.md). Use the current
commit's retained qualification report, rather than historical July counts or
checksums, when evaluating this candidate.

1. Approve a frozen commit and bundle checksum through the pilot protocol.
2. Create `v0.9-pilot.N`; the tag workflow reruns all checks and publishes immutable artifacts.
3. Record defects and corrections against the candidate commit.
4. Rerun affected pilot tasks and all automated checks.
5. Create `v1.0-2026` only after every required sign-off is recorded.

Tags are never moved or reused. A failed tagged build is corrected in a new candidate tag. Live assessment material remains outside the public release even after course publication.
