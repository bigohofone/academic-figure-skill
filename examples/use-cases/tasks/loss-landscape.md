# Task: loss-landscape

Draw a contour plot (lines only) from `loss-landscape.json`, for an ICLR paper (single-column layout, 5.5 in text width).

Data: `contour_lines`: polylines of a loss surface around a trained ResNet-56 on CIFAR-10, each with its `level` (training loss) and `xy` points in the two directions α and β (each −1 to 1, the trained minimizer at (0, 0)); `levels` (0.1 to 9.6 in steps of 0.5); `level_labels`: a position (`xy`) for each level's label.

Deliverable: the figure in the figures folder with its caption, as `loss-landscape.png` and `loss-landscape.pdf`.
