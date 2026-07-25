import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

import katex from 'katex';

const siteRoot = fileURLToPath(new URL('../public/course-data/', import.meta.url));

async function* filesBelow(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      yield* filesBelow(path);
    } else if (entry.isFile()) {
      yield path;
    }
  }
}

function decodeEntities(source) {
  return source
    .replaceAll('&lt;', '<')
    .replaceAll('&gt;', '>')
    .replaceAll('&amp;', '&')
    .replaceAll('&quot;', '"')
    .replaceAll('&#39;', "'")
    .replace(/&#(\d+);/g, (_, value) => String.fromCodePoint(Number(value)))
    .replace(/&#x([0-9a-f]+);/gi, (_, value) =>
      String.fromCodePoint(Number.parseInt(value, 16)),
    );
}

let expressionCount = 0;
const errors = [];
for await (const path of filesBelow(siteRoot)) {
  if (!path.endsWith('.html')) continue;
  const html = await readFile(path, 'utf8');
  const mainStart = html.indexOf('<main ');
  const mainEnd = html.indexOf('</main>', mainStart);
  if (mainStart === -1 || mainEnd === -1) {
    errors.push(`${path}: main course-content landmark is missing`);
    continue;
  }
  const courseContent = html.slice(mainStart, mainEnd);
  const expressions = courseContent.matchAll(/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g);
  for (const match of expressions) {
    const displayMode = match[2] !== undefined;
    const expression = decodeEntities(match[1] ?? match[2]);
    expressionCount += 1;
    try {
      katex.renderToString(expression, {
        displayMode,
        output: 'htmlAndMathml',
        strict: 'warn',
        throwOnError: true,
      });
    } catch (error) {
      errors.push(`${path}: ${expression}: ${error.message}`);
    }
  }
}

if (expressionCount === 0) {
  throw new Error('No rendered AsciiDoc stem expressions were found');
}
if (errors.length > 0) {
  throw new Error(`KaTeX rejected ${errors.length} expression(s):\n${errors.join('\n')}`);
}
console.log(`KaTeX rendering validation passed: ${expressionCount} expressions`);
