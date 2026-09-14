# Class slides

`20260914-pandas.json` contains the 23 slides for the two-hour CSMI session on
14 September 2026. The audience knows Python and is learning pandas. Student
text is in English; teaching notes are in French. The timings include practice
and a ten-minute break.

The route is Python–pandas, groups/joins/SQL, data lifecycle, then arrays and
table reshaping. Each slide links to the relevant public course page or section.
The four corresponding AsciiDoc pages remain the complete, executable references.

Run `node tools/build_lesson_slides.mjs` to regenerate the standalone HTML in
`build/slides/`. Antora also runs this builder and publishes its output as an
attachment. The viewer works without external JavaScript or font downloads;
course links stay in the same Antora site, including a local preview. When the
HTML file is opened directly from disk, they use the public website instead.

The editable PowerPoint is stored in
`docs/course/modules/ROOT/attachments/slides/20260914-pandas.pptx`.
It includes native tables, clickable links and speaker notes. When revising the
session, keep the PowerPoint and JSON content in agreement. Building the website
regenerates the HTML, not the PowerPoint.

The course page `session-pandas.adoc` provides the entry point and schedule.
The presentation is separate from the student notebook bundle.
