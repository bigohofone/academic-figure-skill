# Task: attention-map

Draw a attention map (heatmap) from `attention-map.json`, for an ICLR paper (single-column layout, 5.5 in text width).

Data: `source_tokens` (14 English words), `target_tokens` (15 French words of the translation), and `weights`: 15 × 14, the attention weight on source word j when generating target word i (rows sum to about 1).

Deliverable: the figure in the figures folder with its caption, as `attention-map.png` and `attention-map.pdf`.
