import { readFile, writeFile } from 'node:fs/promises';

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

console.log(
  `Localised UI fonts and normalised ${lastModifiedEntries.length} sitemap timestamps`,
);
