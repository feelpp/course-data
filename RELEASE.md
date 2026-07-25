# Release procedure

The website is continuously published from `main`. Immutable student and site bundles are published only from an approved Git tag.

## Candidate preparation

1. Freeze a commit and run `npm run release:qualify` from a clean checkout.
2. Review `build/release/reproducibility-report.json` and record the ZIP checksum
   from `build/release/course-data-student-bundle.zip.sha256`.
3. Complete the representative-user pilot and every gate in `templates/release-approval.md`.
4. Correct defects, rerun affected human tasks, and repeat the full automated preparation.
5. Obtain the named approval record outside the public repository.

## Publication

Candidate tags use `v0.9-pilot.N`; the approved annual release uses `v1.0-2026`. Create an annotated tag only for the exact approved commit:

```sh
git tag -a v0.9-pilot.1 -m "CSMI course pilot candidate 1"
git push origin v0.9-pilot.1
```

The tag workflow installs the locked environments, compares two complete clean
release builds, packages the site, validates the student bundle, computes
checksums, and creates the GitHub Release. Never move or reuse a published tag.

## Rollback and correction

If a tagged build fails or a release defect is found, keep the tag and artifacts for audit, document the defect, correct it on a new commit, and use a new candidate tag. Live assessment material and named review records never enter the public release.
