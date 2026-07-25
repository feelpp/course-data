# Public exercises, assessment specimens, and variants

**Technical implementation:** complete

**Assessment-custodian approval:** pending human sign-off

**Canonical inventory:** `curriculum.yml` → `exercise_release`

## Decision

Public assessment specimens are AsciiDoc-first exercise documents. Antora publishes each source as an English webpage and `asciidoctor-jupyter` generates a solution-free student notebook from the same source. This removes a separate notebook copy that could drift from task wording, points, importance, allowed resources, AI mode, evidence, or rubric mapping.

The public set covers Control 1, the mini-project, Control 2, and the final examination. These are structural specimens and practice contracts, not current papers. Live variants, answer keys, hidden checks, point keys, embargoed data, and moderation records remain solely in the private `course-data-assessment` repository.

## Machine-readable contract

Every public specimen declares:

- assessment and exercise identifiers;
- stable task identifiers;
- per-task Essential (P0) and Core (P1) importance;
- per-task points whose sum equals the assessment total;
- hint policy;
- AI-assistance mode;
- closed allowed-resource inventory;
- required submission evidence;
- mapping to stable common-rubric criteria `R1`–`R7`.

The Antora extension copies this contract into `notebook.metadata.course.exercise`. Generated notebooks also declare `artifact_variant: student` and `solutions_included: false`. A Markdown cell containing one or more declared tasks receives the `exercise-prompt` tag and its exact task IDs. Generation fails if a declared task is absent from the notebook narrative, if task mappings are incomplete, or if a private cell tag is present.

## Hint boundary

Timed specimens use `specification-only`: students receive requirements, acceptance rules, point allocation, and numerical tolerances, but no task-specific solution path. The mini-project uses `public-checkpoints-and-rubric`: planning checkpoints and evidence expectations are available because they support a long-form learning process without disclosing an answer.

Any later practice hint must be explicitly labelled. A released hint may support reasoning, but it must not reproduce an answer from a live or embargoed task. Public AsciiDoc must never use conditionals to conceal committed private text.

## AI-assistance and evidence

- Mode A prohibits external generative AI and requires an assistance declaration. Examination, hidden-test, confidential, personal, or embargoed material must not be uploaded to an external service.
- Mode B permits external generative AI with disclosure and independent verification. The mini-project requires an `ai-notes` record or an explicit no-assistance declaration, plus individual verification.
- Mode C is reserved for work in which an AI system is itself an announced object of critique; it still requires disclosure and independent validation.

The assessment header is authoritative. The curriculum validator requires each specimen mode to match the corresponding assessment record. Allowed resources and submission evidence must match exactly between the curriculum and the AsciiDoc page header.

## Equivalence checks

Repository validation establishes that:

- one and only one public specimen contract exists for each assessment;
- task IDs are globally unique and appear in both metadata and visible prompts;
- task points equal the published total;
- required importance is limited to Essential (P0) and Core (P1);
- every task maps to a known common-rubric criterion;
- page AI mode, allowed resources, evidence, and hint policy match the curriculum;
- public specimen sources contain no solution or instructor-only markers.

Generated-site validation additionally establishes that:

- every expected webpage and notebook attachment exists;
- notebook and manifest metadata equal the curriculum contract;
- every declared task is present on the webpage and in tagged notebook prompt cells;
- notebook outputs and execution counts are empty;
- solution, instructor-only, and removal tags are absent;
- the deterministic notebook manifest exactly matches the curriculum inventory.

The student-bundle validator repeats the private-path, private-tag, solution-free metadata, prompt inventory, output-state, checksum, and required-specimen checks on the actual ZIP artifact.

## Variant fairness

The private repository owns generation and moderation for two Control 1 variants, two Control 2 variants, and three final-examination variants. Equivalent variants preserve duration, total points, task importance, operation sequence, response schema, tolerance policy, AI mode, allowed-resource profile, and rubric mapping. Context, data values, seeds, and surface wording may change only when the moderated cognitive demand remains equivalent.

The public contract does not certify a live paper. Before release, the assessment custodian must record independent academic moderation, ambiguity and English review, accessibility review, public/private boundary review, retake operation, and a lower-spec physical timing pilot in the private approval record.

## Remaining human gate

Automated validation can prove structural equivalence and absence of known private markers; it cannot approve academic validity, ambiguity, fairness to a particular cohort, or realistic completion time. The technical implementation is therefore complete while the assessment-custodian status remains `pending_human_signoff` in `curriculum.yml`.
