# Restyle Guidelines

For converting an existing deck (PDF, PPTX, Keynote export) into this theme. **Change only the style and keep everything else exactly:** the same slides in the same order, titles word for word, the same text, figures, equations and numbers, the same grouping of items on each slide. Don't rewrite titles or text, don't merge, add or remove slides, and split a slide only under rule 6. The design guidelines apply in full; the argument guidelines don't (the content is the author's).

## Rules

1. **Read the whole source first.** Render every page (PyMuPDF at about 200 dpi) and list what each slide holds.

2. **Layout plan before building** (design-guidelines.md, principle 8). Sort the source slides into kinds of content and give each kind one treatment, so the restyled deck is more consistent than the source, not less. Same-kind slides in one section use the same split, with the same thing on the same side.

3. **Figures and table crops never shrink.** Crop each figure whole from the source page. On the restyled slide it is at least as large as on the source slide (the same share of the slide's width or height), and its smallest text stays readable. The layout makes room for it, not the other way round:
   - give it the full width or all four rows;
   - put a rebuilt table beside it, or lower that table's `row_h`;
   - set the slide's text at 13 pt before shrinking a figure.

   If a figure is taller than the content area allows at source size, use the whole content area and tell the user.

4. **Tables:** rebuild with `add_table` when the table fits at 13 pt. A table too big for that (many rows or columns, multi-line cells, ± subscripts) stays a crop, under rule 3.

5. **Equations and annotations:**
   - Re-set equations with `add_equation` when they were screenshots (avoid `\left`, `\mathcal`, `\mathbb`; see its docstring).
   - Theorems, lemmas, definitions and assumptions go on statement cards (`add_statement`).
   - Boxes, arrows and circled terms that tie a remark to part of a figure or equation are content: redraw them with `highlight()` and `add_arrow`.
   - Logos, clip art, icons and decorative pictures are not content: drop them, keeping logos only on the title slide.

6. **A slide too dense for whitespace** (design-guidelines.md, principle 6). Try in order:
   1. Use the space: full width, all four rows.
   2. Set that slide's body at 13 pt, the smallest size in the scale, never smaller.
   3. Split it into consecutive slides with the same title, the later ones ending in "(cont.)". Split as many times as whitespace needs; dense source decks often double in length, and that is fine. Each part gets the same layout and a balanced share, never a nearly empty slide. Keep every word, figure and item in its original order and grouping.

   Tell the user which slides were split. Never cut words, drop items, overflow or cram.

7. **Original wording stays,** even where `check.py` reports a title over two lines or a single word on a last line that `save()` couldn't pull back. Don't reword and don't force line breaks; list those slides for the user.

## Finishing

- Compare every restyled page with its source page side by side, at the same size: nothing lost, figures no smaller, same-kind slides alike.
- Keep intermediate files (page renders, trial crops, comparison images) in a temporary folder and delete it. Leave only the deck, its PDF, the build script and the figures it uses.
- Report: slides split, figures that couldn't keep their size, tables kept as crops, and anything `check.py` still lists.
