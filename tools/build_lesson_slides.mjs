// Build self-contained, keyboard-accessible class slides from their shared source.
import fs from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const source = JSON.parse(await fs.readFile(path.join(root, 'teaching/slides/20260914-pandas.json'), 'utf8'))
const out = path.join(root, 'build/slides')
const esc = (text) => String(text).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c])
const colors = { green: '#155f46', ink: '#142a24' }
const style = (e) => `left:${e.x}px;top:${e.y}px;width:${e.w}px;height:${e.h}px;font-size:${e.size}px;${e.bold ? 'font-weight:700;' : ''}${e.color ? `color:${colors[e.color] || e.color};` : ''}`
// Keep links inside the same Antora site, including when viewing a local build.
function linkAttributes(href) {
  const courseLink = href.startsWith(source.publicBase)
  const target = courseLink ? '../../' + href.slice(source.publicBase.length) : href
  return `href="${esc(target)}"${courseLink ? ` data-public-href="${esc(href)}"` : ''} target="_blank" rel="noopener"`
}

function element(e) {
  if (e.kind === 'table') {
    const sum = e.widths.reduce((a, b) => a + b, 0)
    return `<table class="element" style="${style(e)}"><colgroup>${e.widths.map((w) => `<col style="width:${100 * w / sum}%">`).join('')}</colgroup><thead><tr>${e.values[0].map((v) => `<th scope="col">${esc(v)}</th>`).join('')}</tr></thead><tbody>${e.values.slice(1).map((row) => `<tr>${row.map((v) => `<td>${esc(v)}</td>`).join('')}</tr>`).join('')}</tbody></table>`
  }
  const body = e.href ? `<a ${linkAttributes(e.href)}>${esc(e.text)}</a>` : esc(e.text)
  return e.kind === 'code' ? `<pre class="element code" style="${style(e)}"><code>${body}</code></pre>` : `<p class="element" style="${style(e)}">${body}</p>`
}

let elapsed = 0
const chapters = []
const sections = source.slides.map((s, i) => {
  const start = elapsed
  elapsed += s.minutes
  if ([0, 9, 14, 18, 22].includes(i)) chapters.push(`<option value="${i + 1}">${esc(s.chapter)}</option>`)
  const href = source.publicBase + s.page + (s.anchor ? `#${s.anchor}` : '')
  return `<section class="slide" id="slide-${i + 1}" aria-labelledby="title-${i + 1}" ${i ? 'hidden' : ''}>
    <p class="chapter">${esc(s.chapter)}</p>
    <h1 id="title-${i + 1}" class="${s.cover ? 'cover-title' : ''}">${esc(s.title)}</h1>
    ${s.elements.map(element).join('\n')}
    <footer><a ${linkAttributes(href)}>Open course page</a><span>${start}–${elapsed} min · ${i + 1} / ${source.slides.length}</span></footer>
    <aside class="notes" hidden lang="fr"><h2>Notes pour la séance</h2><p>${esc(s.notes)}</p></aside>
  </section>`
}).join('\n')
if (elapsed !== source.durationMinutes) throw new Error('Slide timings do not match the session duration')

