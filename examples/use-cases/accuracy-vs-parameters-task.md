# Task: accuracy-vs-parameters

Draw MMLU accuracy against model size for open models and ours (ICML, single column). `accuracy-vs-parameters.json`: `models[name]` → `params_b` (billions of parameters) and `mmlu` (accuracy 0–1). Our models are the two whose names start with "Ours". The point: our models are on the accuracy–size Pareto front, Ours-8B matching models several times larger.

The data is synthetic, made to look like typical results. Deliverable: the figure in `figures/figures.ipynb` with its caption, as `accuracy-vs-parameters.png` and `accuracy-vs-parameters.pdf`.
