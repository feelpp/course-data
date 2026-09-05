# GitHub Pages publishing investigation — 5 September 2026

The normal course CI and the Pages build completed, but creating the Pages
deployment returned HTTP 422. A debug retry and a temporary redacted response
diagnostic confirmed that the API returned only `Validation Failed`, without
field-level errors. The diagnostic was then removed; deployment uses the pinned
upstream action without runtime modification.

Evidence from the initial failures:

- run `33959569514` built commit `57bf6b5` successfully; a failed-job debug retry
  reproduced the rejection;
- run `33960203952` built commit `eb5cebd` successfully and retained the same
  generic API response, with request ID `9420:13BF2E:30B36EB:9EA772A:6A9BECDF`;
- repository Pages mode is `workflow`, HTTPS is enforced, and the `github-pages`
  environment permits `main`;
- the deployment job has `pages: write` and `id-token: write`; OIDC uses the
  repository default configuration;
- the actual uploaded tar contained a root `index.html`, 241 regular files,
  no links or special files, no unsafe paths, and about 15 MB of unpacked data.

The current workflow explicitly reads the existing Pages configuration with
`actions/configure-pages` 6.0.0, uses `actions/deploy-pages` 5.0.1, and retains
the environment policy and OIDC checks. Configuration enablement is false, and
the build receives only read access to Pages metadata. These changes provide a
current standard setup; they do not by themselves establish that the service
rejection has been resolved. The latest main publishing run is the decisive
deployment check.

Useful primary references:

- [Pages deployment API](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-deployment)
- [Deployment action](https://github.com/actions/deploy-pages)
- [Configuration action](https://github.com/actions/configure-pages)

Course execution and two-build reproducibility qualification are separately
reported. A successful test badge must not be presented as evidence that a
rejected publishing job deployed the site. The local preview and student bundle
remain usable independently of GitHub Pages availability.
