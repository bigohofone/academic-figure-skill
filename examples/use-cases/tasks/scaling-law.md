# Task: scaling-law

Draw a line chart of a scaling law with its fit from `scaling-law.json`, for an ICLR paper (single-column layout, 5.5 in text width).

Data: `non_embedding_parameters` (model size N) and `test_loss` (nats per token, same order) for Transformer language models, and `fit`: the power law L = (N / `N_c`)^-`alpha_N` fitted to them, drawn over `plotted_N_range`.

Deliverable: the figure in the figures folder with its caption, as `scaling-law.png` and `scaling-law.pdf`.
