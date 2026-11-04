# Design Guidelines

How every slide looks. These principles hold on every slide; within them, design each slide for its content. The helpers in `assets/slides.py` apply most of them for you, and `assets/check.py` catches the measurable ones. Design serves reading: a slide should be easier to read, not more interesting to look at.

## 1. Grid

- 0.5 in side margins; the 9 in between is 12 columns with 0.2 in gutters. The content area runs from 1.45 in to 4.75 in and is 4 rows with the same gutters; a row holds two lines of 15 pt text.
- Every block starts on a column and spans whole columns: `box(first_column, span, y, h)`.
- Vertically, a block starts on a row (`rows(first_row, span)`), or, in a stack of blocks that size to their content (text, equations, a figure under its text), a gutter below the block above.
- **One column by default.** Text, equations and a single figure or table run the full 12 columns, stacked top to bottom.
- **Columns only when the content needs them:** a figure or table with text beside it, or two to four parallel items that must read as separate (two settings, three components, images to compare).
  - Splits: 6 + 6, 8 + 4, 4 + 4 + 4, 3 × 4.
  - Two sides are 6 + 6 by default. Use 8 + 4 only for a figure with two or three short remarks.
- Off the grid: only a `highlight()` outline on a figure, an `add_arrow` across a gutter, and the contents of a card, which follow its padding.

## 2. Type

- One typeface, one weight: **Inter Regular**, titles included. Hierarchy comes from size and color, never weight.
- Four sizes, by role:

| Role | Size |
|---|---|
| Slide titles | 20 pt |
| Subheadings, card headings | 17 pt |
| Body text | 15 pt |
| Tables, footnotes, page numbers | 13 pt |
| Title and section slides | 28 pt |

- These suit the theme's 10 × 5.625 in slide: 15 pt here reads like 20 pt on a 13.33 in widescreen slide, the usual minimum for body text.
- Never another size to make text fit: cut words or split the slide. (A restyle may drop one slide's body to 13 pt; restyle-guidelines.md.)
- Line spacing 1.15. 10 pt before a bullet, 4 pt before a sub-point. Bullets • – ◦ by level.
- Left-align body text. Center only captions under centered figures, the single sentence of a Statement slide, and term lines under a centered equation.

## 3. Color

All from one blue, Paul Tol's #4477AA (the academic-figure skill's charts use the same). White background, gray text, one accent:

| Role | Color | For |
|---|---|---|
| Body | gray #6A737C | All running text |
| Emphasis | dark navy #1B3A7A | Titles, lead-ins, key words, best values in tables, table rules, equations |
| Structure | blue #4477AA | Subheadings, card headings, outlines on figures |
| Quiet | gray #8D949B | Footnotes, page numbers |
| Surface | #EDF2F7 (cards, our table row), #E1EBF4 (title and section backgrounds) | Grouping, never meaning |

- Color directs attention; it never decorates.
- Emphasize a few words per slide. If everything is navy, nothing is.
- An underline may add to color where color alone isn't enough (the one key phrase of a dense slide, a second-best value), sparingly.
- Words that name a figure's series may take that series' color.
- Never let color alone carry meaning; pair it with a label or a shape.

## 4. Spacing

- Inside is tighter than outside: line gap < sub-point gap < bullet gap < padding inside a card (0.15 in, visually equal on all four sides) < gutter between blocks (0.2 in).
- Related things sit close; unrelated things a gutter or more apart.

## 5. Reading order

- Decide what the audience must read first on each slide and make it the largest or highest-contrast thing there: usually the exhibit, then the title's claim, then the remarks.
- One focal point per slide; everything else supports it.
- Left to right, top to bottom. A figure's remarks sit to its right (or below it), in the order the speaker will point at them.

## 6. Whitespace

- Whitespace is signal, not wasted canvas; a dense slide reads as unclear thinking.
- Nothing runs past the content area, ever. Blocks keep at least a gutter between them and never touch the title, the footnote or each other.
- Text fills at most about three quarters of the content area's height.
- About 40 words of body text per slide is the aim; past 60 (`check.py` reports it, not counting titles, footnotes, tables and references) the slide must lose words or become two slides.
- When in doubt: more space, fewer things.

## 7. Alignment and balance

- Edges align to the grid and to each other: text blocks share a left edge, the columns of a split start on the same row, captions center under centered figures.
- A single group (cards, a theorem with its points) sits in the vertical middle of the content area (`center_vertically`); anything else starts at the top row.
- Use the content area: no empty lower half.

## 8. Consistency

- The same kind of content looks the same on every slide.
- **Before building, write a layout plan:** list the kinds of content in the deck (a figure with its equations, a results table, a figure with remarks, a theorem) and give each one treatment: its split, which side holds what, where its lead-in goes.
- Build every slide of a kind the same way, especially consecutive slides in one section: if one method slide puts the figure left and the equations right on 6 + 6, they all do.
- A slide may differ only when its content is a different kind, never because its text is a little longer.

## 9. Restraint

- No card by default; card-usage-guidelines.md has the gate. The exception: every theorem, lemma, proposition, definition and assumption sits on a statement card (`add_statement`).
- Never nest cards. No borders, shadows, gradients, icons or decoration.
- Tables have horizontal rules only.
- Figures stay whole at their own aspect ratio, centered in their box; never stretched or cropped.
- Marks on a figure are dotted outlines in the theme blue (`highlight`).

## 10. Tone: a research talk, not a pitch

- Results come with their conditions and comparisons ("4.0 vs 4.6 WER on LibriSpeech clean, 10 h of labels"), never as headline claims.
- No hero-number slides, superlatives ("dramatically", "game-changing") or slogans: researchers read them as overselling and trust the work less.

## 11. Finish

- No single word on a paragraph's last line: `save()` tightens spacing by at most 0.5 pt to fix it; otherwise reword.
- Two-line titles break at a natural point (`save()` does this).
- No empty placeholders (`save()` removes them).

## Google Slides compatibility

The deck must look the same after uploading to Google Drive and opening in Google Slides:

- Inter only (a Google Font); Google Slides replaces fonts it doesn't have.
- No autofit (Google Slides never shrinks text): keep text short enough for its box.
- Equations as images (`add_equation`) or Unicode text (`R² = 0.91`); Office equations don't survive the import.
- Charts as images: a native pptx chart becomes an uneditable picture.
- Solid fills only; no gradients, shadows, 3D, animations, transitions, audio, video or embedded objects.
- Hyperlinks and speaker notes survive; use them.

A user's or institution's template replaces the theme when they give one; these principles still apply wherever it doesn't decide.
