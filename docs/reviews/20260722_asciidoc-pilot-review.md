# Executable AsciiDoc pilot review

Date: 2026-07-22

Scope: `data-lifecycle.adoc`, `eda-sampling.adoc`, and `linear-probabilistic.adoc`.

## Review method

The instructor review followed each page in navigation order and checked the learning question, mathematical definitions, error-estimation language, executable evidence, interpretation, exercise, and notebook hand-off. A structured representative-student walkthrough then used three profiles: a student comfortable with Python but new to statistical estimands, a mathematically strong student new to pandas and scikit-learn conventions, and a student using keyboard navigation and non-colour visual encodings. This is a documented proxy review; observations from an actual cohort should still be collected during delivery.

Each profile had to answer the page's opening question, predict an output before execution, explain one result without relying on the code listing, download the generated notebook, restart and run it, and identify one unsupported claim.

## Findings

### Data lifecycle and first audit

- The estimand/estimate distinction is introduced before code and is used again in the exercise.
- The executable table makes duplicate, missing-value, and physical-range checks visible without hiding detection inside a notebook.
- The prose correctly separates detection, blocking, repair, and population representativeness.
- The generated notebook uses the same commented code and resolves its dataset path relative to the notebook.

### Exploratory analysis and sampling

- Empirical distribution, covariance, sampling inclusion, dependence, and effective-information arguments precede plotting.
- The SVG figure has labelled units, markers and line styles in addition to colour, alternative text, a caption, and a separate interpretation.
- The limitation explicitly prevents causal or city-wide claims from a three-station, fourteen-day slice.
- The notebook restarts cleanly and produces the same substantive evidence.

### Stable linear regression and probabilistic modelling

- The page connects empirical risk, normal equations, SVD, Gaussian likelihood, conditioning, coefficient uncertainty, and prediction error.
- The normal-equation solve is labelled as a diagnostic counterexample. The stable path uses `lstsq`; Ridge is described as changing the objective and estimand.
- The semantic table exposes coefficient instability alongside stable RMSE. The residual/singular-value figure prevents a reassuring residual plot from hiding ill-conditioning.
- Exercises distinguish numerical sensitivity, sampling variation, and generalisation error.

## Acceptance decision

All Essential/Core gates pass for the reviewed scope: the pages are sufficient to learn the concepts without opening the notebook; the notebooks are runnable extensions of the pages rather than duplicate narratives; code/output IDs are stable; outputs remain usable offline; and accessibility evidence is explicit. No blocking issue was found for continuing the same architecture across the required foundations sequence.

Delivery follow-up: collect time-on-task, the first point of confusion, notebook restart failures, and accessibility feedback from the first CSMI cohort. Treat those observations as evidence for revising explanations, not as a reason to fork page and notebook narratives.
