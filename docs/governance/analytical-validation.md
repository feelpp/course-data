# P1 analytical-core validation

**Validation date:** 2026-07-18  
**Implementation status:** complete  
**Canonical inventory:** `curriculum.yml` → `analytical_release`

## Delivered core

| Family | P1 concept coverage | English page/notebook | Independent evidence | Private bank ID |
|---|---|---|---|---|
| Stable/probabilistic regression | `DP-LIN-01`, `DP-PROB-01`, `DP-NUM-01` | `linear-probabilistic` | Chronological air-quality solver/residual transfer | `QB-LIN-01` |
| Classification losses | `DP-CLS-01`, `DP-THR-01` plus probability/stability | `classification-losses` | Imbalanced multiclass metric/loss transfer | `QB-CLS-01` |
| Regularisation/generalisation | `DP-REG-01`, `DP-GEN-01`, `DP-CV-01` | `regularisation-generalisation` | Cross-seed coefficient/learning-curve transfer | `QB-REG-01` |
| Validation/search/features | `DP-CV-01`, `DP-SEARCH-01`, `DP-FEAT-01` | `model-selection` | Chronological search with fitted feature selection | `QB-CV-01` |
| Tree ensembles | `DP-TREE-01`, `DP-ENS-01`, `DP-ENS-02`, `DP-INT-01` | `tree-ensembles` | Sample/importance/error instability transfer | `QB-TREE-01` |
| PCA/clustering | `DP-PCA-01`, `DP-CLU-01`, `DP-CLU-02`, `DP-CLU-03` | `pca-clustering` | Geometry and bootstrap/seed challenge | `QB-CLU-01` |
| Columnar performance | `DP-PERF-01`, `DP-FMT-01`, `DP-SQL-01` | `performance-columnar` | Memory-bounded projected/query transfer | `QB-PERF-01` |

The union covers all 21 P1 concepts. Each page contains a guided laboratory, explicit independent transfer, assumptions/failure modes, and assessment evidence. Each canonical notebook has a tagged reference solution, public checks, deterministic cell IDs, P1 metadata, and the full CPU execution profile.

## Data and dependency evidence

- Dry Bean is generated deterministically from the reviewed UCI 602 ARFF snapshot into a 13,611-row UTF-8 CSV with CC BY 4.0 datasheet and SHA-256 manifest.
- UCI 501 and UCI 601 teaching tables remain the scientific/industrial regression, classification, and performance cases.
- Synthetic oracles use fixed generators/seeds for conditioning, softmax overflow, regularisation, grouped leakage, and cluster geometry.
- `scipy`, `pyarrow`, and `duckdb` are exact dependencies in the locked Python environment; P1 remains CPU-only.
- Performance assertions check result equality, projection, size, and bounded claims; they do not grade noisy wall-clock speed.

## Project and examination alignment

The public mini-project specification provides four P1 routes: stable regression, classification/ensembles, PCA/clustering, and performance-aware processing. Every route requires a P0 baseline and a validity challenge. The private question bank contains seven point/time/variant/tolerance records with the IDs above. The public final specimen selects announced P1 method families without depending on P2/P3 material.

## Automated gates

Repository validation rejects:

- a missing P1 page, notebook, teaching manifest, project specification, or final specification;
- a P1 concept absent from the declared inventory, page metadata, or notebook metadata;
- an analytical page without both guided and independent-transfer evidence;
- an analytical notebook outside the P1/full-CPU contract;
- duplicated or incomplete question-bank identifiers;
- nondeterministic generated notebook cell IDs;
- source/data checksum, public/private boundary, or learner-language failures.

Current implementation evidence:

- 13 repository, curriculum, release-inventory, data, and notebook-generation tests pass;
- 7 P0 notebooks execute in the fast CPU profile;
- all 14 P0/P1 notebooks execute in the full CPU profile;
- 14 solution-free student notebooks are generated;
- 31 Antora HTML pages build and pass generated-site link/asset checks.

Current live examination content, solutions, hidden tests, variants, and detailed marking keys remain in the private assessment repository.
