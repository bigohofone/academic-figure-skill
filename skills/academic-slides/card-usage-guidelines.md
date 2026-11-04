# Card Usage Guidelines

Apply this before putting any card or box on a slide: a tinted, bordered or shadowed rectangle that wraps content. It adapts the Nielsen Norman Group's definition of cards (Laubheimer, 2016, "Cards: UI-Component Definition") to talks.

## Why slides are stricter

For NN/g, a card is a summary entry point into more detail, used to browse heterogeneous content; homogeneous items, comparisons and rankings are better as lists or tables. A slide has no clicks, so the entry-point job disappears and only grouping is left, and spacing and alignment already do most grouping. **The default is no card.** Use cards only when every gate below passes.

## The card gate (all must be true)

1. There are 2 to 4 items.
2. Each item is a **different kind of thing** with equal standing. A list of the same kind (five datasets, a list of baselines) fails.
3. There is no order, cause or flow between the items.
4. The audience doesn't need to compare numbers or attributes across items.
5. Each item fits a short heading plus at most 2 lines.
6. Spacing and alignment alone don't make the item boundaries obvious.

If any is false, don't use cards; use the default for the kind of content below.

**Exception: formal statements.** A theorem, lemma, proposition, corollary, definition or assumption always goes on its own card (`add_statement`), even alone on a slide: the card marks it as a formal statement, set apart from the talk's own words, and the same card on every slide makes them easy to find. Its proof or what it means goes below the card, not inside it.

**Exception: a dense slide.** When a slide has to hold a lot (several distinct blocks such as a definition, an example and a result), cards may separate the blocks even if items 4 and 5 fail: one card per block, 2 to 4 blocks, equal widths in one row, nothing nested. This is grouping for readability, not decoration; if the blocks are short enough to separate with spacing and headers alone, do that instead.

## Default by kind of content

| Slide content | Default | Cards |
|---|---|---|
| Title, section slides | Type only (Title, Section Header layouts) | Never |
| Outline | Numbered list | Never |
| Motivation, problem | One strong sentence, plus a figure if needed | Never |
| Research question | Statement layout: its single box is the emphasis box (see below) | Never |
| Related work comparison | Table: rows are works, columns are attributes, our row highlighted | Never |
| Method pipeline, procedure, algorithm steps | Arrow flow diagram or numbered steps | Never |
| Model architecture, system design | Diagram | Never |
| Equations | Set apart with space; color the key symbols | Never |
| Theorems, lemmas, propositions, definitions, assumptions | One statement card each (`add_statement`): the label as its heading, the statement's text and equations inside | Always |
| Experimental setup (datasets, metrics, hyperparameters) | Table or short list | Never |
| Quantitative results, ablations | A chart with the finding marked, or a table with the best values in dark navy | Never |
| Qualitative results, several example images | Image grid with captions | Never |
| Contributions | Cards if the gate passes, otherwise a numbered list | If gated |
| Contrasting approaches or views (prior work vs ours) | 2 cards (columns 0–5 and 6–11) if the gate passes, otherwise two columns with subheadings | If gated |
| Limitations, future work | List | Never |
| Conclusions, take-home message | 2 or 3 takeaways, contact and a link or QR code | Never (one emphasis box allowed) |

## Visual rules for cards

- Draw cards only with `add_cards(slide, y, [(heading, [lines]), ...])` (slides.py): a light tint fill, 8 pt corners, **no shadow and no border**, equal widths on the grid, one height for the group, and the heading and lines laid out the same way in every card. Shadows and thin borders vanish or look muddy on projectors and screen shares.
- Spacing hierarchy: padding inside a card (equal on all four sides) < gap between cards < gap to the next block.
- Every card in a group has the same size, padding and inner structure (heading position, body position). Give them equal column spans on the same row.
- Cards sit in the vertical middle of the content area (`center_vertically`): a card row, a card grid, the Statement card, a theorem card with its points.
- One card group per slide.
- Nothing inside a card but its heading and text: no cards, tables or other boxes in a card.
- Never wrap a figure, chart or table in a card; they already have their own edges.
- Never wrap a whole slide body in one big box; the slide is the frame.

## Emphasis boxes are not cards

A single box that makes one conclusion or key result stand out is emphasis, not grouping. The Statement layout's card is one. Allow **at most one per slide, and few in the whole deck**: if every slide has one, nothing stands out. First try emphasis with color (dark navy, the theme blue); use a box only when that isn't enough.

## Separators instead of cards (weakest first)

Spacing → heading and type-size hierarchy → alignment on grid columns → a vertical or horizontal rule → a light tint panel → a card

Start with the weakest and stop as soon as the separation is clear.

## Self-check after the deck is built

1. Find every slide with a card or box.
2. For each, confirm it passes gate items 1 to 6. If any fails, switch to the default for its kind of content.
3. If cards appear on more than a small minority of slides, they were probably added out of habit; check again. (This ratio is a rule of thumb, not an NN/g standard.)
4. If the user explicitly asked for a card layout, follow it, and point out in one line where it fails the gate.

## Examples

- "Three contributions: a new dataset / a new loss function / a theoretical analysis": different kinds, 3 items, no order, no comparison → **3 cards.**
- "Contributions 1, 2, 3" that are all "we propose a module" and build on each other in order → **numbered list.**
- "Accuracy on 5 datasets": a comparison → **table.**
- "Preprocessing → encoder → decoder → postprocessing": an order → **flow diagram.**
- "Limits of prior methods vs our approach": two different views, each within 2 lines → **2 cards.** If either side runs to 4 lines or more, cut it or use Two Content.
- "Conclusion: the method improves X by Y%" → **a strong sentence, with one emphasis box if needed.**
