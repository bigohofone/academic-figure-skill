# Task: stacked-bar-chart

Draw how each model's answers on MATH split into correct answers and three error types (ICML, single column). `stacked-bar-chart.json`: `models`, `categories`, and `shares[category]` (fraction of answers per model, same order as `models`; each model's shares sum to 1). The point: our 7B model's errors are mostly reasoning errors, and it makes the fewest format errors.

The data is synthetic, made to look like typical results. Deliverable: the figure in `figures/figures.ipynb` with its caption, as `stacked-bar-chart.png` and `stacked-bar-chart.pdf`.
