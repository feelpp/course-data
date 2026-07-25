const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const test = require('node:test')

const asciidoctor = require('@asciidoctor/core')()
const JupyterConverter = require('asciidoctor-jupyter')
const feelppJupyter = require('@feelpp/antora-extensions/src/jupyter.js')

asciidoctor.ConverterFactory.register(JupyterConverter, ['jupyter'])

const fixtureDir = path.join(__dirname, '..', 'fixtures', 'asciidoc-jupyter')

function convertFixture (name) {
  const source = path.join(fixtureDir, name)
  const converted = asciidoctor.convertFile(source, {
    backend: 'jupyter',
    safe: 'safe',
    standalone: true,
    to_file: false
  })
  return JSON.parse(converted)
}

function generateCourseNotebook (root, relative) {
  const basename = path.basename(relative, '.adoc')
  const page = {
    contents: fs.readFileSync(
      path.join(root, 'docs', 'course', 'modules', 'ROOT', 'pages', relative)
    ),
    src: {
      component: 'course-data',
      version: '',
      module: 'ROOT',
      family: 'page',
      relative
    },
    pub: { url: `/course-data/foundations/${basename}.html` }
  }
  return feelppJupyter.generateNotebook(page, {
    asciidoctorExtensionVersion: '1.0.0-rc.18'
  })
}

function notebookText (notebook, cellType) {
  return notebook.cells
    .filter((cell) => cell.cell_type === cellType)
    .map((cell) => Array.isArray(cell.source) ? cell.source.join('') : cell.source)
    .join('\n')
}

test('representative AsciiDoc converts deterministically to notebook 4.4', () => {
  const first = convertFixture('representative.adoc')
  const second = convertFixture('representative.adoc')

  assert.deepEqual(first, second)
  assert.equal(first.nbformat, 4)
  assert.equal(first.nbformat_minor, 4)
  assert.equal(first.metadata.language_info.name, 'python')
  assert.equal(first.metadata.language_info.version, '3.12')
  assert.equal(first.metadata.kernelspec.name, 'python3')

  const markdown = first.cells
    .filter((cell) => cell.cell_type === 'markdown')
    .flatMap((cell) => cell.source)
    .join('')
  const code = first.cells.filter((cell) => cell.cell_type === 'code')

  assert.match(markdown, /Representative executable lesson/)
  assert.match(markdown, /standard error/i)
  assert.match(markdown, /\\widehat\\mu_n/)
  assert.match(markdown, /\\operatorname\{SE\}/)
  assert.match(markdown, /Declare the population/)
  assert.match(markdown, /\| Property \| Value/)
  assert.match(markdown, /companion\.ipynb/)
  assert.match(markdown, /sample\.svg/)
  assert.equal(code.length, 2)
  assert.match(code[0].source.join(''), /default_rng\(42\)/)
  assert.match(code[1].source.join(''), /assert sample\.shape == \(8,\)/)
  assert.match(code[1].source.join(''), /<1>/)
  assert.ok(code.every((cell) => cell.outputs.length === 0))
})

test('unsupported constructs are inventoried and surrounding prose survives', () => {
  const notebook = convertFixture('unsupported.adoc')
  const rendered = notebook.cells.flatMap((cell) => cell.source).join('')
  const inventory = JSON.parse(
    fs.readFileSync(path.join(fixtureDir, 'unsupported-nodes.json'), 'utf8')
  )

  assert.match(rendered, /surrounding prose must survive/)
  assert.match(rendered, /final paragraph must also survive/)
  assert.doesNotMatch(rendered, /notebook-demo\.mp4/)
  assert.doesNotMatch(rendered, /data-test="raw-pass"/)
  assert.equal(inventory.converter_version, '0.7.0')
  assert.deepEqual(
    inventory.constructs.map((item) => item.node),
    ['video', 'pass', 'antora_xref', 'source_block_metadata', 'code_callout']
  )
})

test('schemas define deterministic source and notebook identities', () => {
  const root = path.join(__dirname, '..', '..')
  const metadata = JSON.parse(
    fs.readFileSync(path.join(root, 'schemas', 'asciidoc-notebook-metadata.schema.json'), 'utf8')
  )
  const manifest = JSON.parse(
    fs.readFileSync(path.join(root, 'schemas', 'asciidoc-notebook-manifest.schema.json'), 'utf8')
  )

  assert.equal(metadata.properties.source_kind.const, 'asciidoc')
  assert.ok(metadata.required.includes('source_sha256'))
  assert.ok(metadata.required.includes('accessibility'))
  assert.equal(manifest.properties.artifact.const, 'asciidoc-notebook-manifest')
  assert.equal(manifest.properties.entries.type, 'array')
  assert.equal(manifest.properties.generated_at, undefined)
})

