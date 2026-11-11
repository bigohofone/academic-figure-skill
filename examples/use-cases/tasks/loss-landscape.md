# Task: loss-landscape

Please redraw a loss-landscape contour plot from a published paper, using the data in `loss-landscape.json`.

**Source:** Hao Li, Zheng Xu, Gavin Taylor, Christoph Studer, Tom Goldstein, "Visualizing the Loss Landscape of Neural Nets", NeurIPS 2018. arXiv: https://arxiv.org/abs/1712.09913 (v3). The figure is **Figure 5(b)**, "ResNet-56, 5.89%". It shows the 2-D loss surface of a ResNet-56 trained on CIFAR-10 (5.89% test error) around the trained minimizer.

**What the plot is:** the paper plots f(α, β) = L(θ* + αδ + βη). Here θ* is the trained minimizer, and δ, η are two random directions with filter-wise normalization. L is the loss over the CIFAR-10 training set. The center (0, 0) is the minimizer. The two axes are α and β, each from -1 to 1. The paper computed the surface on a 51 × 51 grid and drew it as labelled contour lines.

**Data keys (`loss-landscape.json`):**
- `x_range`, `y_range`: axis limits, [-1, 1] for α (x) and β (y).
- `levels`: the 20 contour levels, from 0.1 to 9.6 in steps of 0.5.
- `contour_lines`: a list of polylines. Each has a `level` (the loss value) and `xy`, a list of [α, β] points. One level can have several pieces. The pieces have small gaps where the paper placed inline level labels.
- `level_labels`: where the paper put each inline level label. Each has a `level` and an `xy` position in data coordinates. There are 53 labels.
- `test_error_percent`: 5.89, the test error the paper reports for this network in the panel title.
- `source`, `x_label`, `y_label`, `z_label`: descriptions of the source and the axes.

**What the figure shows (from the paper):** with skip connections, ResNet-56 has a smooth landscape around the minimizer. The minimizer sits in a wide, nearly convex basin with roughly elliptical contours. The paper compares this with ResNet-56-noshort (Figure 5(e)), whose landscape is chaotic and highly non-convex. In the paper's words, "residual connections prevent the transition to chaotic behavior as depth increases" and "prevent the explosion of non-convexity that occurs when networks get deep."

Width: the original is one panel of a 2 × 3 grid across the text width of a single-column layout (NeurIPS); redrawn on its own, it takes half the ICLR text width (2.75 in).

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `loss-landscape.png` and `loss-landscape.pdf`.
