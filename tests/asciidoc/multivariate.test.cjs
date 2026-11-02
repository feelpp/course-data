const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const test = require('node:test')
const asciidoctor = require('@asciidoctor/core')()
const { generateNotebook } = require('@feelpp/antora-extensions/src/jupyter.js')
const root = path.resolve(__dirname, '../..')

test('collapsible multivariate proofs and code survive canonical notebook conversion', () => {
  const contracts = [
    ['joint-variation', 11, 12, ['Unbiased covariance', 'Best affine approximation',
      '20 October 2026', 'The correlation matrix is a standardized Gram matrix',
      'Independence implies zero covariance', 'Step 1 — Factor the joint probabilities',
      'Step 3 — Expand the covariance', 'two independent fair coin tosses',
      '\\frac1{n^2}', '\\mathbb E[Q_{XY}]', 'Step 4 — Take the expectation', 'intersection']],
    ['matrix-geometry', 4, 8, ['2 November 2026', 'PCA maximizes',
      'reference/preparation for 9 November', 'new coordinate need not be a physical sensor',
      '\\Sigma^\\top\\Sigma', '\\mathbf X(\\widehat\\beta-\\gamma)',
      'Step 3.', 'same-hour', 'not an untouched final test']],
    ['pca-practical', 0, 6, ['45-minute practical', 'calculate the quantities',
      'Reconstruct and change one decision', 'original physical unit']]
  ]
  for (const [name, proofs, cells, required] of contracts) {
    const relative = `sessions/${name}.adoc`
    const contents = fs.readFileSync(path.join(root, 'docs/course/modules/ROOT/pages', relative))
    const page = { contents,
      src: { component: 'course-data', version: '', module: 'ROOT', family: 'page', relative },
      pub: { url: `/course-data/${relative.replace('.adoc', '.html')}` } }
    const first = generateNotebook(page)
    assert.deepEqual(first, generateNotebook(page))
    const notebook = JSON.parse(first.toString())
    const markdown = notebook.cells.filter(c => c.cell_type === 'markdown').map(c => c.source).join('\n')
    const code = notebook.cells.filter(c => c.cell_type === 'code')
    for (const token of required) assert.ok(markdown.includes(token), `${name}: lost ${token}`)
    assert.equal(code.length, cells)
    assert.ok(code.every(c => c.outputs.length === 0 && c.execution_count === null))
    assert.equal(notebook.metadata.course.language, 'en')
    // Standard HTML conversion must keep native keyboard-operable details.
    const html = asciidoctor.convert(contents.toString(), { standalone: true })
    assert.equal((html.match(/<summary[^>]*>Proof/g) || []).length, proofs)
    assert.ok((html.match(/<details>/g) || []).length >= proofs)
    if (proofs > 0) assert.ok(html.includes('Proposition:'))
  }
})
