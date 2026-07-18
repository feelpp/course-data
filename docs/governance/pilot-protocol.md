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
