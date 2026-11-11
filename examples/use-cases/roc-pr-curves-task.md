# Task: roc-pr-curves

Please redraw Fig. 1 from "Membership Inference Attacks From First Principles" by Nicholas Carlini, Steve Chien, Milad Nasr, Shuang Song, Andreas Terzis, and Florian Tramèr (IEEE S&P 2022; arXiv 2021), https://arxiv.org/abs/2112.03570. The figure plots ROC curves, on log-log axes, for nine membership inference attacks against a CIFAR-10 model.

The data is in `roc-pr-curves.json`:
- `curves`: one entry per attack, in the paper's legend order. `method` is the attack name ("Ours" is the paper's LiRA attack). `attack_accuracy_percent` is the attack's balanced accuracy, which the paper shows in the legend as "(acc=…%)". `fpr` and `tpr` are the ROC points (false-positive rate and true-positive rate), in plotting order.
- `chance_line`: the diagonal TPR = FPR, which marks a random-guess attack.
- `x_label`, `y_label`, `x_scale`, `y_scale`, `x_limits`, `y_limits`: the paper's axes. Both axes are log scale from 1e-5 to 1. Some curves begin just left of 1e-5, and the axes clip those points.
- The Ye et al. curve starts at FPR ≈ 5e-3, as it does in the paper.

What the figure shows: an attack's average accuracy says little about how it performs at low false-positive rates. In the paper's words, "the attack of Yeom et al. has a high accuracy (59.5%) yet fails completely at low FPRs, and the attack of Long et al. has a much lower accuracy (53.5%) but achieves higher success rates at low FPRs." The paper's attack (LiRA, "Ours") is about 10× more powerful than prior attacks at low FPRs and also strictly dominates them on aggregate metrics.

Column width: single column (the figure sits in one column of the two-column paper).

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `roc-pr-curves.png` and `roc-pr-curves.pdf`.
