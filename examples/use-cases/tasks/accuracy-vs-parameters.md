# Task: accuracy-vs-parameters

Please redraw Figure 1 of "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks" by Mingxing Tan and Quoc V. Le (ICML 2019), https://arxiv.org/abs/1905.11946v3. The figure plots ImageNet top-1 accuracy against the number of parameters for many ConvNets. The data is in `accuracy-vs-parameters.json`, one entry per plotted model:

- `model`: model name.
- `label_in_figure`: the text label next to the point in the original figure, or `null` if the point has no label (EfficientNet-B1, B2 and one NAS model).
- `params_millions`: number of parameters, in millions (x axis).
- `top1_accuracy`: ImageNet top-1 accuracy in % (y axis).
- `family`: `EfficientNet` (the proposed models B0 to B7, joined by a line), `hand-designed (dotted gray front)` and `NAS (dashed blue front)` (baseline models joined by a line in the original), or `other (no line)` (baseline models shown as single points).
- `source`: `Table 2` if the value is from the paper's Table 2, or `read from plot` if it was read from the vector points of the original figure (rounded to 0.1).

What the figure shows, from the paper: "Figure 1 summarizes the ImageNet performance, where our EfficientNets significantly outperform other ConvNets." The scaled EfficientNet models reach better accuracy with an order of magnitude fewer parameters than other ConvNets. EfficientNet-B7 reaches the state-of-the-art 84.4% top-1 accuracy while being 8.4x smaller than GPipe (not plotted), and EfficientNet-B1 is 7.6x smaller than ResNet-152.

The figure is single-column in the paper.

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `accuracy-vs-parameters.png` and `accuracy-vs-parameters.pdf`.