test('course mathematics sequence uses the vendored Antora generator deterministically', () => {
  const root = path.join(__dirname, '..', '..')
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
  const notebooks = new Map()
  for (const relative of relatives) {
    const first = generateCourseNotebook(root, relative)
    const second = generateCourseNotebook(root, relative)
    assert.deepEqual(first, second)
    notebooks.set(relative, JSON.parse(first.toString('utf8')))
  }

  for (const notebook of notebooks.values()) {
    assert.equal(notebook.metadata.course.generator.asciidoctor_jupyter, '0.7.0')
    assert.equal(notebook.metadata.course.generator.feelpp_antora_extensions, '1.0.0-rc.7')
    assert.equal(notebook.metadata.course.generator.feelpp_asciidoctor_extensions, '1.0.0-rc.18')
    assert.ok(notebook.cells.every((cell) => /^[0-9a-f]{16}$/.test(cell.id)))
    assert.ok(notebook.cells.filter((cell) => cell.cell_type === 'code').every((cell) => cell.outputs.length === 0))
  }

  const distributions = notebooks.get('foundations/probability-distributions-moments.adoc')
  const distributionMarkdown = notebookText(distributions, 'markdown')
  const distributionCode = notebookText(distributions, 'code')
  assert.match(distributionMarkdown, /Probability distributions and statistical moments/)
  assert.match(distributionMarkdown, /\\gamma_1=\\mu_3\/\\sigma\^3/)
  assert.match(distributionMarkdown, /Visual probability distribution zoo/)
  assert.match(distributionMarkdown, /failed Poisson implication/i)
  assert.match(distributionCode, /# Build probability masses for three named discrete models/)
  assert.match(distributionCode, /stats\.bernoulli\.pmf/)
  assert.match(distributionCode, /stats\.t\.pdf/)

  const quantiles = notebooks.get('foundations/quantiles-exceedance-risk.adoc')
  const quantileMarkdown = notebookText(quantiles, 'markdown')
  const quantileCode = notebookText(quantiles, 'code')
  assert.match(quantileMarkdown, /Q\(p\)=\\inf/)
  assert.match(quantileMarkdown, /strict exceedance probability/i)
  assert.match(quantileMarkdown, /classifier decision threshold/i)
  assert.match(quantileCode, /# Map a probability level to a quantile/)
  assert.match(quantileCode, /duration_model\.sf\(limit\)/)

  const mean = notebooks.get('foundations/mean-uncertainty.adoc')
  const meanMarkdown = notebookText(mean, 'markdown')
  const meanCode = notebookText(mean, 'code')
  assert.match(meanMarkdown, /\$\$\n\\widehat\\mu_n/)
  assert.match(meanMarkdown, /Classical central limit theorem/)
  assert.match(meanMarkdown, /t_\{n-1/)
  assert.match(meanMarkdown, /long-run coverage/i)
  assert.doesNotMatch(meanMarkdown, /attachment\$/)
  assert.match(meanCode, /# Fix the seed so that the webpage, notebook, and CI obtain the same simulation\./)
  assert.match(meanCode, /# Generate one population sample with the requested shape/)
  assert.match(meanCode, /# Compute one estimator per repeated sample/)
  assert.match(meanCode, /# Use panel labels, edges, and a dashed reference/)
})

test('public specimens become solution-free task notebooks with equivalent contracts', () => {
  const root = path.join(__dirname, '..', '..')
  const relatives = [
    'assessment/control-1-specimen.adoc',
    'assessment/mini-project.adoc',
    'assessment/control-2-specimen.adoc',
    'assessment/final-exam-specimen.adoc'
  ]
  for (const relative of relatives) {
    const notebook = JSON.parse(generateCourseNotebook(root, relative).toString('utf8'))
    const exercise = notebook.metadata.course.exercise
    const promptCells = notebook.cells.filter((cell) => (cell.metadata.tags || []).includes('exercise-prompt'))
    const promptTaskIds = new Set(promptCells.flatMap((cell) => cell.metadata.course.task_ids))
    assert.equal(notebook.metadata.course.artifact_variant, 'student')
    assert.equal(notebook.metadata.course.solutions_included, false)
    assert.deepEqual(promptTaskIds, new Set(exercise.task_ids))
    assert.deepEqual(new Set(Object.keys(exercise.task_priorities)), new Set(exercise.task_ids))
    assert.deepEqual(new Set(Object.keys(exercise.task_points)), new Set(exercise.task_ids))
    assert.ok(notebook.cells.every((cell) => {
      const tags = new Set(cell.metadata.tags || [])
      return !['solution', 'instructor-only', 'remove-cell'].some((tag) => tags.has(tag))
    }))
    assert.ok(notebook.cells.every((cell) => cell.cell_type !== 'code' || (cell.outputs.length === 0 && cell.execution_count === null)))
  }
})
