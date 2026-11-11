# Task: rlvr

Draw three figures, for an ICLR paper (single-column layout, 5.5 in text width).

- `rlvr-fig2`, a grid of line charts (rows models, columns benchmarks) from `rlvr.json`: keyed by benchmark, then model, then "Base" or "RL", each `{"k": [...], "pass": [...]}`, the pass@k (0–1) of a base model and its RL-trained version over the number of samples k. Benchmarks: AIME24, MATH500, Minerva, Olympiad. Models: Qwen2.5-7B, Qwen2.5-14B, Qwen2.5-32B, LLaMA-3.1-8B.
- `rlvr-fig5`, a histogram of counts per named bin from `rlvr-fig5.json`: `bins` (12 accuracy intervals, "0.0", "(0.0,0.1]", …, "1.0") and, for "Base" and "RL", the number of Minerva problems whose per-problem accuracy falls in each bin.
- `rlvr-fig6`, a box plot from `rlvr-fig6.json`, "Problem 1" only: `["Problem 1"][name]`, perplexities of individual responses for four groups: PPL_Base(Y_Base), PPL_Base(Y_RL), PPL_RL(Y_RL), PPL_Base(Y_GT).

Deliverable: each figure in the figures folder with its caption, as `rlvr-fig2.png`/`.pdf`, `rlvr-fig5.png`/`.pdf`, `rlvr-fig6.png`/`.pdf`.
