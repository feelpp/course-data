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
- 7 fast-profile and 15 full-profile notebooks executed successfully;
- 44 generated HTML pages passed link, mathematics, landmark, and image checks;
- the student bundle contained 86 manifest-verified files and no instructor, solution, hidden-test, private assessment, or course-operations path.

This rehearsal demonstrates technical readiness only. The immutable bundle checksum is recorded by the tagged release workflow after the human gates below are signed.

## Version progression

1. Approve a frozen commit and bundle checksum through the pilot protocol.
2. Create `v0.9-pilot.N`; the tag workflow reruns all checks and publishes immutable artifacts.
3. Record defects and corrections against the candidate commit.
4. Rerun affected pilot tasks and all automated checks.
5. Create `v1.0-2026` only after every required sign-off is recorded.

Tags are never moved or reused. A failed tagged build is corrected in a new candidate tag. Live assessment material remains outside the public release even after course publication.
