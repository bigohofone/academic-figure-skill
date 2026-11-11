# Task: data-mixture

Draw how our three-stage curriculum changes the pretraining data mixture over training (ICML, single column). `data-mixture.json`: `steps`, and `shares[domain]` (fraction of tokens at each step; the domains sum to 1). The stages switch at 30k and 70k steps. The point: the share of web text falls from 62% to 40% while code and math grow.

The data is synthetic, made to look like a real experiment. Deliverable: the figure in `figures/figures.ipynb` with its caption, as `data-mixture.png` and `data-mixture.pdf`.
