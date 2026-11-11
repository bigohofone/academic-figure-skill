# Task: hyperparameter-grid

Draw validation accuracy over a grid of learning rates and batch sizes (ICML, single column). `hyperparameter-grid.json`: `learning_rates`, `batch_sizes`, and `accuracy[i][j]` for learning rate i and batch size j. The point: the best setting is learning rate 1e-4 with batch size 32, and accuracy drops at the largest learning rate.

The data is synthetic, made to look like typical results. Deliverable: the figure in `figures/figures.ipynb` with its caption, as `hyperparameter-grid.png` and `hyperparameter-grid.pdf`.
