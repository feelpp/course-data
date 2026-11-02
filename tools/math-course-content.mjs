// Match the literal elements ignored by KaTeX auto-render in the course UI.
// This is math-source selection, not an HTML sanitizer.
export function courseMathContent(html) {
  const source = html
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(
      /<(script|style|pre|code|textarea|noscript|option)\b[^>]*>[\s\S]*?<\/\1\s*>/gi,
      '',
    );
  const start = source.search(/<main\b[^>]*>/i);
  const end = source.indexOf('</main>', start);
  return start === -1 || end === -1 ? null : source.slice(start, end);
}
