---
name: academic-slides
description: "Builds research talks as .pptx decks that open cleanly in Google Slides, from a ready-made Academic theme with python-pptx. Use it for any talk about research, such as a paper at a conference, a seminar, a thesis or dissertation defense, a grant pitch, a group meeting, or a guest lecture, and whenever the user asks for slides about a paper, study, dataset or thesis. It plans the argument, the order of slides, the titles, the citations and the timing, then fills the theme's layouts."
---

# Academic Slides

Every deck starts from `{skill-dir}/assets/theme.pptx` (`{skill-dir}` is this skill's base directory). The theme holds the colors, fonts, sizes, line spacing, page numbers and slide layouts, plus one example slide per layout, so a deck script only picks layouts and fills placeholders. Read this file and [content.md](content.md) before creating anything.

## Step 1: Plan the argument

1. Pick one argument the talk can make in its time slot, and a narrative spine ([content.md](content.md) §1).
2. Write a slide-by-slide outline: layout, title, and the one piece of evidence on it.
3. Ghost deck test: read only the titles in order. They must tell the whole argument. Fix the outline until they do.
4. Show the outline to the user and wait for agreement when the deck has more than 10 slides or the content is complex.

**Titles:** content slides get a story title, one sentence stating the takeaway, with the number in it when there is one. **At most two lines** at the theme's 24 pt (about 90 characters); cut words rather than shrink the font. No em dash. Structural slides (title, section headers, conclusions, references) get a plain label.

## Step 2: Build with python-pptx

Write one Python script in the user's project with the helpers in `{skill-dir}/assets/slides.py`:

```python
import sys; sys.path.insert(0, "{skill-dir}/assets")
from slides import new_deck, add_slide, figure, add_card, save

prs = new_deck()  # the theme without its example slides
add_slide(prs, "Title", "Early childhood program effects last into adulthood",
          p1=["Society for Labor Economics · May 2025", "Jane Smith¹, John Doe²", "¹ University of X · ² Lab Y"])
add_slide(prs, "Title and Content", "Long-run effects of early childhood programs are rarely measured",
          p1=[[("Short-run gains: ", True), ("confirmed by meta-analyses¹", False)]],  # (text, semibold) runs
          p13=["¹ Heckman et al. (2013), Science."])
s = add_slide(prs, "Figure and Text", "Program children earn 18% more by age 35",
              p2=["Largest gain in the bottom quartile: 28%"], p13=["Source: SSA earnings records."])
figure(s, 1, "figures/earnings.png")
save(prs, "talk.pptx")  # also deletes empty placeholders
```

`p<idx>` fills the placeholder with that index:

| Layout | Placeholders (grid columns) | Use for |
|--------|-----------------------------|---------|
| Title | 0 title (0–11); 1 venue · date, authors, affiliations, one per line (0–9) | Title slide |
| Title and Content | 0 title; 1 bullets (0–11); 13 footnote (0–9) | Motivation, conclusions, any bullet slide |
| Statement | 0 title; 1 research question on a card (1–10); 2 contribution (0–11); 13 footnote | Research question |
| Two Content | 0 title; 1 header, 2 bullets (0–5); 3 header, 4 bullets (6–11); 13 footnote | Methods ("Design" / "Outcomes"), discussion ("Interpretation" / "Main limitation") |
| Figure and Text | 0 title; 1 figure (0–7); 2 points (8–11); 13 footnote | Results |
| Section Header | 1 "Part 2"; 0 section name | Section dividers for decks over 15 slides, and "Appendix" |
| References | 0 title; 1 references, one per paragraph | References |
| Title Only | 0 title | A slide drawn by hand |
| Blank | none | A full-slide image |

**Grid:** the 9 in between the 0.5 in side margins is 12 columns of 0.567 in with 0.2 in gutters, and every layout's x and width come from it. Shapes drawn by hand also start and end on column edges: `box(first_column, span, y, h)` in `slides.py` gives their position in inches. To change the theme itself, edit `assets/theme.py`, run it, and commit the new `theme.pptx`.

- **Don't restyle text.** Fonts, sizes, colors, bullets and the 1.15 line spacing come from the theme. Set only the lead-in runs to Inter SemiBold (`(text, True)` runs) and `hyperlink` on links (`run.hyperlink.address = url`).
- **Type rules:** body text at least 16 pt (footnotes and page numbers are the only smaller text). Weights are Inter Regular and Inter SemiBold only, never bold: titles, headers and lead-ins use the `Inter SemiBold` font. All text is dark navy, never black.
- **Cards:** draw a card only with `add_card(slide, first_column, span, y, h)`, so every card has the same fill, 16 pt corners, no border, and sits on the grid. Add the card first, then the text on it. **Never nest cards**: no card inside or overlapping another card.
- **Body text:** at most about 40 words and three or four short bullets per slide. Bullet slides are the minority; a number or a comparison belongs in a figure.
- A user's or institution's template replaces the theme when they give one.

## Step 3: Figures

This skill does not make figures; use the user's own image files.

- Put a figure in a picture placeholder with `figure()`. It keeps the image's aspect ratio, fits it inside the placeholder, and aligns it to the left margin. Never stretch or crop a figure.
- If the user has no file yet, leave the picture placeholder empty and list which slides need which figure.
- Mark the key finding in the body text next to the figure.

## Step 4: Google Slides compatibility

The deck must look the same after uploading to Google Drive and opening in Google Slides:

- **Font:** Inter is a Google Font; don't introduce others. Google Slides replaces fonts it doesn't have.
- **No autofit:** the theme turns it off, because Google Slides never shrinks text. Keep text short enough to fit its placeholder.
- **Equations** as images or plain Unicode text (`R² = 0.91`, `p < 0.001`); Office equations don't survive the import.
- **Images, not native charts:** a native pptx chart becomes an uneditable picture in Google Slides.
- **Solid fills only;** no gradients, shadows, 3D, animations, transitions, audio, video or embedded objects.
- Hyperlinks and speaker notes (`slide.notes_slide.notes_text_frame.text`) survive; use them.

## Step 5: Check

1. Automatic checks: `python {skill-dir}/assets/check.py deck.pptx`. It currently measures every text box with Inter's real metrics and reports overflow and titles over two lines. Fix every report by cutting words or splitting the slide, never by shrinking the font.
2. Render: `FONTCONFIG_FILE={skill-dir}/assets/fonts.conf soffice --headless --convert-to pdf deck.pptx` (the config points LibreOffice at the bundled Inter), then look at every page for overlap and figures too small to read.
3. Run the academic checks:

```
□ Every content slide has a story title of at most two lines; the titles alone tell the argument
□ The research question has its own slide, by slide 3
□ One exhibit per results slide, with the key finding stated next to it
□ Every borrowed claim, figure or number has a footnote on its slide
□ A References slide lists every source cited
□ Conclusions is the last slide before references and appendix, with contact details
□ No "Thank you" or blank slide after Conclusions
□ Slide count fits the time slot (content.md §5)
□ No empty placeholders; figures keep their aspect ratio
□ Missing figures listed for the user
```

Tell the user how to open it in Google Slides: upload the .pptx to Google Drive, then open it with Google Slides (File → Save as Google Slides to convert). Keynote and PowerPoint need Inter installed, or they draw the text in Times New Roman: install `{skill-dir}/assets/Inter-Regular.ttf` and `Inter-SemiBold.ttf` (on a Mac, copy them to `~/Library/Fonts/`).
