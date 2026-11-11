# Task: hyperparameter-surface

Draw validation loss over a sweep of learning rate and weight decay (13 × 13 runs, log-spaced) for our model (ICML, single column). `hyperparameter-surface.json`: `learning_rate`, `weight_decay`, and `val_loss[i][j]` at weight decay i and learning rate j. The point: the loss is lowest around learning rate 3e-4 and weight decay 6e-3, and training diverges at the largest learning rates.

The data is synthetic, made to look like a real experiment. Deliverable: the figure in `figures/figures.ipynb` with its caption, as `hyperparameter-surface.png` and `hyperparameter-surface.pdf`.
