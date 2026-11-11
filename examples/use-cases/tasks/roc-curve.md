# Task: roc-curve

Draw a ROC curve (line chart) from `roc-curve.json`, for an ICLR paper.

Data: `methods`: four AI-text detectors, each with `name` (Ours: W/ P and Ours: W/o P are two variants of ours, with and without the golden prompt; OpenAI and GPTZero are baselines), `fpr` and `tpr`, the false and true positive rates tracing its ROC curve as a step curve.

Deliverable: the figure in the figures folder with its caption, as `roc-curve.png` and `roc-curve.pdf`.
