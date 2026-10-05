const assert = require('node:assert/strict')
const fs = require('node:fs')
const os = require('node:os')
const path = require('node:path')
const { spawnSync } = require('node:child_process')
const test = require('node:test')

test('solution references stay published but absent from search and sitemap across repeated builds', (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'course-solution-publication-'))
  t.after(() => fs.rmSync(root, { recursive: true, force: true }))
  const publicDir = path.join(root, 'public')
  fs.mkdirSync(path.join(root, 'tools'), { recursive: true })
  fs.mkdirSync(path.join(publicDir, '_/css'), { recursive: true })
  const script = path.join(root, 'tools/sanitise_site.mjs')
  fs.copyFileSync(path.join(__dirname, '../../tools/sanitise_site.mjs'), script)
  fs.writeFileSync(path.join(publicDir, '_/css/site.css'), 'body { color: black; }')
  fs.writeFileSync(path.join(publicDir, '_/css/course.css'), 'code { color: black; }')
  const html = '<html><head><link href="_/css/course.css" rel="stylesheet"></head><body>Lesson</body></html>'
  fs.writeFileSync(path.join(publicDir, 'lesson.html'), html)
  fs.writeFileSync(path.join(publicDir, 'lesson-solution.html'), html.replace(
    'Lesson', '<nav><a href="lesson-solution.html">Reference</a></nav>Lesson'))
  fs.writeFileSync(path.join(publicDir, 'sitemap.xml'),
    '<urlset><url><loc>https://example.org/lesson.html</loc><lastmod>2026-10-05</lastmod></url>' +
    '<url><loc>https://example.org/lesson-solution.html</loc><lastmod>2026-10-05</lastmod></url></urlset>')
  fs.writeFileSync(path.join(publicDir, 'search-index.json'), JSON.stringify({
    documents: [{ id: 1, url: '/lesson.html' }, { id: 2, url: '/lesson-solution.html' }]
  }))
  const run = () => {
    const result = spawnSync(process.execPath, [script], { encoding: 'utf8' })
    assert.equal(result.status, 0, result.stderr)
  }
  run()
  const reference = fs.readFileSync(path.join(publicDir, 'lesson-solution.html'), 'utf8')
  assert.match(reference, /noindex, nofollow/)
  assert.doesNotMatch(reference, /href="lesson-solution.html"/)
  assert.match(reference, /<span>Reference<\/span>/)
  assert.doesNotMatch(fs.readFileSync(path.join(publicDir, 'lesson.html'), 'utf8'), /noindex/)
  const search = JSON.parse(fs.readFileSync(path.join(publicDir, 'search-index.json'), 'utf8'))
  assert.deepEqual(search.documents.map((document) => document.url), ['/lesson.html'])
  assert.doesNotMatch(fs.readFileSync(path.join(publicDir, 'sitemap.xml'), 'utf8'), /lesson-solution/)
  run()
  assert.equal(fs.readFileSync(path.join(publicDir, 'lesson-solution.html'), 'utf8'), reference)
})
