# Task: draw the 7 figures of an ICML paper (DAPO, LLM reinforcement learning)

Data: `dapo.json` in your working folder. Every curve is `{"step": [...], "value": [...]}`.
Keys: fig1 → {"DAPO avg@32", "DAPO pass@32", "DAPO cons@32"}; fig2a/fig2b → {"w/ Clip-Higher", "w/o Clip-Higher"};
fig3a, fig3b → single curve; fig4a/fig4b → {"w/ token-level loss", "w/o token-level loss"};
fig5a/fig5b → {"w/ overlong filtering", "w/o overlong filtering"}; fig6 → {"w/ Dynamic Sampling", "w/o Dynamic Sampling"};
fig7a..fig7d → single curve. The x axis is always training steps.

Figures (all span the full text width of the ICML two-column template, except Figure 6, which is 1.5 column wide):

1. AIME 2024 scores of DAPO on Qwen2.5-32B base over training (avg@32, pass@32, cons@32). For reference, DeepSeek-R1-Zero-Qwen-32B reaches 47 on AIME 2024 using 10,000 (10k) steps; DAPO surpasses it with 50% of the steps.
2. Clip-Higher ablation, two panels: (a) accuracy on AIME (avg@32), (b) entropy of the actor model's generation probabilities.
3. Two panels: (a) mean up-clipped probability, (b) proportion of samples with an accuracy of 1.
4. Token-level policy gradient loss ablation, two panels: (a) entropy of generation probabilities, (b) average length of responses.
5. Overlong filtering ablation, two panels: (a) performance on AIME (avg@32), (b) entropy of actor model.
6. Training progress before and after applying dynamic sampling on a baseline setting (AIME avg@32).
7. Training dynamics of DAPO, four panels: (a) mean response length, (b) reward score, (c) generation entropy, (d) mean probability.

Deliverable: one PNG per figure named `fig1.png` … `fig7.png`, plus the code that produced them.
Python: use `uv run -p 3.12 --with <packages> ...` (installing packages this way is allowed).
