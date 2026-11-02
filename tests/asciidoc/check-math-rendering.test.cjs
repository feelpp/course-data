const assert = require('node:assert/strict')
const test = require('node:test')
const katex = require('katex')

test('math validation ignores JavaScript, styles and literal code like the browser renderer', async () => {
  const { courseMathContent } = await import('../../tools/math-course-content.mjs')
  const content = courseMathContent(String.raw`
    <script>const fake = '<main id="fake">\\(not math\\)</main>';</script>
    <aside>\(outside\)</aside>
    <main id="main-content">
      <p>\(x^2\)</p><div>\[S=C^TC/(n-1)\]</div>
      <script type="text/javascript">const regex = /\(hsl\)/; const closing = '</main>';</script>
      <style>.example:after { content: '\(literal\)'; }</style>
      <pre><code>\(literal code\)</code></pre>
      <!-- \(a comment\) -->
    </main>`)
  const expressions = [...content.matchAll(/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g)]
    .map(match => match[1] ?? match[2])
  assert.deepEqual(expressions, ['x^2', 'S=C^TC/(n-1)'])
  for (const expression of expressions) {
    assert.doesNotThrow(() => katex.renderToString(expression, { throwOnError: true }))
  }
})

test('invalid visible mathematics still fails and a missing main landmark is still rejected', async () => {
  const { courseMathContent } = await import('../../tools/math-course-content.mjs')
  const content = courseMathContent(String.raw`<main id="main-content">\(\unknownCourseCommand{x}\)</main>`)
  const expression = [...content.matchAll(/\\\(([\s\S]*?)\\\)/g)][0][1]
  assert.throws(() => katex.renderToString(expression, { throwOnError: true }), /Undefined control sequence/)
  assert.equal(courseMathContent('<script>const fake = "<main id=a></main>";</script>'), null)
  assert.equal(courseMathContent('<main id="main-content">incomplete'), null)
})
