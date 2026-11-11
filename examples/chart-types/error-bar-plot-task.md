# Task: error-bar-plot

Draw the accuracy of five fine-tuning methods on GLUE averaged over 5 seeds, with their spread (ICML, single column). `error-bar-plot.json`: `accuracy_per_seed[method]`, the accuracy of each of 5 seeds. The point: ours is best, ahead of full fine-tuning by more than the spread over seeds.

The data is synthetic, made to look like typical results. Deliverable: the figure in `figures/figures.ipynb` with its caption, as `error-bar-plot.png` and `error-bar-plot.pdf`.
