# Content Guidelines

How specific kinds of content go on a slide: figures, tables, equations, citations and wording. The storyline and titles are in argument-guidelines.md; the grid, type and color in design-guidelines.md.

## Figures

- This skill doesn't make figures; use the user's image files (the academic-figure skill makes charts in the same colors). If a figure doesn't exist yet, leave it out and list which slides need which figure.
- One figure per slide unless the slide compares two. Two charts making one comparison become one chart.
- Make figures at slide size with 14–15 pt text: about 5.9 × 3.3 in beside text (8 columns), 9.0 × 2.8 in across the full width with a row of text below. Figures pasted from a paper have print-size text that doesn't read on a screen; ask for the source or rebuild them when you can.
- Charts: ours in the theme blue, baselines in grays, one legend, the metric's direction (lower or higher is better) stated.
- **Mark the key finding on the figure:** the focal series in the theme blue with the rest gray, a dotted `highlight()` around the part that matters, or the finding stated as the first remark beside the figure.
- Words that name a series in a figure may take that series' color (`"#RRGGBB"` runs).
- Never stretch, crop or recolor a figure; `add_image` and `figure` keep it whole and centered.

## Tables

- At most about 6 columns and 8 rows. Larger: keep the key rows and move the full table to a backup slide.
- `add_table` sets the style: 13 pt text; rules above, under the header and below, no vertical lines; dark navy header; a grouped header with `groups=` (a test set with several splits); the best value per column in dark navy with `best=`, or within each setting with `best_groups=`; a light tint on our row only; numbers right-aligned, marks (✓ ✗) centered.
- Give each column enough grid columns that no cell wraps; `check.py` reports cells that do.
- Put the unit on the metric and say whether lower or higher is better, in the header or the footnote.
- Never paste a table as an image in a new talk (in a restyle, a table too big to rebuild stays a crop).

## Equations

- Display equations: `add_equation(slide, first_column, span, y, tex, size)` sets LaTeX (matplotlib mathtext) in Computer Modern, the serif of LaTeX papers, as an image, so equations look as they do in the paper. Office equation objects don't survive the import into Google Slides.
- Inline math in text: plain Unicode (`R² = 0.91`, `p < 0.001`), italic runs for variables, `"sub"` / `"super"` runs where Unicode has no character. Never combining accents (π̄, x̂): renderers misplace or drop them. Put a symbol with an accent in an `add_equation` line, or name it in words ("π-bar").
- Explain the key symbols in short term lines below the equation; the equation itself stays dark navy.
- Theorems, lemmas, propositions, definitions and assumptions: one statement card each (`add_statement`), the label as its heading, the statement's text and equations inside, what it means below the card.

## Citations

- After a borrowed claim or number, a superscript number (`¹`); in the footnote, the same number and the author-year reference: "¹ Heckman et al. (2013), *Science*." Follow the field's convention (author-year in the sciences, numbered notes in the humanities), one style through the deck.
- Under a borrowed figure, in the footnote: "Source: Jones et al. (2021), Fig. 3." Reusing a published figure may need the publisher's permission; mention it to the user.
- The References slide lists every footnoted source in full.
- Cite only sources the user gave or you read; never invent one.

## Wording

- Define every acronym on first use.
- Telegraphic bullets: drop articles and filler where the meaning survives ("Intervention cut costs 23% (p < 0.01)", not "Our study found that the intervention reduced costs").
- Parallel bullets: same grammatical form, one idea each, a lead-in in dark navy when the bullets are a list of named things.
- Plain words, no idioms.
- Never end a paragraph with a single word on its last line; reword it if `check.py` reports one.
