const assert = require('node:assert/strict')
const fs = require('node:fs')
const os = require('node:os')
const path = require('node:path')
const test = require('node:test')
const braces = require('braces')
const glob = require('fast-glob')

test('patched braces preserves expansion, compilation, AST round trips and file discovery', async (t) => {
  assert.deepEqual(braces.expand('x/{a,b}/file-{1..2}.adoc'), [
    'x/a/file-1.adoc', 'x/a/file-2.adoc', 'x/b/file-1.adoc', 'x/b/file-2.adoc'
  ])
  assert.deepEqual(braces('docs/{course,governance}/**/*.adoc'), [
    'docs/(course|governance)/**/*.adoc'
  ])
  const pattern = 'x/{a,b}/file-{1..2}.adoc'
  assert.equal(braces.stringify(braces.parse(pattern)), pattern)
  const shallow = '{'.repeat(50) + 'value' + '}'.repeat(50)
  assert.deepEqual(braces.expand(shallow), [shallow])

  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'course-braces-compatibility-'))
  t.after(() => fs.rmSync(root, { recursive: true, force: true }))
  for (const name of ['course', 'governance']) {
    fs.mkdirSync(path.join(root, 'docs', name), { recursive: true })
    fs.writeFileSync(path.join(root, 'docs', name, 'page.adoc'), '= Page')
    fs.writeFileSync(path.join(root, 'docs', name, 'skip.txt'), 'Not a page')
  }
  assert.deepEqual((await glob('docs/{course,governance}/**/*.adoc', { cwd: root })).sort(), [
    'docs/course/page.adoc', 'docs/governance/page.adoc'
  ])
})

test('deep brace, parenthesis and unclosed patterns fail with a controlled depth error', () => {
  const patterns = [
    '{'.repeat(4000) + 'a' + '}'.repeat(4000),
    '('.repeat(4000) + 'a' + ')'.repeat(4000),
    '{'.repeat(4000) + 'a'
  ]
  for (const pattern of patterns) {
    for (const operation of [braces, braces.parse, braces.compile, braces.expand, braces.stringify]) {
      assert.throws(() => operation(pattern, { maxLength: 65536, maxDepth: Infinity }), {
        name: 'SyntaxError', message: /maximum depth/
      })
    }
  }
})

test('direct AST walkers reject excessive nesting and cycles without following parent backlinks', () => {
  const ast = { type: 'root', nodes: [] }
  let node = ast
  for (let i = 0; i < 4000; i++) {
    const child = { type: 'brace', nodes: [], parent: node }
    node.nodes.push(child)
    node = child
  }
  const cycle = { type: 'root', nodes: [] }
  cycle.nodes.push(cycle)
  for (const name of ['compile', 'expand', 'stringify']) {
    const internal = require(`braces/lib/${name}`)
    for (const input of [ast, cycle]) {
      for (const operation of [braces[name], internal]) {
        assert.throws(() => operation(input), { name: 'SyntaxError', message: /maximum depth/ })
      }
    }
  }
})
