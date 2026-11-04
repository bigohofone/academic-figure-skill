---
name: academic-slides
description: "Builds research talks as .pptx decks that open cleanly in Google Slides, from a ready-made Academic theme with python-pptx. Use it for any talk about research, such as a paper at a conference, a seminar, a thesis or dissertation defense, a group meeting, or a guest lecture; whenever the user asks for slides about a paper, study, dataset or thesis; and to restyle an existing research deck into the theme."
---

# Academic Slides

Builds a research talk as a .pptx from `{skill-dir}/assets/theme.pptx` (`{skill-dir}` is this skill's base directory). The theme holds the colors, fonts, layouts and page numbers; **you design each slide yourself** under the guidelines below. The helpers in `assets/slides.py` put content on the grid in the theme's sizes and colors, and `assets/check.py` catches what can be measured.

## Guidelines

| File | Covers | Read |
|---|---|---|
| [argument-guidelines.md](argument-guidelines.md) | Audience, storyline, action titles, one job per slide, the slides every talk needs, timing | Before planning a new talk |
| [design-guidelines.md](design-guidelines.md) | Grid, type, color, spacing, reading order, whitespace, consistency, tone, Google Slides compatibility | Always, before building |
| [content-guidelines.md](content-guidelines.md) | Figures, tables, equations, citations, wording | Always, before building |
| [card-usage-guidelines.md](card-usage-guidelines.md) | When a card or box is allowed, and how it looks | Before adding any card or box |
| [restyle-guidelines.md](restyle-guidelines.md) | Converting an existing deck: what must stay, what may change | Instead of Step 1, when restyling |

When they conflict, the order is: what the user asked > restyle rules (for a restyle) > design > content > argument.

## Step 1: Plan the argument (new talks)

1. Settle the audience, the time slot and the one argument the talk makes (argument-guidelines.md).
2. Write a slide-by-slide outline: each slide's action title and its one exhibit or point.
3. Ghost deck test: read only the titles in order; they must tell the whole argument. Fix the outline until they do.
4. Check the count: at most about one content slide per minute.
5. Show the outline to the user and wait for agreement when the deck has more than 10 slides or the content is complex.

For a restyle, follow restyle-guidelines.md instead: the content and order are the author's.

## Step 2: Plan the layout

Write the layout plan (design-guidelines.md, principle 8): the kinds of content in the deck and one treatment for each kind, its column split, which side holds what, where the lead-in goes. One column unless the content needs more. Then for each slide: name its focal point, take its kind's treatment, place the rest in reading order.

## Step 3: Build

Write one Python script in the user's project:

```python
import sys; sys.path.insert(0, "{skill-dir}/assets")
from slides import new_deck, add_slide, add_bullets, add_image, rows, save

prs = new_deck()  # the theme without its example slides
add_slide(prs, "Title", "Early childhood programs raise adult earnings",
          p1=["SOLE · May 2025", "Jane Smith¹, John Doe²", "¹ University of X · ² Lab Y"])

slide = add_slide(prs, "Title Only", "Program children earn 18% more by age 35",
                  p13=["Source: SSA earnings records."])
add_image(slide, 0, 8, *rows(0, 4), "figures/earnings.png", valign="middle")
add_bullets(slide, 8, 4, *rows(0, 4), [[("Bottom quartile: ", True), ("+28%", False)], "Gap opens after age 25"])
slide.notes_slide.notes_text_frame.text = "Transition from the design slide; the one number to remember: 18%."

save(prs, "talk.pptx")  # deletes empty placeholders, balances titles, fixes runts
```

**Layouts** (`add_slide(prs, layout, title, p<idx>=paragraphs)`; `p13` is the footnote): Title, Section Header (the section name alone, centered), Title and Content (bullets), Two Content, Figure and Text, Figure, Statement (the research question on a card), References, Title Only (compose the rest with helpers), Blank.

**Helpers** in `slides.py`, all on the grid; their docstrings give the arguments:

| Helper | Puts on the slide |
|---|---|
| `add_bullets`, `add_text` | Text in grid columns; `h=None` fits the height to the text. A 17 pt subheading is `add_text(..., [[(text, True, True)]], 17)` |
| `add_image`, `figure` | A figure, whole and centered, in a grid box or a picture placeholder |
| `add_table` | A table: 13 pt, horizontal rules, `best=`, `groups=`, `highlight=` |
| `add_equation` | LaTeX in Computer Modern, the serif of papers, as an image |
| `add_statement` | A theorem, lemma or definition on a card, text and equations inside |
| `add_cards`, `add_card` | 2–4 cards in a row, only when the card gate passes |
| `add_flow`, `add_arrow` | Steps with arrows; an arrow joining two blocks |
| `highlight` | A dotted outline on part of a figure |
| `box`, `rows`, `next_row`, `center_vertically`, `resize` | Positions on the grid |
| `numbered`, `plain`, `align` | Numbered or unbulleted paragraphs, alignment |

**Text arguments:** a paragraph is a str, a list of runs, or `(level, ...)` for a sub-point. A run is `(text, style...)`: `True` is emphasis (dark navy), a second `True` or `"accent"` the theme blue, `"underline"` (sparingly, with emphasis), `"italic"` for variables and titles of works, `"super"` / `"sub"`, and `"#RRGGBB"` for words that name a figure's series.

**Showcase:** `assets/examples.py` builds the example slides in `theme.pptx`, using every helper once in a whole slide. Read it to see how helpers compose; it is not a set of layouts to pick from.

To change the theme itself, edit `assets/theme.py`, run it, and commit the new `theme.pptx`.

## Step 4: Check

1. `python {skill-dir}/assets/check.py deck.pptx`: measures every text box with Inter's real metrics (overflow, titles over two lines, table cells that wrap, single words on a last line), and reports shapes off the grid, past the bottom margin, overlapping or shadowed. Fix everything it reports, or (in a restyle) list it for the user.
2. `python {skill-dir}/assets/aesthetics.py deck.pptx`: renders the deck and measures each slide after AeSlides: fill (crowding), whitespace (large empty regions) and balance (a lean to one side), and flags slides past the thresholds (design-guidelines.md, principle 6). Fix the flagged slides.
3. Render and look at every page: `FONTCONFIG_FILE={skill-dir}/assets/fonts.conf soffice --headless --convert-to pdf deck.pptx` (the config points LibreOffice at the bundled Inter). For each page: is the focal point obvious, does the eye move in reading order, is anything crowded or empty, does it match the deck's other slides of its kind? Fix and render again.
4. Academic checks:

```
□ The titles alone tell the argument; each is one sentence of at most two lines
□ The research question has its own slide, by slide 3
□ One exhibit per slide, supporting its title, with the finding marked on it
□ Text above a figure stacks; columns only for tall figures or parallel items
□ Every borrowed claim, figure or number has a footnote; the References slide lists them all
□ Conclusions is the last main slide, with contact and a link or QR code; no "Thank you" slide
□ Backup slides answer the likeliest questions
□ No pitch-style slides: no hero numbers, superlatives or slogans
□ Every card passes the card gate; slide count fits the time slot
□ Missing figures listed for the user
```

## Hand-over

Tell the user:
- How to open it in Google Slides: upload the .pptx to Google Drive, then File → Save as Google Slides. Keynote and PowerPoint need Inter installed, or they draw the text in Times New Roman: install `{skill-dir}/assets/Inter-Regular.ttf` and `Inter-Italic.ttf` (on a Mac, copy them to `~/Library/Fonts/`).
- Which figures are missing, which slides `check.py` still flags, and (for a restyle) which slides were split.
- To rehearse aloud to time and finish 1–2 minutes early, bring the deck as .pptx and PDF in two places, and test it on the venue's projector.
