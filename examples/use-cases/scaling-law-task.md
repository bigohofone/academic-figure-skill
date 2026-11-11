# Task: scaling-law

Redraw a scaling-law figure from a published paper using the paper's own plotted values in `scaling-law.json`.

**Paper:** Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, Dario Amodei. "Scaling Laws for Neural Language Models." 2020. https://arxiv.org/abs/2001.08361

**Figure:** Figure 1, right panel ("Parameters"): test loss of Transformer language models against model size, both axes on log scales, with the measured points and a power-law fit.

**Data (`scaling-law.json`):**
- `non_embedding_parameters`: model size N, number of parameters excluding embeddings (x axis).
- `test_loss`: test loss in nats per token on WebText2 for each model, trained to near convergence (y axis). Same order as `non_embedding_parameters`; the measured points are drawn connected by a line in the original.
- `fit`: the power-law fit shown in the figure and its printed formula, L = (N / 8.8·10^13)^-0.076 (`N_c`, `alpha_N`), and the N range over which the fit line is drawn (`plotted_N_range`).
- `axes`: axis labels and the y-axis tick values used in the original (2.4, 3.2, 4.0, 4.8, 5.6).

**What the figure shows (from the paper):** Language modeling performance improves smoothly as model size grows. When not bottlenecked by dataset size or compute, test loss follows a power law in the number of non-embedding parameters, L(N) = (N_c/N)^α_N with α_N ≈ 0.076, across about six orders of magnitude in N, with no sign of deviation at the upper end. For example, doubling the number of parameters makes the loss smaller by a factor 2^-α_N ≈ 0.95.

**Column width:** single column. The paper uses a one-column layout; the original Figure 1 spans the full text width as three panels, and this is the rightmost panel.

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `scaling-law.png` and `scaling-law.pdf`.
