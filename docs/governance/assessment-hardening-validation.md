# Assessment hardening validation

**Validation date:** 2026-07-18

**Technical implementation:** complete

**Live-release approval:** pending human sign-off and physical lower-spec pilot

**Canonical public inventory:** `curriculum.yml` → `assessment_hardening`

## Delivered controls

The private assessment repository now provides deterministic generation and an offline operator workflow for two Control 1 variants, two Control 2 variants, and three final-examination dataset variants. The final set includes independently packaged main, retake, and reserve roles. All seven variants share fixed duration, points, importance, response schema, and operation contracts within their assessment.

Student bundles contain only an English brief, local data, a response template, a public structural checker, and a public manifest. Private reference answers, hidden checks, point keys, and safety-cap triggers are excluded. The machine rehearsal inspects every generated bundle for private paths and exercises the full accept, check, pseudonymous export, grade, and archive lifecycle.

## Grading and privacy controls

- Hidden checks produce a point-level record with pass, partial, or fail status rather than one all-or-nothing score.
- P0 leakage checks can activate a declared local safety cap; the grade record identifies the trigger without making runtime part of the score.
- Written reasoning points remain explicitly pending until human review.
- Submission export uses HMAC-SHA256 to create a stable pseudonymous candidate code and allow-lists only the response file.
- The assessment archive stores the candidate code, grade, and bundle/submission/grade checksums; direct identity remains in the approved university system.
- Bundles require no network, personal account, accelerator, or third-party service.

## Importance and fairness

Every required variant declares P0 Essential and P1 Core concept coverage. No P2 Extension or P3 Deferred content is required. Runtime is recorded only for operational support; fixed data and iteration budgets determine the workload, and wall-clock performance never determines marks.

The automated operational pilot passed on the current reference host and a single-thread restricted proxy. That evidence measures packaging, checking, export, grading, and archival, not student thinking time or a complete physical-room setup. A human pilot on the actual lower-spec student-machine profile remains a release gate.

## Verification evidence

Private repository checks currently establish:

- exact variant counts `2 / 2 / 3` and point equivalence;
- deterministic files and SHA-256 manifests;
- complete public/hidden separation in every bundle;
- successful reference grading for all seven variants;
- standalone package, submission, grading, and archive operation for the retake;
- pseudonymous, direct-identity-free archives;
- passing lint, unit tests, fresh-account rehearsal, and runtime evidence generation.

The public repository checks establish the inventory, English delivery page, permitted importance boundary, variant counts, offline requirements, and runtime fairness rule.

## Required human release gates

No specimen is a live examination until named reviewers sign the private record. Required decisions are independent academic moderation, English and ambiguity review, accessibility review, assessment-custodian boundary review, invigilator retake rehearsal, and a physical lower-spec timing pilot. Reviewers must record conditions, alternative accepted answers, and any rubric change before release.
