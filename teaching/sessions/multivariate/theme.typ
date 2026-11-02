#let ink = rgb("142a24")
#let green = rgb("155f46")
#let muted = rgb("50675e")
#let setup(session, body) = {
  set document(title: session.title, author: "M1 CSMI · Traitement de données")
  set page(width: 13.333in, height: 7.5in,
    margin: (x: 43pt, top: 29pt, bottom: 35pt), fill: rgb("faf8f2"),
    footer: context {
      set text(size: 10pt, fill: muted)
      grid(columns: (1fr, auto, 1fr), [M1 CSMI · #session.label],
        [#counter(page).display() / #session.slides], align(right)[Traitement de données])
    })
  set text(font: "Arial", size: 21pt, fill: ink, lang: "fr")
  set par(leading: 0.5em, spacing: 0.6em)
  show math.equation: set text(font: "New Computer Modern Math", size: 24pt)
  show raw: set text(font: "DejaVu Sans Mono", size: 13pt)
  body
  context [#metadata(counter(page).get().first()) <slide-page-count>]
}
#let frame(title, body) = {
  context {
    if counter("frames").get().first() > 0 { pagebreak() }
  }
  counter("frames").step()
  [#metadata(title) <frame-title>]
  text(size: 30pt, weight: "bold", fill: green, title)
  v(17pt)
  body
}
#let point(body) = {grid(columns: (13pt, 1fr), gutter: 5pt, text(fill: green)[•], body); v(10pt)}
#let ask(body) = {v(9pt); text(size: 18pt, fill: green, weight: "bold")[À discuter : #body]}
#let note(body) = {v(8pt); block(fill: rgb("eaf0e9"), inset: 10pt, width: 100%)[#set text(size: 18pt); #body]}
#let two(left, right) = grid(columns: (1fr, 1fr), gutter: 25pt, left, right)
#let fig(name, height: 235pt) = align(center, image("generated/" + name + ".svg", width: 100%, height: height, fit: "contain"))
#let notebook(name, section) = block(above: 8pt)[#text(size: 15pt, fill: green)[
  #link("https://feelpp.github.io/course-data/course-data/sessions/" + name + ".html")[Notebook anglais ↗] · #section]]
#let code(body) = block(width: 100%, fill: rgb("edf2ee"), inset: 12pt)[#body]
