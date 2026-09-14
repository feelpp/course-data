import { createHash } from 'node:crypto';
import { readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const stylesheet = new URL('../public/_/css/site.css', import.meta.url);
const sitemap = new URL('../public/sitemap.xml', import.meta.url);
const externalImports = [
  '@import url("https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,700&display=swap");',
  '@import url("https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600;1,700&display=swap");',
  '@import url("https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@300;400;500;600;700&display=swap");',
];

let source = await readFile(stylesheet, 'utf8');
let importsFound = 0;
for (const externalImport of externalImports) {
  const first = source.indexOf(externalImport);
  if (first !== -1 && source.indexOf(externalImport, first + 1) !== -1) {
    throw new Error(`Found a duplicate upstream font import: ${externalImport}`);
  }
  if (first !== -1) {
    importsFound += 1;
    source = source.replace(externalImport, '');
  }
}
if (importsFound !== 0 && importsFound !== externalImports.length) {
  throw new Error(`Found only ${importsFound}/${externalImports.length} upstream font imports`);
}

source = source
  .replaceAll('Source Sans Pro', 'Roboto')
  .replaceAll('Open Sans', 'Roboto')
  .replaceAll('Source Code Pro', 'Roboto Mono');

if (/url\(\s*['"]?(?:https?:)?\/\//.test(source)) {
  throw new Error('The generated UI stylesheet still contains an external runtime URL');
}

await writeFile(stylesheet, source, 'utf8');

let sitemapSource = await readFile(sitemap, 'utf8');
const buildEpochSeconds = Number(process.env.SOURCE_DATE_EPOCH ?? '1767225600');
const buildTimestamp = new Date(buildEpochSeconds * 1000).toISOString();
const lastModifiedEntries = sitemapSource.match(/<lastmod>[^<]+<\/lastmod>/g) ?? [];
if (lastModifiedEntries.length === 0) {
  throw new Error('The generated sitemap has no last-modified entries to normalise');
}
sitemapSource = sitemapSource.replaceAll(
  /<lastmod>[^<]+<\/lastmod>/g,
  `<lastmod>${buildTimestamp}</lastmod>`,
);
await writeFile(sitemap, sitemapSource, 'utf8');

// Antora can preserve an asset's timestamp across builds. Use the stylesheet
// content to refresh cached course styles in both previews and deployed pages.
const siteDirectory = fileURLToPath(new URL('../public/', import.meta.url));
const courseCss = await readFile(path.join(siteDirectory, '_/css/course.css'));
const courseCssVersion = createHash('sha256').update(courseCss).digest('hex').slice(0, 12);
async function versionCourseStyles(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      await versionCourseStyles(filename);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      const html = await readFile(filename, 'utf8');
      const versioned = html.replace(
        /(href="[^"?]*\/css\/course\.css)(?:\?[^"\s]*)?("|&quot;)/g,
        `$1?v=${courseCssVersion}$2`,
      );
      if (versioned !== html) await writeFile(filename, versioned, 'utf8');
    }
  }
}
await versionCourseStyles(siteDirectory);

console.log(
  `Localised UI fonts, versioned course styles, and normalised ${lastModifiedEntries.length} sitemap timestamps`,
);
