# Task: roc-curve

Please make an ROC curve figure from the data in `roc-curve.json`.

The data comes from Figure 8 (left panel, "Reddit") of "DNA-GPT: Divergent N-Gram Analysis for Training-Free Detection of GPT-Generated Text" by Xianjun Yang, Wei Cheng, Yue Wu, Linda Petzold, William Yang Wang, and Haifeng Chen (arXiv 2023, published at ICLR 2024), https://arxiv.org/abs/2305.17359. The figure is in Appendix B.7 ("Sliding window").

In the JSON, `methods` lists four AI-text detectors, each with its `name`, `fpr` (false positive rate) and `tpr` (true positive rate) lists. Together they trace the ROC curve as a step curve. `auc` is null because the paper's legend prints no AUC values. `chance_diagonal` is false because the paper draws no diagonal. The methods are:
- `Ours: W/ P`: DNA-GPT using the golden prompt (the question that produced the text).
- `Ours: W/o P`: DNA-GPT without the golden prompt.
- `OpenAI`: OpenAI's AI-text classifier (a baseline).
- `GPTZero`: GPTZero (a baseline).

The test texts start with gpt-3.5-turbo output and continue with human writing. DNA-GPT runs detection on a sliding window: it splits each text in two and flags it as AI-written if either half is flagged. The baselines cannot score the short halves, so they classify the whole text. The paper uses the figure to show that DNA-GPT, with or without the golden prompt, still clearly beats both baselines in this setting. That supports the sliding-window strategy for long texts that start with machine-generated text and are finished by a human.

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `roc-curve.png` and `roc-curve.pdf`.
