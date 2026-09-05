# Learning experiments — 5 September 2026

The regularisation, selection, and clustering examples were independently authored
for this course. The colleague's locally reviewed archive motivated the repeated-
sample bias–variance and penalty-path teaching ideas; no raw notebook, historical
exam solution, or restricted bibliography content was copied.

The regularisation experiment uses a known quadratic oracle and distinguishes
library alpha, a penalty path, a fixed-model learning curve, and a finite-repeat
bias–variance estimate. Extreme high-degree fits can dominate a finite set of
replications; the displayed ordering is not a universal ranking of estimators.

Feature/model search uses separate synthetic data from the initial split-design
diagnostic, with complete groups held out before preprocessing or selection.
The search grid is fixed before evaluation. Its winning CV score and final-test
score have different roles.

The Dry Bean example is a class-balanced benchmark with prescribed K=7; it does
not claim label-blind discovery. New blobs/moons experiments compare K-means,
single linkage, and DBSCAN with fixed parameters. DBSCAN coverage accompanies
its silhouette to avoid hiding rejected points. Oracle class agreement is a
teaching diagnostic, not scientific proof of natural classes.

All executable sources remain in the AsciiDoc pages and generate the notebooks
and figures. Normal/full execution and academic review have distinct roles;
these computational examples do not replace the pending independent review.
