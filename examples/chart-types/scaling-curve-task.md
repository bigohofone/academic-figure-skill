# Task: scaling-curve

Draw validation loss against model size for dense models and our mixture-of-experts models (ICML, single column). `scaling-curve.json`: `params` (number of parameters, same for both), then the loss of each family at those sizes. The point: our MoE models reach a lower loss than dense models at every size.

The data is synthetic, made to look like typical results. Deliverable: the figure in `figures/figures.ipynb` with its caption, as `scaling-curve.png` and `scaling-curve.pdf`.
