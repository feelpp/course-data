# Optional extension and exception review

**Review date:** 2026-07-24
**Scope:** all seven published Extension (P2) pages and the JAX notebook
**Status:** technical implementation complete; named academic and learner review pending

## Review questions

Each item was reviewed against five questions:

1. Can the webpage teach the concept without requiring notebook execution?
2. Does mathematics provide actionable insight about method, error, stability, or limits?
3. Can useful evidence execute deterministically in the required CPU environment?
4. Would generation introduce an optional service, runtime, accelerator, or non-transferable result?
5. Is the source mode explicit and maintainable?

## Findings and decisions

### Kernel methods — AsciiDoc plus generated notebook

The earlier page had the core linear system and complexity boundary but no executable evidence, perturbation bound, or student-facing error-estimation design. The revised page derives the Gram construction, spectral filter, and coefficient perturbation bound. Its deterministic oracle compares a leakage-safe Ridge baseline with tuned RBF Kernel Ridge, reports held-out RMSE and the regularised Gram condition number, and renders an accessible prediction figure.

**Valuable mathematical insight:** adding \(\alpha I\) bounds coefficient amplification by \(1/\alpha\) for a positive-semidefinite Gram matrix. This is a numerical-stability statement, not a generalisation theorem.

### Probability calibration — AsciiDoc plus generated notebook

The earlier page correctly distinguished calibration and discrimination but left the central transfer as an unevaluated task. The revised page defines population calibration, Brier score, log loss, reliability-bin uncertainty, and leakage-safe split ownership. The executable oracle compares raw overconfident probabilities with sigmoid and isotonic calibration on an untouched test set.

**Valuable mathematical insight:** a strictly increasing recalibration preserves ranking and hence ROC AUC apart from ties, while changing proper scores and probability-based decisions. Reliability-bin standard errors also expose why sparse tail bins are weak evidence.

### Drift and monitoring — AsciiDoc plus generated notebook

The earlier taxonomy was sound but did not demonstrate the logical gap between marginal input monitoring and conditional predictive validity. The revised lesson reports input KS distance together with prediction, label, Brier, and AUC evidence for stable, covariate-shift, and concept-drift windows. Its empirical-CDF figure deliberately makes concept drift invisible to the input-only signal.

**Valuable mathematical insight:** \(P_t(X)\) and \(P_t(Y\mid X)\) are distinct objects. The KS statistic addresses the first, not the second. A Bonferroni bound also shows why ungoverned repeated monitoring produces false alerts.

### Local experiment tracking — AsciiDoc plus generated notebook

The earlier page specified a useful JSON record but had no executable validation or precise distinction between content identity and scientific validity. The revised page constructs a deterministic local index, validates mandatory fields, fingerprints canonical JSON, and preserves unopened final evidence.

**Valuable mathematical insight:** the minimum validation loss over many candidates is selected using random fluctuations; recording every run does not remove selection bias. A content hash detects change but proves neither truth nor authenticity.

### JAX transformations — notebook-native exception

The page and reviewed Python notebook already form a compact CPU bridge. Migration would currently cause one of two regressions: execute optional JAX during the required Antora build, or lose the established solution-removal/student-instructor cell transformation. The page now carries the gradient, central-difference error, vectorisation, and relative-discrepancy mathematics needed to learn before opening the notebook.

**Exception:** owner, optional CPU environment, and update-triggered full execution are recorded in `curriculum.yml`. Reconsider after the AsciiDoc pipeline can express the variant metadata without installing JAX in the required build.

### Comparative dataframe engines — page-only exception

A build-time result would mix machine, cache, storage, file-layout, and engine-version effects and could become a misleading universal benchmark. A complete comparison also requires optional Polars. The page therefore remains a protocol rather than a frozen notebook result.

**Valuable mathematical insight:** \(T\ge B/b\) is an I/O lower bound and \(n\sum_j w_j\) is only a raw memory-payload lower bound. Neither predicts end-to-end performance without execution-plan and machine evidence.

### Downstream CSMI paths — page-only exception

This item is an ownership and prerequisite map. A notebook would add a redundant artifact with no computation, method, or result. The exception is reviewed annually against the programme and downstream owners.

## Cross-cutting consistency

The four generated optional lessons now:

- use English AsciiDoc as the source of truth;
- show Extension (P2) importance explicitly;
- contain Context–Method–Implementation–Results–Conclusion worked examples;
- keep mathematical insight and error estimation on the webpage;
- generate cleared, deterministic, full-profile notebooks;
- use only the required CPU dependency set;
- avoid network access, services, personal accounts, and accelerators.

The three exceptions display the same reason/owner/environment/maintenance information that is canonical in `curriculum.yml`.

## Verification and human gates

Automated verification covers classification completeness, required exception fields, page metadata, dependency isolation, notebook generation, clean-kernel execution, rendered STEM, semantic tables, accessible figures, link resolution, manifests, and the student bundle.

Automation does not provide:

- named instructor approval of the mathematical exposition;
- review by the downstream course owners;
- representative-student evidence that the pages are learnable;
- accessibility sign-off;
- permission to change the annual release status.

Those remain human release gates.
