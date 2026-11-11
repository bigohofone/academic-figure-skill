# Task: draw Figures 2, 5 and 6 of a NeurIPS paper ("Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?", LLM reinforcement learning)

Data, in your working folder:

- `rlvr.json` (Figure 2): `data[benchmark][model]` → {"Base", "RL"}, each curve `{"k": [...], "pass": [...]}`: pass@k (0–1) of a base model and its RLVR-trained counterpart (SimpleRL-Zoo, GRPO) over the number of samples k. Benchmarks: AIME24, MATH500, Minerva, Olympiad. Models: Qwen2.5-7B, Qwen2.5-14B, Qwen2.5-32B, LLaMA-3.1-8B. k runs to 1024 on AIME24 (to ~700 for LLaMA-3.1-8B, also on Olympiad) and to 128 elsewhere.
- `rlvr-fig5.json` (Figure 5): `bins` (12 accuracy intervals: "0.0", "(0.0,0.1]", …, "(0.9,1.0)", "1.0") and, per model ("Base", "RL"), the number of Minerva problems (272 in total) whose per-problem accuracy falls in each interval. Qwen2.5-7B base vs. its RLVR-trained version (SimpleRL-Zoo).
- `rlvr-fig6.json` (Figure 6): `data[problem][name]` → perplexities of individual responses, for two problems sampled from AIME24 ("Problem 1", "Problem 2"). Names: "PPL_Base(Y_Base)" (Qwen2.5-7B-Base's perplexity on its own 16 responses), "PPL_Base(Y_RL)" (the base model's perplexity on the 16 responses of the RL-trained model), "PPL_RL(Y_RL)" (the RL model on its own responses), "PPL_Base(Y_GT)" (the base model on 8 responses from OpenAI-o1). One of Problem 1's 8 o1 points overlapped another in the original and could not be recovered, so that group has 7.

Figures:

2. Pass@k curves of base models and their RLVR-trained counterparts across mathematical benchmarks. When k is small, RL-trained models outperform their base versions. However, as k increases to the tens or hundreds, base models consistently catch up and surpass RL-trained models.
5. Qwen2.5-7B accuracy histogram on Minerva. RLVR increases the frequency of high accuracies near 1.0 and reduces the frequency of low accuracies (e.g., 0.1, 0.2); however, it also increases the frequency at accuracy 0, i.e. more unsolvable problems.
6. Perplexity distribution of responses to Problem 1 only (the conditioning problem x is omitted from the labels), one panel filling the column. PPL_Base(Y_RL) closely matches the lower portion of the PPL_Base(Y_Base) distribution: responses of the RL model are ones the base model already tends to generate.

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: `fig2.png`, `fig5.png` and `fig6.png`, plus the code that produced them.
Python: use `uv run -p 3.12 --with <packages> ...` (installing packages this way is allowed).
