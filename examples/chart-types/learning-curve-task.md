# Task: learning-curve

Draw validation accuracy over training on CIFAR-100 for our augmentation, Mixup and the baseline (for an ICLR paper). `learning-curve.json`: `epochs`, and `accuracy[method]`, a list of 5 runs (seeds), each with one accuracy per epoch. The point: ours converges to a higher accuracy than both, consistently over seeds.

The data is synthetic, made to look like a real experiment. Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `learning-curve.png` and `learning-curve.pdf`.
