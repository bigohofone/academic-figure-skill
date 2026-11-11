# Task: reliability-diagram

Please redraw Figure 1 from Chuan Guo, Geoff Pleiss, Yu Sun and Kilian Q. Weinberger, "On Calibration of Modern Neural Networks", ICML 2017 (arXiv: https://arxiv.org/abs/1706.04599). It compares a 5-layer LeNet (left column) with a 110-layer ResNet (right column) on CIFAR-100. The top row shows confidence histograms and the bottom row shows reliability diagrams. The data is in `reliability-diagram.json`.

Data keys:
- `reliability_bin_edges`: the 10 equal-width confidence bins (0.0 to 1.0) used by the reliability diagrams.
- `histogram_bin_edges`: the 20 equal-width confidence bins (0.0 to 1.0) used by the histograms.
- `models.lenet` / `models.resnet`, each with:
  - `label`: the panel title (the dataset, CIFAR-100, goes on a second line).
  - `error_percent`: the test error printed in the reliability-diagram panel ("Error=44.9" and "Error=30.6").
  - `accuracy_per_bin`: the accuracy of each reliability bin (the "Outputs" bars).
  - `avg_confidence_per_bin`: the average confidence of each reliability bin. The "Gap" bar spans from the accuracy to this value. The ResNet's first bin (0.0 to 0.1) is empty and is stored as 0.
  - `fraction_of_samples_per_bin`: the fraction of test samples in each histogram bin (y axis "% of Samples", 0 to 1).
  - `avg_confidence_line`, `accuracy_line`: the vertical reference lines in the histogram ("Avg. confidence" and "Accuracy").

Both rows share the x axis "Confidence" from 0 to 1. Both y axes run from 0 to 1. The reliability diagrams include the identity diagonal (perfect calibration).

The paper's point: modern neural networks are no longer well calibrated. LeNet's average confidence closely matches its accuracy, and its bars line up roughly along the diagonal, so it is well calibrated. The ResNet is more accurate, but its average confidence is much higher than its accuracy, and its bars fall well below the diagonal, so it is overconfident.

Column width: one column. The original sits in one column of a two-column layout; in ICLR this is half the text width (2.75 in).

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `reliability-diagram.png` and `reliability-diagram.pdf`.
