# Task: dapo

Draw two line charts from `dapo.json`, for an ICLR paper.

Data: every curve is `{"step": [...], "value": [...]}`: AIME accuracy (avg@32, 0–1) over training steps.
- `fig2a`: "w/ Clip-Higher" (ours) and "w/o Clip-Higher" (ablation), one chart, `dapo-fig2`.
- `fig6`: "w/ Dynamic Sampling" (ours) and "w/o Dynamic Sampling" (ablation), one chart, `dapo-fig6`.

Deliverable: each figure in the figures folder with its caption, as `dapo-fig2.png`/`.pdf` and `dapo-fig6.png`/`.pdf`.
