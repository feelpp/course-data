const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const test = require('node:test')

const asciidoctor = require('@asciidoctor/core')()
const dynamicPython = require('@feelpp/asciidoctor-extensions/src/dynamic-notebook-processor.js')
const feelppJupyter = require('@feelpp/antora-extensions/src/jupyter.js')

const root = path.join(__dirname, '..', '..')
const interpreter = path.join(root, '.venv', 'bin', 'python3')
const file = { src: { relative: 'contract.adoc' } }
const contentCatalog = {
  resolveResource: (key) => {
    if (key === 'attachment$data.csv') {
      return { pub: { url: '/course-data/_attachments/data.csv' } }
    }
    return null
  }
}

function convert (body, attributes = '') {
  const registry = asciidoctor.Extensions.create()
  dynamicPython.register(registry, { contentCatalog, file })
  const source = `:dynamic-blocks:\n:dynamic-blocks-strict:\n:dynamic-blocks-timeout-seconds: 5\n:dynamic-blocks-max-output-bytes: 4096\n:dynamic-python-interpreter: ${interpreter}\n:dynamic-python-isolate-user-site:\n${attributes}\n${body}`
  return asciidoctor.convert(source, { extension_registry: registry })
}

function captureError (callback) {
  try {
    callback()
  } catch (error) {
    return error
  }
  assert.fail('Expected callback to throw')
}

test('course execution preserves state, seeds, attachment paths, and clean reruns', () => {
  const body = `
[#seeded-value]
[%dynamic,python,fail-on-error=]
----
import numpy as np

rng = np.random.default_rng(20260722)
value = int(rng.integers(0, 1_000_000))
print(f"seeded-value={value}")
----

[#shared-value]
[%dynamic,python,fail-on-error=]
----
assert isinstance(value, int)
print("shared-state=ok")
print("resolved=xref:attachment$data.csv[]")
----`

  const first = convert(body)
  const second = convert(body)
  assert.equal(first, second)
  assert.match(first, /seeded-value=178173/)
  assert.match(first, /shared-state=ok/)
  assert.match(first, /resolved=public\/course-data\/_attachments\/data\.csv/)
})

test('course execution fails on Python errors, timeouts, and excessive output', () => {
  const failed = captureError(() => convert(`
[#strict-failure]
[%dynamic,python,fail-on-error=]
----
raise RuntimeError("course integration failure")
----`))
  assert.equal(failed.code, 'block-execution-failed')
  assert.equal(failed.details.blockId, 'strict-failure')

  const timedOut = captureError(() => convert(`
[#timeout-failure]
[%dynamic,python,fail-on-error=]
----
while True:
    pass
----`, ':dynamic-blocks-timeout-seconds: 1'))
  assert.equal(timedOut.code, 'execution-timeout')

  const oversized = captureError(() => convert(`
[#output-failure]
[%dynamic,python,fail-on-error=]
----
print("x" * 100_000)
----`, ':dynamic-blocks-max-output-bytes: 1024'))
  assert.equal(oversized.code, 'output-limit-exceeded')
})

test('course execution does not pass arbitrary credentials to Python', () => {
  const previous = process.env.COURSE_EXECUTION_SECRET
  process.env.COURSE_EXECUTION_SECRET = 'must-not-be-visible'
  let html
  try {
    html = convert(`
[#credential-check]
[%dynamic,python,fail-on-error=]
----
import os

print("credential=" + os.environ.get("COURSE_EXECUTION_SECRET", "absent"))
----`)
  } finally {
    if (previous === undefined) delete process.env.COURSE_EXECUTION_SECRET
    else process.env.COURSE_EXECUTION_SECRET = previous
  }
  assert.match(html, /credential=absent/)
  assert.doesNotMatch(html, /must-not-be-visible/)
})

test('course rich outputs are deterministic, semantic, and accessible', () => {
  const body = `
[#contract-svg]
[%dynamic%open,python,fail-on-error=,output=matplotlib,figure-format=svg,figure-alt="A deterministic line",figure-caption="A deterministic SVG line",result-interpretation="The line rises from zero to one."]
----
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(3, 2))
ax.plot([0, 1], [0, 1])
plt.show()
----

[#contract-table]
[%dynamic%open,python,fail-on-error=,output=table,table-caption="Contract values",table-description="Rows identify variables and columns report values."]
----
import pandas as pd

pd.DataFrame({"value": [1, 2]}, index=["alpha", "beta"])
----`

  const richOutputAttributes = `:dynamic-blocks-timeout-seconds: 30
:dynamic-blocks-max-output-bytes: 1048576`
  const first = convert(body, richOutputAttributes)
  const second = convert(body, richOutputAttributes)
  assert.equal(first, second)
  assert.match(first, /data:image\/svg\+xml;base64,/)
  assert.match(first, /width="\d+" height="\d+"/)
  assert.match(first, /id="contract-svg-interpretation"/)
  assert.match(first, /id="contract-table-table"/)
  assert.match(first, /<caption>Contract values<\/caption>/)
  assert.match(first, /scope="col"/)
  assert.match(first, /scope="row"/)

  const ids = Array.from(first.matchAll(/\sid="([^"]+)"/g), (match) => match[1])
  assert.equal(new Set(ids).size, ids.length)
})

test('generated notebooks preserve page code and contain no pre-filled outputs', () => {
  const relatives = [
    'foundations/data-lifecycle.adoc',
    'foundations/tabular-data.adoc',
    'foundations/data-quality.adoc',
    'foundations/eda-sampling.adoc',
    'foundations/probability-distributions-moments.adoc',
    'foundations/quantiles-exceedance-risk.adoc',
    'foundations/mean-uncertainty.adoc',
    'foundations/safe-pipelines.adoc',
    'foundations/metrics-errors.adoc',
    'foundations/baseline-synthesis.adoc',
    'analytical/linear-probabilistic.adoc',
    'analytical/classification-losses.adoc',
    'analytical/regularisation-generalisation.adoc',
    'analytical/model-selection.adoc',
    'analytical/tree-ensembles.adoc',
    'analytical/pca-clustering.adoc',
    'analytical/performance-columnar.adoc'
  ]
  for (const relative of relatives) {
    const contents = fs.readFileSync(
      path.join(root, 'docs', 'course', 'modules', 'ROOT', 'pages', relative)
    )
    const page = {
      contents,
      src: {
        component: 'course-data',
        version: '',
        module: 'ROOT',
        family: 'page',
        relative
      },
      pub: { url: `/course-data/${relative.replace(/\.adoc$/, '.html')}` }
    }
    const notebook = JSON.parse(feelppJupyter.generateNotebook(page).toString('utf8'))
    const pageSource = contents.toString('utf8')
    const dynamicCode = Array.from(
      pageSource.matchAll(/\[[^\]]*%dynamic[^\]]*\]\n----\n([\s\S]*?)\n----/g),
      (match) => match[1].trim()
    )
    const codeCells = notebook.cells.filter((cell) => cell.cell_type === 'code')
    const codeSources = codeCells.map((cell) => {
      const source = Array.isArray(cell.source) ? cell.source.join('') : cell.source
      return source.trim()
    })

    assert.ok(dynamicCode.length > 0)
    const expectedCode = dynamicCode.map((source) => feelppJupyter.normaliseCode(source, page))
    assert.deepEqual(codeSources, expectedCode)
    assert.ok(codeCells.every((cell) => cell.outputs.length === 0))
  }
})