const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${esc(source.title)}</title>
<style>
*{box-sizing:border-box}.skip{position:fixed;left:8px;top:-90px;padding:10px;background:white;z-index:9}.skip:focus{top:8px}html,body{margin:0;min-height:100%;font-family:Arial,Helvetica,sans-serif;color:#142a24;background:#e3e9e6}body{overflow:hidden}a{color:#155f46;text-decoration:underline;text-underline-offset:5px}a:focus-visible,button:focus-visible,select:focus-visible{outline:4px solid #b77712;outline-offset:3px}.viewport{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform:translate(-50%,-50%) scale(var(--scale,1));transform-origin:center}.slide{position:relative;width:1280px;height:720px;background:#fffefb;overflow:hidden;border-top:8px solid #155f46}.slide[hidden]{display:none}.chapter{position:absolute;left:72px;top:26px;margin:0;font-size:21px;color:#155f46;font-weight:700}h1{position:absolute;left:72px;top:69px;width:1136px;height:88px;margin:0;font-size:43px;line-height:1.08;font-weight:700}h1.cover-title{top:127px;font-size:60px;height:143px;max-width:1110px}.element{position:absolute;margin:0;line-height:1.22;white-space:pre-line}.code{font-family:Consolas,'Liberation Mono',monospace;background:#f0f4f1;padding:14px 16px;white-space:pre;line-height:1.24}.code code{font:inherit}table.element{border-collapse:collapse;table-layout:fixed;white-space:normal}th,td{border:1px solid #c6d5cc;padding:10px 14px;vertical-align:middle;text-align:left}th{background:#155f46;color:white;font-weight:700}tbody tr:nth-child(even){background:#f0f4f1}footer{position:absolute;left:72px;right:72px;bottom:21px;font-size:20px;display:flex;justify-content:space-between;align-items:center;color:#566c61}footer a{font-weight:700}.controls{position:fixed;left:0;right:0;bottom:0;height:54px;background:#142a24;color:white;display:flex;gap:14px;align-items:center;justify-content:center;padding:8px;font-size:15px}.controls button,.controls select{font:inherit;padding:6px 10px;border:1px solid #9fbbb0;border-radius:3px;background:#fffefb;color:#142a24}.controls a{color:white}.controls button:disabled{opacity:.5}.status{min-width:90px;text-align:center}.notes{position:absolute;bottom:0;left:0;right:0;max-height:310px;overflow:auto;background:#fff7dd;border-top:3px solid #b77712;padding:20px 40px;font-size:25px;line-height:1.3;z-index:2}.notes h2{margin:0 0 10px;font-size:28px}.notes p{margin:0}.help{font-size:13px;opacity:.85}body.fullscreen .controls{opacity:0;transition:opacity .2s}body.fullscreen .controls:hover,body.fullscreen .controls:focus-within{opacity:1}@media(max-width:700px){.help{display:none}.controls{gap:6px;font-size:12px}.controls select{max-width:130px}.controls a{display:none}}@media print{html,body{background:white;overflow:visible}.controls{display:none}.viewport{position:static;transform:none;width:auto;height:auto}.slide,.slide[hidden]{display:block;page-break-after:always;break-after:page}.notes{display:none!important}a{color:inherit} @page{size:13.3333in 7.5in;margin:0}}
</style></head><body>
<a class="skip" href="#main-content">Skip to slides</a>
<main id="main-content" tabindex="-1" class="viewport" aria-label="Presentation">${sections}</main>
<nav class="controls" aria-label="Slide controls"><button id="previous" aria-label="Previous slide">Previous</button><span id="status" class="status" aria-live="polite"></span><button id="next" aria-label="Next slide">Next</button><select id="chapter" aria-label="Go to section">${chapters.join('')}</select><button id="notes" aria-pressed="false">Notes (N)</button><button id="fullscreen">Full screen (F)</button><a href="20260914-pandas.pptx">PowerPoint</a><span class="help">← → navigate</span></nav>
<script>
const slides=[...document.querySelectorAll('.slide')];
if(location.protocol==='file:')document.querySelectorAll('a[data-public-href]').forEach(a=>{a.href=a.dataset.publicHref;});
const previous=document.getElementById('previous'), next=document.getElementById('next'), status=document.getElementById('status');
const notesButton=document.getElementById('notes'), chapter=document.getElementById('chapter');
let notesVisible=false;
function current(){const value=Number(location.hash.slice(1));return Number.isInteger(value)&&value>=1&&value<=slides.length?value:1;}
function show(){const n=current();slides.forEach((s,i)=>{s.hidden=i!==n-1;s.querySelector('.notes').hidden=!notesVisible;});status.textContent=n+' / '+slides.length;previous.disabled=n===1;next.disabled=n===slides.length;const part=[...chapter.options].filter(o=>Number(o.value)<=n).at(-1);chapter.value=part.value;document.title=n+' / '+slides.length+' · ${esc(source.title)}';}
function go(n){location.hash=String(Math.max(1,Math.min(slides.length,n)));}
function toggleNotes(){notesVisible=!notesVisible;notesButton.setAttribute('aria-pressed',String(notesVisible));show();}
async function fullScreen(){try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{document.getElementById('fullscreen').textContent='Use browser full screen';}}
function resize(){const h=innerHeight-(document.fullscreenElement?0:64);document.documentElement.style.setProperty('--scale',Math.min(innerWidth/1280,h/720));document.querySelector('.viewport').style.top=(document.fullscreenElement?'50%':'calc(50% - 32px)');}
previous.onclick=()=>go(current()-1);next.onclick=()=>go(current()+1);chapter.onchange=()=>go(Number(chapter.value));notesButton.onclick=toggleNotes;document.getElementById('fullscreen').onclick=fullScreen;
document.addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey||/INPUT|SELECT|TEXTAREA/.test(e.target.tagName))return; if(e.key===' '&&/BUTTON|A/.test(e.target.tagName))return; if(['ArrowRight','PageDown',' ','ArrowLeft','PageUp','Home','End'].includes(e.key))e.preventDefault();if(['ArrowRight','PageDown',' '].includes(e.key))go(current()+1);if(['ArrowLeft','PageUp'].includes(e.key))go(current()-1);if(e.key==='Home')go(1);if(e.key==='End')go(slides.length);if(e.key.toLowerCase()==='n')toggleNotes();if(e.key.toLowerCase()==='f')fullScreen();});
document.querySelector('.skip').addEventListener('click',e=>{e.preventDefault();document.getElementById('main-content').focus();});
addEventListener('hashchange',show);addEventListener('resize',resize);document.addEventListener('fullscreenchange',()=>{document.body.classList.toggle('fullscreen',!!document.fullscreenElement);resize();});show();resize();
</script></body></html>\n`
await fs.mkdir(out, { recursive: true })
await fs.writeFile(path.join(out, '20260914-pandas.html'), html)
console.log(`Built ${source.slides.length} slides for ${elapsed} minutes in ${path.relative(root, out)}`)
