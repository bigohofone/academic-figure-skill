# Task: reliability-diagram

Draw a confidence histograms (top row) above reliability diagrams (bottom row), one column per model from `reliability-diagram.json`, for an ICLR paper (single-column layout, 5.5 in text width).

Data: `histogram_bin_edges` (20 confidence bins) and `reliability_bin_edges` (10 bins), and `models.lenet` / `models.resnet` (a 5-layer LeNet and a 110-layer ResNet on CIFAR-100), each with `label`, `error_percent` (test error), `fraction_of_samples_per_bin` (per histogram bin), `avg_confidence_line` and `accuracy_line` (the average confidence and the accuracy over all samples), `accuracy_per_bin` and `avg_confidence_per_bin` (per reliability bin; an empty bin is stored as 0).

Deliverable: the figure in the figures folder with its caption, as `reliability-diagram.png` and `reliability-diagram.pdf`.
