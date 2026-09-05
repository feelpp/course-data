# Representative-user pilot protocol

## Status

The technical rehearsal is automated. The human pilot remains pending until one colleague and two representative students or alumni complete the protocol and sign the release record. Automated execution must not be presented as human learning evidence.

## Participants and independence

- One colleague reviews academic coherence, English, accessibility, assessment validity, and the stated course boundary.
- One participant represents a mathematically strong student with less Python experience.
- One participant represents a student comfortable with Python and scientific computing.
- At least one participant uses the lower-spec supported machine profile or an equivalent two-core, 8 GiB CPU-only environment.
- Participants must not have authored the tested material.

Record only role, environment class, and relevant prior experience. Do not place names, email addresses, health information, or student identifiers in the repository.

## Candidate preparation

1. Freeze one candidate commit and build the student bundle from a clean checkout.
2. Record commit, bundle SHA-256, operating system, CPU/memory class, Python/Node versions, and start time.
3. Confirm that no participant has instructor sources, solutions, hidden tests, or live assessment material.
4. Give participants only the public website, student bundle, and the tasks below.

For the September revision, use the new public practice notebooks and original
synthetic data. A specimen notebook containing only the specification is not a
timed implementation task. Prepare the environment before starting an assessment
clock, and record installation time separately.

The course lead also rehearses the Monday application tour against its 20-minute
budget and the complete opening agenda against 120 minutes. Record actual elapsed
time and cuts in the opening-session record. This instructor rehearsal does not
replace the independent learner pilot.

## Tasks and evidence

|Task |Target evidence |Maximum diagnostic window |
|---|---|---:|
|Install from the published instructions |Environment succeeds without undocumented repair |30 min |
|Find P0/P1 meaning and the first foundation chapter |Navigation and terminology are understood |5 min |
|Learn one definition and worked example from a webpage |Participant explains the concept without instructor prompting |20 min |
|Run one foundation notebook from restart |All cells run; paths and task boundaries are clear |30 min |
|Complete one independent exercise |Reasoning and implementation instructions are sufficient |45 min |
|Interpret one uncertainty/error statement |Participant distinguishes estimate, uncertainty, and limitation |15 min |
|Use only keyboard for navigation and notebook execution |No mouse-only blocker |15 min |
|Locate glossary, feedback, rubric, and specimen |Student-facing support artifacts are discoverable |10 min |

Record active time, waiting time, first failure, recovery, unclear terms, environment issues, accessibility barriers, and unprompted misconceptions. Do not coach during the timed attempt; record the point at which help becomes necessary.

## Timed public assessment rehearsals

Use separate sittings after the prerequisite content has been learned. Do not
combine all three formats into a single pilot visit or treat prior exposure to
the public tasks as an unseen-exam timing observation.

|Public task |Prerequisites |Target elapsed time |Evidence |
|---|---|---:|---|
|Control 1 practice |Blocks 1–7 |70 min |Validated join, repairs, checks, protected baseline, interpretation |
|Control 2 practice |Blocks 1–13 |55 min |Evidence for defects, consequences, verified repairs, recommendation |
|Final practice |Blocks 1–14 |165 min |Audit, reasoning, implementation, evaluation and reproducibility |

Use `templates/assessment-rehearsal-observation.md` for actual elapsed and active
time, completed tasks, first ambiguity, help required, and the exported artifact.
A successful run of the supplied blank response notebook is a startup test only.
The observer checks whether the student's evidence meets the public rubric;
completeness messages are not correctness checks. Keep completed observation and
assessment records in the approved private location and publish aggregates only.

If a format overruns or requires undocumented help, reduce the task scope or
improve scaffolding, then repeat with an independent learner. Two learners expose
problems but do not establish a population timing distribution; retain slower
completions and support needs in the decision instead of relying on a median alone.

## Semester checkpoints

After the Monday opening, summarise exit-ticket misconceptions and setup barriers
before Block 2. After Blocks 4 and 9 compare actual contact, preparation and task
time with the published allocation. At Blocks 5, 7, 9 and 13 review mini-project
scope and per-student time logs. After each control review timing, ambiguous task
wording and rubric interpretation. Use the course retrospective template and link
each proposed change to evidence and a verification step. Publish only aggregates
large enough to preserve anonymity.

## Exit criteria

The candidate may advance only when:

- all three participants can install, navigate, learn from a page, and execute a notebook;
- no P0/P1 task depends on network access after preparation, a GPU, a personal service account, hidden state, colour alone, or mouse-only interaction;
- no unresolved severity-1 accessibility, privacy, licence, assessment-boundary, or correctness defect remains;
- median task time fits the declared duration, with documented accommodation for slower environments;
- unclear terms and recurring misconceptions are corrected or explicitly taught;
- the colleague signs academic, English, accessibility, and assessment-boundary review.

## Severity and decision

- **S1 Blocker:** prevents access, execution, correct learning, privacy, or assessment validity. Release stops.
- **S2 Major:** material confusion or repeated workaround. Correct and rerun the affected task.
- **S3 Minor:** local wording or presentation issue. Record before the annual teaching release.

The signed record names the candidate commit and bundle checksum, lists unresolved S3 items, and chooses reject, revise-and-rerun, or approve-candidate. A later content change invalidates approval when it changes a tested task, environment, assessment, or accessibility surface.
