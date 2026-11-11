# Task: t-sne

Please redraw Figure 1(a) from "A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks" by Kimin Lee, Kibok Lee, Honglak Lee, and Jinwoo Shin (NeurIPS 2018), https://arxiv.org/abs/1807.03888. The panel is titled "Visualization by t-SNE". It shows a t-SNE embedding of the final (penultimate-layer) features of a ResNet-34 trained on CIFAR-10, for CIFAR-10 test samples. Points are colored by class.

Data is in `t-sne.json`. Its keys `class_1` to `class_10` are the ten CIFAR-10 classes, 100 points each. Each key has `x` and `y` lists with the 2-D t-SNE coordinates. The paper has no legend and does not say which color is which class, so the classes have no names. They are numbered in the order the paper draws them. The coordinates are in arbitrary t-SNE units, so the axes need no ticks or labels.

What the figure should show: the paper argues that the features of a pre-trained softmax classifier follow class-conditional Gaussian distributions. In its words, "all ten classes are clearly separated in the embedding space, which supports our intuition". This motivates the Mahalanobis-distance confidence score.

Width: the original is the first of three side-by-side subfigures across the text width of a single-column layout (NeurIPS); redrawn on its own, it takes half the ICLR text width (2.75 in).

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `t-sne.png` and `t-sne.pdf`.
