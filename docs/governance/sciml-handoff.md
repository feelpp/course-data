# Scientific Machine Learning hand-off

## Ownership decision

Data Processing publishes one compact P2 JAX bridge covering arrays, pure functions, explicit random keys, automatic differentiation with finite-difference verification, JIT compilation boundaries, and `vmap`. It does not publish a second machine-learning course under an optional label.

The following legacy families remain in the restricted source archive and are proposed to Scientific Machine Learning 1 or later specialist material. They are not student dependencies for this repository.

| Legacy family | Useful evidence to preserve | Downstream owner | Required rewrite before reuse |
|---|---|---|---|
| PyTree notebook | Container/tree reasoning and transformation patterns | Scientific Machine Learning 1 | Current English API examples, pure interfaces, small tests |
| Manual and Optax training notebooks | Batching, update functions, optimiser state | Scientific Machine Learning 1 | Remove bespoke framework, state assumptions, CPU oracle, current Optax API |
| Hyperparameter agent | Search persistence and experiment lineage ideas | Project / Scientific Machine Learning | Replace custom agent with leakage-safe nested selection and an interoperable run record |
| Sentiment and MNIST notebooks | Error-analysis and multiclass visualisation fragments | Scientific Machine Learning / specialist ML | Resolve dataset licences, remove live downloads, shrink runtime, write original tasks |
| Two-dimensional neural studies | Decision-boundary visual reasoning | Scientific Machine Learning | Consolidate duplication and separate visual diagnosis from architecture mechanics |
| Deep architectures | Normalisation, residual, and multi-branch ideas | Specialist deep learning | Establish provenance/licensing and rebuild with current small examples |
| Distributed or multi-device material | Scaling questions only | High Performance Computing / Scientific Machine Learning | Add communication, memory, topology, profiling, and reproducible hardware records |

## Entry contract supplied by this course

Students entering Scientific Machine Learning should already be able to reason about shapes/dtypes, stable losses, data provenance, leakage-safe splits, baselines, metrics, error analysis, deterministic tests, and result limitations. The optional JAX bridge adds transformation vocabulary but is not assumed unless the downstream course announces it.

## Archive and publication rule

The raw source ZIP remains ignored and checksum-addressed. A downstream maintainer may extract it into a temporary review directory, but publication requires an original English rewrite, source/licence decision, current dependency lock, deterministic CPU reference run, solution-free student variant, and explicit downstream concept IDs. Restricted PDFs and unclear third-party notebook prose are not redistributed.
