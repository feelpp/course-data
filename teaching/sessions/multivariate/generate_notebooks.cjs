// Use exactly the same converter and metadata contract as Antora.
const fs = require('node:fs')
const path = require('node:path')
const { generateNotebook } = require('@feelpp/antora-extensions/src/jupyter.js')
const root = path.resolve(__dirname, '../../..')
const output = path.join(root, 'build/teaching/multivariate/notebooks')
fs.mkdirSync(output, { recursive: true })
for (const name of ['joint-variation', 'matrix-geometry', 'pca-practical']) {
  const relative = `sessions/${name}.adoc`
  const contents = fs.readFileSync(path.join(root, 'docs/course/modules/ROOT/pages', relative))
  const page = {
    contents,
    src: { component: 'course-data', version: '', module: 'ROOT', family: 'page', relative },
    pub: { url: `/course-data/sessions/${name}.html` }
  }
  const notebook = generateNotebook(page, { asciidoctorExtensionVersion: '1.0.0-rc.18' })
  fs.writeFileSync(path.join(output, `${name}.ipynb`), notebook)
  console.log(`Generated ${relative} using the Antora converter`)
}
