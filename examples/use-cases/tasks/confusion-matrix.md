# Task: confusion-matrix

Draw a confusion matrix (heatmap) from `confusion-matrix.json`, for an ICLR paper (single-column layout, 5.5 in text width).

Data: `labels` (star ratings 1 to 5), and `matrix`: 5 × 5, rows the true rating, columns the predicted one, each value the fraction of the row's reviews (rows sum to about 1, values with 2 significant digits), from a Random Forest that predicts Yelp review ratings.

Deliverable: the figure in the figures folder with its caption, as `confusion-matrix.png` and `confusion-matrix.pdf`.
