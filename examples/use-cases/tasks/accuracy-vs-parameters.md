# Task: accuracy-vs-parameters

Draw a scatter plot from `accuracy-vs-parameters.json`, for an ICLR paper.

Data: one entry per ConvNet with `model`, `params_millions` (parameters, in millions), `top1_accuracy` (ImageNet top-1, %) and `family`: `EfficientNet` (ours, B0 to B7), two baseline groups whose models form a Pareto front (`hand-designed`, `NAS`), and `other` baselines.

Deliverable: the figure in the figures folder with its caption, as `accuracy-vs-parameters.png` and `accuracy-vs-parameters.pdf`.
