# Baseline validation checklist

**Baseline date:** 2026-07-18  
**Status:** passed  
**Next work package:** source audit, salvage, and licensing

This checklist is the acceptance record for the course baseline. It freezes the decisions needed to start implementation without leaving major pedagogical or technical questions implicit.

## Acceptance checks

| Check | Evidence | Result |
|---|---|---|
| Course identity and audience are defined | `course-contract.md`; `curriculum.yml` | Pass |
| Public course language is unambiguous | English-only mandate in `decisions.md` | Pass |
| Course scope and boundaries with neighbouring CSMI courses are defined | `decisions.md`; `curriculum.yml` | Pass |
| Learning outcomes are measurable | 11 outcomes in `course-contract.md` and `curriculum.yml` | Pass |
| Every concept has an importance level | 55 concepts classified P0–P3 in `curriculum.yml` | Pass |
| Every concept has an expected difficulty | 55 concepts classified D1–D3 in `curriculum.yml` | Pass |
| Contact-time envelope is feasible | 14 blocks × 2 hours = 28 contact hours | Pass |
| High-priority content is taught | All 44 P0/P1 concepts occur in the schedule | Pass |
| High-priority content is assessed | All 44 P0/P1 concepts map to at least one assessment | Pass |
| Assessment weighting is complete | A1 20% + A2 25% + A3 15% + A4 40% = 100% | Pass |
| Assessment modes and AI-use rules are explicit | `assessment-blueprint.md`; `decisions.md` | Pass |
| Semester datasets are selected and licensed | UCI 501, UCI 601, optional UCI 602; all CC BY 4.0 | Pass |
| Data packaging and offline-exam policy are defined | `datasets.md` | Pass |
| Public/private repository boundary is defined | `decisions.md` | Pass |
| Antora publication architecture is selected | Antora with `feelpp/antora-ui`; hybrid page/notebook sources | Pass |
| Reproducibility baseline is selected | Python 3.12, Ubuntu 24.04 LTS, CPU-first, `uv`, pinned Node dependencies | Pass |
| Ownership and change control are defined | Accountable roles and amendment policy in `decisions.md` | Pass |
| Machine-readable curriculum is internally consistent | YAML parse and reference validation completed on 2026-07-18 | Pass |

## Validation snapshot

The baseline consistency check returned:

```text
assessment_weight: 100
blocks: 14
contact_hours: 28
concepts: 55
outcomes: 11
p0_p1_concepts: 44
p0_p1_assessed: 44
p0_p1_scheduled: 44
errors: []
```

The validation checked unique concept identifiers; valid concept-to-outcome and concept-to-assessment references; valid schedule references; total assessment weight; contact-hour arithmetic; language metadata; and teaching and assessment coverage for every P0/P1 concept.

## Decisions that remain intentionally revisable

These are implementation details, not baseline blockers:

- the named people assigned to each accountable role;
- the exact academic-year calendar and control dates;
- the tested `feelpp/antora-ui` release selected during repository bootstrap;
- the final package lock after notebook conversion experiments;
- whether the P2 engine lab uses DuckDB, Polars, or a controlled comparison;
- which P2 topics are activated for a particular cohort.

Any change to the English-only policy, 28-hour envelope, assessment weights, P0/P1 classification, primary dataset, or public/private repository boundary requires a dated decision-record amendment and a matching update to `curriculum.yml`.
