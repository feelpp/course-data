# Course and assessment blueprint validation

**Decision date:** 2026-07-18  
**Status:** approved for content production  
**Canonical source:** `curriculum.yml`, schema version 2

## Completion decision

The fourteen-block course, entry diagnostic, practice sequence, assessments, public specimens, rubric, runtime limits, numerical tolerances, and hardware assumptions are fixed. Repository validation rejects a change that leaves required material untaught, unpractised, or unassessed.

The binding curriculum contains 23 P0 concepts, 21 P1 concepts, 6 P2 concepts, and 5 P3 concepts. All 44 P0/P1 concepts are scheduled, attached to a concrete learning activity with acceptance criteria, and mapped to at least one assessment. P2/P3 concepts have no required assessment mapping.

## Required-outcome evidence

| Outcome | Importance | Taught in blocks | Practised in activities | Assessed in |
|---|---:|---|---|---|
| LO1 Question, unit, stakeholders, risks | P0 | 1, 4 | E01, E04 | A1, A2, A3, A4 |
| LO2 Provenance, schema, quality, privacy | P0 | 1, 2, 3, 4, 12 | E01, E02, E03, E04, E12 | A1, A2, A3, A4 |
| LO3 Validated tabular transformation | P0 | 1, 2, 3 | E01, E02, E03 | A1, A2, A3, A4 |
| LO4 Reproducible EDA and visualisation | P0 | 3, 4 | E03, E04 | A1, A2, A3, A4 |
| LO5 Leakage-safe pipelines | P0 | 3, 5, 8, 13, 14 | E03, E05, E08, E13, E14 | A1, A2, A3, A4 |
| LO6 Evaluation, metrics, uncertainty, failures | P0 | 4–10, 13, 14 | E04–E10, E13, E14 | A1, A2, A3, A4 |
| LO7 Supervised and unsupervised methods | P1 | 6–10, 13 | E06–E10, E13 | A2, A3, A4 |
| LO8 Complexity, memory and storage | P1 | 1, 6, 10, 11 | E01, E06, E10, E11 | A2, A3, A4 |
| LO9 Tests and clean execution | P0 | 1, 3, 5, 12, 13 | E01, E03, E05, E12, E13 | A1, A2, A3, A4 |
| LO10 Documentation, limitations, AI declaration | P0 | 1, 9, 12, 14 | E01, E09, E12, E14 | A1, A2, A3, A4 |

LO11 is a P2 downstream bridge. It may appear in the optional Block 14 demonstration but is deliberately absent from required assessment evidence.

## Assessment artifacts

| Artifact | Public contract | Private production record |
|---|---|---|
| Control 1 | `assessment/control-1-specimen.adoc` | reference outline, hidden-test plan, moderation checklist |
| Mini-project | `assessment/mini-project.adoc` | verification prompts and moderation record |
| Control 2 | `assessment/overview.adoc` | defect bank, variants, reference repairs |
| Final exam | `assessment/final-exam-specimen.adoc` | answer outline, tolerance plan, variants, moderation checklist |
| Common rubric | `assessment/rubric.adoc` | point-to-test mapping per live paper |

## Technical contract

- Reference target: CPython 3.12, Ubuntu 24.04 LTS, two CPU cores, 8 GiB RAM, no required accelerator.
- Required peak memory: at most 4 GiB.
- Fast CI: 5 minutes; full CI: 30 minutes; ordinary student notebook: 10 minutes.
- Final reference run: 15 minutes; prepared student compute path: 8 minutes.
- Exact checks for identity, schema, counts, joins, and deterministic labels.
- Default deterministic floating tolerance: relative `1e-7`, absolute `1e-10`.
- Seeded metric tolerance: absolute `0.01`; explicitly stochastic comparison: absolute `0.02` with a stated repetition or uncertainty design.
- Wall-clock speed is not graded; fixed data and iteration budgets are used.

## Diagnostic decision

The 35-minute readiness check covers environment, core Python, NumPy arrays, tabular reasoning, and mathematical notation. The general threshold is 75%; environment evidence requires full completion. Each domain has a 45–120 minute targeted route, repeat evidence, and instructor/teaching-assistant escalation before Block 3 when needed.

## Automated gates

`tools/validate_repository.py` and `tests/test_curriculum.py` enforce:

- exactly fourteen sequential two-hour blocks;
- valid concept, outcome, dataset, activity, prerequisite, and assessment references;
- prerequisites taught in an earlier block;
- complete P0/P1 teaching, practice, and assessment coverage;
- equality between assessment outcome declarations and concept mappings;
- no required P2/P3 assessment content;
- valid diagnostic routes and positive execution budgets;
- public specification presence and English page metadata.

This record authorises production of the P0 course material. It does not authorise publication of current solutions, hidden tests, or live examination material.
