# Task: stacked-bar-chart

Please redraw Figure 4 from "Why Do Multi-Agent LLM Systems Fail?" by Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez and Ion Stoica (NeurIPS 2025 Datasets and Benchmarks Track; arXiv 2025, https://arxiv.org/abs/2503.13657). The figure shows how failures in MAST-Data split across the 14 MAST failure modes for 7 multi-agent systems.

The data is in `stacked-bar-chart.json`:
- `systems`: the 7 multi-agent systems (AppWorld, HyperAgent, AG2, ChatDev, MetaGPT, MagenticOne, OpenManus). Each one gets a bar.
- `failure_categories`: the 3 failure categories (FC1 System Design Issues, FC2 Inter-Agent Misalignment, FC3 Task Verification). Each category lists its failure modes by id (e.g. "1.3") and name (e.g. "Step Repetition").
- `failure_counts[system][mode_id]`: how many failures of that mode were annotated in that system's first 30 traces (210 traces in total). The unit is a count of failures ("# Failures").
- `panel_titles_as_printed`: each category's share of all 601 annotated failures, as printed in the paper (41.8%, 36.9%, 21.3%). These shares match the counts.

In the paper the figure has one group per failure category, with a bar for each system. Each bar is stacked by that category's failure modes.

What the paper uses it for: the figure shows each system's own failure profile. The caption says it is not meant as a performance comparison across MAS, because the tasks and benchmarks differ between systems. Failures spread across all three categories: system design issues are the largest share, then inter-agent misalignment, then task verification. The text points out that systems with explicit verifiers, such as MetaGPT and ChatDev, generally show fewer total failures, so explicit checks help. A verifier alone is not enough, though.

Column width: the paper uses a single-column layout, and the figure spans the full text width.

Original caption: "Figure 4: Distribution of failure in MAST-Data with MAST labels on total 210 traces. This plot visualizes the failure distributions of the first 30 traces for each system. As the specific tasks and benchmarks may differ across the MAS configurations shown, these results are intended to illustrate system-specific failure profiles rather than to serve as a performance comparison across MAS."

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in `figures/figures.ipynb` with its caption, as `stacked-bar-chart.png` and `stacked-bar-chart.pdf`.
