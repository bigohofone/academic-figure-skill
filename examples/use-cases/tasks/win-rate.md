# Task: win-rate

Please make a figure from `win-rate.json`. It is Figure 1 of Zhou et al., "LIMA: Less Is More for Alignment" (Chunting Zhou, Pengfei Liu, Puxin Xu, Srini Iyer, Jiao Sun, Yuning Mao, Xuezhe Ma, Avia Efrat, Ping Yu, Lili Yu, Susan Zhang, Gargi Ghosh, Mike Lewis, Luke Zettlemoyer, Omer Levy; 2023; https://arxiv.org/abs/2305.11206). The paper's caption: "Human preference evaluation, comparing LIMA to 5 different baselines across 300 test prompts."

Data (`win-rate.json`):
- `opponents`: the five baselines LIMA (a 65B LLaMa fine-tuned on only 1,000 curated examples) is compared against, in the paper's order from top to bottom: Alpaca 65B, DaVinci003, BARD (April), Claude (April), GPT-4 (April).
- `categories`: the three outcomes, named as in the paper: "LIMA wins", "Tie", "LIMA Loses".
- One list per category, aligned with `opponents`: the percentage of the 300 test prompts on which crowd workers preferred LIMA's response, judged neither better, or preferred the baseline's. Each opponent's three values sum to 100.

What it shows: despite training on 52 times more data, Alpaca 65B produces less preferable outputs than LIMA, and so does DaVinci003, even though it was trained with RLHF. Bard, Claude and GPT-4 generally beat LIMA, but LIMA's response is equal or better in 58%, 46% and 43% of cases respectively, a non-trivial share. The paper takes this as support for its Superficial Alignment Hypothesis: almost all knowledge is learned in pretraining, and a small set of examples suffices for alignment.

Width: the paper is single-column; this figure sits in a half-text-width minipage, side by side with Figure 2.

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `win-rate.png` and `win-rate.pdf`.
