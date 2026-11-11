# Task: confusion-matrix

Please make a confusion-matrix figure from the data in `confusion-matrix.json`.

The data comes from Figure 5 of "Yelp Review Rating Prediction: Machine Learning and Deep Learning Models" by Zefang Liu (2020), https://arxiv.org/abs/2012.06690. That figure is the confusion matrix of a Random Forest classifier (500 trees, TF-IDF features) that predicts a restaurant review's star rating (1 to 5) from its text, measured on the test set.

Data keys:
- `labels`: the five classes, the Yelp star ratings "1" to "5" (1 = worst, 5 = best).
- `matrix`: a 5x5 matrix. Rows are the true star rating, columns the predicted rating. Each value is the fraction of reviews with that true rating that were predicted as that column's rating, so each row sums to about 1. The values are given exactly as printed in the paper (2 significant digits).
- `row_axis` / `column_axis`: the axis names ("True label", "Predicted label").

What the figure shows: the paper uses it to show that the Random Forest's predictions are skewed towards the two extremes. 1-star and 5-star reviews are mostly classified correctly (0.82 and 0.76), but 2-star reviews are confused with 1-star about as often as they are classified correctly (0.38 vs 0.37), and 4-star reviews are confused with 5-star about as often (0.37 vs 0.39). The paper explains this as 1- and 2-star reviews sharing negative sentiment words and 4- and 5-star reviews sharing positive ones, which a tree-based model handles poorly.

Width: the original spans one column of a two-column layout; in ICLR this is half the text width (2.75 in).

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in the figures folder with its caption, as `confusion-matrix.png` and `confusion-matrix.pdf`.
