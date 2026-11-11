# Task: reward-distribution

Draw the distribution of reward-model scores of responses from three policies as violin plots (for an ICLR paper). `reward-distribution.json`: `rewards[policy]`, the scores of 400 responses each. The point: the scores are bimodal (bad and good responses), and our policy moves most responses into the high-reward mode.

The data is synthetic, made to look like typical results. Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `reward-distribution.png` and `reward-distribution.pdf`.
