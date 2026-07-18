# Optional enrichment validation

**Validation date:** 2026-07-18

**Implementation status:** complete

**Assessment status:** excluded

**Canonical inventory:** `curriculum.yml` → `enrichment_release`

## Delivered material

| Route | Importance | Artifact | Boundary |
|---|---|---|---|
| JAX arrays, PRNG, autodiff, JIT, `vmap` | P2 | English page and tested CPU notebook | No PyTrees, Optax, neural networks, accelerators, or large training |
| Kernel methods | P2 | Original Kernel Ridge/SVM bridge | No redistribution of the restricted legacy PDF |
| Probability calibration | P2 depth on a P1 concept | Reliability, proper scores, safe calibration design | Does not replace split, leakage, or shift checks |
| DuckDB and Polars | P2 | Correctness-first local engine comparison | No distributed-engine or database-theory claim |
| Experiment tracking | P2 | Local, account-free run record | No cloud service or full deployment orchestration |
| Drift and monitoring | P2 | Data/prediction/label/concept change framework | Alerts do not automatically trigger retraining |
| Downstream map | P2/P3 boundary | SciML, HPC, Database, and Project hand-offs | P3 material remains outside assessment |

## Core isolation

The enrichment inventory declares zero required contact hours, no assessed concepts, and a separate dependency extra. Foundation and analytical release inventories contain no extension path. Normal `uv sync --locked --all-groups`, pull-request CI, and the fourteen P0/P1 notebooks do not install or import JAX or Polars.

The scheduled/release full-notebook workflow installs the `extensions` extra and executes the additional JAX notebook on CPU. Removing the extension pages, notebook, builder, and optional dependency extra leaves the complete 28-hour schedule, four assessments, all P0/P1 concepts, and fourteen core notebooks intact.

## Source decisions

The new JAX notebook is an original compact synthesis informed by the reviewed legacy array and autodiff topics. It uses current pure-function, explicit-key, gradient-check, compilation-boundary, and vectorisation practice. The SciML hand-off record keeps PyTrees, custom training/Optax agents, sentiment/MNIST, and deep architectures out of this course.

Kernel notes are original and cite authorised official documentation; the legacy all-rights-reserved PDF is not distributed. The engine, calibration, tracking, and drift pages use local or synthetic data contracts and require no live service or personal account.

## Automated gates

Repository validation rejects a missing enrichment artifact, a P2 page marked as assessed, a mismatch with the complete P2 concept set, an extension notebook outside the P2/full CPU contract, or any P2/P3 assessment mapping. Notebook generation removes the JAX solution cells, and the full profile executes its public checks with the locked optional environment.
