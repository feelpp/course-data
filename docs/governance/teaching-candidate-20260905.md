# September teaching candidate

The September review led to separate maintenance, opening-session, progression,
learning-experiment and public-practice changes. The local review and plan remain
in `docs/analysis/`; public delivery is tracked in
[roadmap #26](https://github.com/feelpp/course-data/issues/26).

## Finding disposition

|Finding |Implemented response |Remaining observation or review |
|---|---|---|
|F1: preprocessing outside CV folds |Whole-pipeline search with ordinary Ridge/Lasso and a fold-row regression test |Independent academic review |
|F2: overloaded timetable |Fourteen explicit 120-minute blocks, minimum refresher, separate preparation and verification |Instructor timetable confirmation and learner timing |
|F3: promised experiments missing |Executable penalty path, learning curve, repeated-sample decomposition and group-safe feature/model search |Independent interpretation and academic review |
|F4: label-informed clustering described as discovery |Prescribed class-balanced benchmark plus controlled geometry comparisons |Learners distinguish oracle agreement from scientific discovery |
|F5: specification-only practice |Three independent runnable rehearsals, synthetic inputs, response cells and completeness export |Observed 70-, 55- and 165-minute rehearsals and ambiguity review |
|F6: project workload and verification unclear |Ten hours per student outside class, tested starter, checkpoints and separate individual appointments |Actual cohort staffing and observed workload |
|F7: starting route out of date |Four-application opening page, CSMI connections, first audit and current notebook inventory |Instructor rehearses the application tour and opening agenda |

The opening examples are labelled teaching schematics. Actual research results
and shareable application visuals remain the course lead's choice. No colleague
archive, historical solution or research dataset is part of the public release.
Optional JAX and other SciML preparation remain outside the required contact time.

## Frozen technical evidence

Run `npm run release:qualify` from a clean committed checkout, or dispatch
**Full notebook check** with `qualify=true` against the selected commit. The
workflow retains `teaching-candidate-evidence`, containing the student bundle and
`reproducibility-report.json`. That report identifies the exact commit, source
fingerprint, locked inputs, notebook/site inventories and bundle checksum, and
requires two identical clean preparations. A dirty or build-mutated checkout is
rejected before it can be reported as qualified.

Both preparations execute the fast and full notebook profiles, repository tests,
site and mathematics checks, and the bundle publication-boundary checks. The
September public inventory includes 28 AsciiDoc-generated notebooks and one
declared JAX notebook-native exception; the fast profile remains 14 notebooks.
Check the retained report for the actual counts and hashes of its commit.
Local browser inspection checks figure and task presentation in addition to the
automated structural checks; it is not an independent accessibility sign-off.

## Human decisions still pending

The course lead's opening rehearsal, colleague plus two-learner pilot, timed
assessment attempts, lower-spec and accessibility observations, academic review,
data review and assessment-custodian decisions remain open in
[pilot tracker #32](https://github.com/feelpp/course-data/issues/32). Blank forms
are available in `templates/pilot-observation.md`,
`templates/assessment-rehearsal-observation.md` and
`templates/course-retrospective.md`. Completed identifiable or assessment records
belong in the approved private location; publish only anonymous aggregates.

Monday exit tickets and the later teaching checkpoints cannot be completed before
those classes occur. A green technical candidate does not authorise the annual
release tag. Follow `docs/governance/release-readiness.md` after the dated named
decisions have been recorded.
