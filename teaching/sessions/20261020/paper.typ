#let green = rgb("155f46")
#let pale = rgb("edf2ee")
#let paper(title, body) = {
  set document(title: title, author: "CSMI M1 · Traitement de données")
  set page(paper: "a4", margin: (x: 16mm, top: 15mm, bottom: 17mm),
    footer: context {set text(size: 8pt, fill: green); grid(columns: (1fr, auto),
      [CSMI M1 · 20 octobre 2026 · Traitement de données], counter(page).display())})
  set text(font: "Arial", size: 10.5pt, lang: "fr", fill: rgb("142a24"))
  set par(leading: 0.5em, spacing: 0.65em)
  set heading(numbering: none)
  show heading.where(level: 1): set text(size: 20pt, fill: green)
  show heading.where(level: 2): set text(size: 12.8pt, fill: green)
  show math.equation: set text(font: "New Computer Modern Math", size: 12.5pt)
  show raw: set text(font: "DejaVu Sans Mono", size: 8.3pt)
  body
}
#let callout(body) = block(width: 100%, fill: pale, inset: 8pt, radius: 4pt)[#body]
#let th(body) = table.cell(fill: green)[#text(fill: white, weight: "bold", body)]
#let tab(columns, ..cells) = table(columns: columns, inset: 6pt,
  stroke: 0.4pt + rgb("c7d5ca"), ..cells)
