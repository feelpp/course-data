# Accessibility validation

## Implemented contract

Student pages provide a skip link, visible keyboard focus, reduced-motion handling, textual P0--P3 importance labels, English headings, and a dedicated accessibility page. UI icons are decorative when adjacent text supplies the name; logos have meaningful alternatives. Generated-site validation rejects content images without an `alt` attribute and verifies the main landmark and skip link.

The bilingual English--French glossary supports entry terminology while keeping all learning and assessment instructions in English. Mathematics uses `stem`/MathJax and is interpreted in prose near each expression.

Required notebook figures use titles, labelled axes with units, captions/text descriptions, and line/marker differences in addition to colour. Required tasks do not depend on widgets, drag interactions, hover state, or stored output. Student notebooks remain linear, output-free, and keyboard executable.

## Automated evidence and limits

Automation checks structure, metadata, image alternatives, focus CSS, notebook headings, forbidden interactive widgets, and the reviewed figure contract. It cannot certify screen-reader comprehension, cognitive accessibility, mathematical clarity, or an individual's adjustment.

The representative-user pilot therefore includes a keyboard-only task and an assistive-context review. A named human reviewer must record any blocker and the tested browser/Jupyter environment before a candidate tag is approved.
