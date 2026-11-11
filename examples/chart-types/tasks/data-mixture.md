# Task: data-mixture

Draw how our three-stage curriculum changes the pretraining data mixture over training as a stacked area chart (for an ICLR paper). `data-mixture.json`: `steps`, and `shares[domain]` (fraction of tokens at each step; the domains sum to 1). The stages switch at 30k and 70k steps. The point: the share of web text falls from 62% to 40% while code and math grow.

The data is synthetic, made to look like a real experiment. Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in the figures folder with its caption, as `data-mixture.png` and `data-mixture.pdf`.
