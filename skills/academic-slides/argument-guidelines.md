# Argument Guidelines

What a research talk says and in what order: the audience, the storyline, titles, one job per slide, the slides every talk needs, and timing. Read it before planning a new talk. The order of priority in an academic talk is **argument > data > layout > aesthetics**: fix the argument before polishing anything else.

## Audience and scope

- Before outlining, settle three things with the user (or from the request): the venue and audience (specialists in the subfield, a broad department, a mixed panel), the time slot, and the one argument the talk makes.
- Specialists expect technical precision; a mixed room needs broader framing, fewer acronyms and more intuition before the formalism.
- **One argument.** Don't present the whole paper. Pick the part that can be made clearly in the time; everything else goes in the backup slides or stays in the paper.
- International audience: plain sentences, no idioms or culture-bound jokes.

## Storyline

- State the research question or central claim **by slide 3**, so the audience knows what everything after it is for.
- Follow one spine:
  - Situation → complication → resolution: what was known, what was missing or broken, what this work contributes.
  - Or: context → gap → approach → findings → implications.
- **One job per slide.** Each slide makes one point in the argument. If a slide does two things, split it into two slides.
- Each slide should make the next one feel like its natural consequence; if the transition needs a long spoken bridge, the order is wrong.
- Talks over ~15 minutes: a section slide (the Section Header layout, the section name alone) at the start of each part.

## Titles

- Every content slide's title is an **action title**: one plain sentence stating the takeaway, with the number when there is one.
  - Not "Results", but "Ours has the lowest WER on three of four test sets".
  - Not "Related work", but "Prior methods need labels or give up streaming".
- At most two lines (20 pt). If it needs more, the point isn't sharp yet.
- **Ghost deck test:** read only the titles in order. They must tell the whole argument; if they don't, fix the outline, not the slides.
- Structural slides (title, sections, outline, conclusions, references, backup) get plain labels.
- No hype: no superlatives, slogans or hero numbers (design-guidelines.md, principle 10).

## Exhibits: one insight per slide

- At most one exhibit per slide (a chart, table, diagram or equation), and it supports the title directly. If it doesn't, change the title or the exhibit.
- **Self-sufficient slide test:** would someone who can't hear the speaker still get the point? If not, mark the finding on the slide: a dotted `highlight()` on the part of the figure, the focal series in the theme blue, an `add_arrow`, or the finding stated as the first remark beside the exhibit.
- Prefer a chart to a table for results and trends; a table is right when exact values matter (main results, ablations).
- A figure with remarks: figure on the left, remarks on the right, in the order the speaker will point at them.
- Show only what the talk discusses. An exhibit you'll skip over doesn't belong on a slide.
- No decorative icons, clip art, stock photos or logos on content slides; logos at most on the title slide.

## Text on slides

- Full sentences only in titles. Body text is short parallel bullets, one idea each; drop articles and filler ("Intervention cut costs 23% (p < 0.01)").
- **Aim for about 40 words of body text per slide**; `check.py` reports a slide past 60 (titles, footnotes, tables and references not counted). Detail goes in the speaker notes or a backup slide.
- If the audience is reading, they aren't listening: the slide supports the talk, it doesn't replace it.

## Slides every talk needs

| Slide | What it holds |
|---|---|
| Title | The title as a claim or question; authors, affiliations, venue, date |
| Motivation | Why the problem matters: the real gap or open question |
| Research question | Stated precisely, on its own slide (the Statement layout), by slide 3 |
| Method | 1–2 slides of what the audience needs to judge the results; the rest to backup |
| Results | One finding per slide, the finding marked on the exhibit |
| Discussion | What the findings mean, their limits, back to the research question |
| Conclusions | 2–3 takeaways; contact details and a link or QR code to the paper; stays on screen during Q&A |
| References | Every source cited on the slides |
| Backup | Answers to the 3–5 likeliest questions, labelled "Appendix A: ...", after References |

Never end on a "Thank you" or blank slide: Conclusions stays up during Q&A.

## Time

- At most about one slide per minute: 12–14 content slides for a 15-minute slot, not counting title and references.
- Plan to finish 1–2 minutes early; nerves speed up the real talk, and overrunning eats the Q&A.
- Put what to say in each slide's speaker notes (`slide.notes_slide.notes_text_frame.text`): the transition into the slide and the one sentence the audience must remember.

## Before handing over

Tell the user, briefly: rehearse aloud to time; try it on one specialist and one outsider; bring the deck in two formats and places (the .pptx and a PDF, on a USB stick and in the cloud); test on the venue's projector; at the end ask for "questions or feedback", not just questions.
