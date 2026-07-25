# Course operation and maintenance

## Recurring checks

- **Monthly:** dependency and GitHub Actions update review; `npm audit --audit-level=high`; security-triage review.
- **Weekly and before a candidate tag:** complete CPU notebook suite, repository tests, site build, link/accessibility checks, and student-bundle validation.
- **Before each semester:** clean installation on the reference environment and one supported lower-spec physical machine; rerun representative tasks and assessment delivery rehearsal.
- **Annually:** dataset licence, source URL, checksum, privacy classification, attribution, and link audit; accessibility and English review; environment support decision.
- **After each assessment:** item difficulty/discrimination review using aggregate pseudonymous statistics; rotate compromised or overexposed items in the private assessment repository.
- **At semester end:** publish an internal retrospective, prioritise issues, record deprecations, and assign owners/dates for the next delivery.

## Deprecation rule

Stable concepts are not rewritten solely to follow tool fashion. A dependency, API, dataset, or page can be deprecated when it is unsupported, insecure, inaccessible, unlicensed, misleading, or outside the course boundary. Record replacement, migration path, last supported release, and assessment impact before removal.

## Incident handling

Correctness, accessibility, privacy, licence, and assessment-boundary defects are release blockers. Environment outages and defective bundles are infrastructure incidents; record the affected version/checksum and apply an equitable assessment response. Public issues must never contain student submissions, direct identifiers, hidden tests, live examination content, or confidential review notes.
