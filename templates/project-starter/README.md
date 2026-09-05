# CSMI mini-project starter

Available from Block 5. Copy this folder into your assigned private Classroom
repository, including `.github/`, `.python-version`, and the lock file. The
starter provides an executable input contract and CI. You must add the scientific
question, approved data, analysis, evidence, and tests required by the project
specification. The supplied toy test is not evidence for an assessed method.

## First clean run

Use CPython 3.12 and `uv`, then run from this folder:

```sh
uv sync --locked --all-groups
uv run python -m src.analysis
uv run ruff check src tests
uv run pytest
```

The workflow runs the same commands on each push and pull request. Dependencies
must be installed before working offline. No account, network, or GPU is needed
by the example itself. The environment retains the course's required analytical
packages so the approved project routes have one shared starting point.

## Replace the toy example

1. State one question, unit of analysis, intended use and non-goal in this README.
2. Add the approved dataset ID, attribution, licence, checksum and datasheet.
3. Keep raw inputs separate from reproducible derived artifacts. Put reusable
   transformations in `src/`; notebooks call them rather than hiding state.
4. Define a split or stability design and an appropriate baseline. Add your own
   identity, semantic, toy-oracle and end-to-end checks. Supplied checks only
   cover the toy input and do not validate the scientific workflow.
5. Complete the course result-card and AI-notes templates. Report failures,
   variation, limitations, runtime, and the exact assessed commit.
6. Check out that commit afresh and run the documented commands before tagging.

The toy CSV is original synthetic course data under CC-BY-4.0, attributable to
CSMI Data Processing and Mining course contributors (2026). Its two rows have
no scientific interpretation. Starter code is under the repository's MIT code
licence; carry the course licence files into your project and record the separate
licence of your selected dataset.

The project has a 10-hour outside-class budget **per student**, plus the scheduled
clinic. Keep a time log and report a likely overrun at a checkpoint so the scope
can be reduced. Individual verification uses separate 5–8 minute appointments.
