# Task: error-bar-plot

Draw the accuracy of five fine-tuning methods on GLUE averaged over 5 seeds, with their spread (for an ICLR paper). `error-bar-plot.json`: `accuracy_per_seed[method]`, the accuracy of each of 5 seeds. The point: ours is best, ahead of full fine-tuning by more than the spread over seeds.

The data is synthetic, made to look like typical results. Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `error-bar-plot.png` and `error-bar-plot.pdf`.
