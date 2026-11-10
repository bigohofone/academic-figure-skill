# Task: draw Figures 2 and 6 of an ICML paper (DAPO, LLM reinforcement learning)

Data: `dapo.json` in your working folder. Every curve is `{"step": [...], "value": [...]}`; the x axis is always training steps.
Keys used here: fig2a → {"w/ Clip-Higher", "w/o Clip-Higher"}; fig6 → {"w/ Dynamic Sampling", "w/o Dynamic Sampling"}.

Figures:

2. Clip-Higher ablation: accuracy on AIME (avg@32) over training, with and without Clip-Higher. One panel, single column of the ICML two-column template.
6. Training progress before and after applying dynamic sampling on a baseline setting (AIME avg@32). 1.5 column wide.

Deliverable: one PNG per figure named `fig2.png` and `fig6.png`, plus the code that produced them.
Python: use `uv run -p 3.12 --with <packages> ...` (installing packages this way is allowed).
