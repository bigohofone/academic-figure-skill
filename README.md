# academic-figure-skill

A Claude Code skill for academic paper figures made with matplotlib or seaborn: sized to the venue's column width, print typography, color-blind-safe colors, value labels where the paper makes its claim, and a paper-style caption, delivered as cells in a `figures/figures.ipynb` notebook in your project.

## Design

How figures look is defined in [`DESIGN.md`](skills/academic-figure/assets/DESIGN.md), in the [DESIGN.md](https://github.com/google-labs-code/design.md) format: tokens (colors, type sizes, spacing, line widths) in its front matter, then Overview, Colors, Typography, Layout, Shapes, Components (the chart types) and Do's and Don'ts. The skill copies it into your project's `figures/`, and `paper.use_design()` reads its tokens to set matplotlib's style, so editing `figures/DESIGN.md` restyles every figure of that paper. [`SKILL.md`](skills/academic-figure/SKILL.md) is the workflow: takeaway, chart type, notebook, caption and checks.

## Examples

Figures from published papers, redrawn by Claude Code subagents with a clean context: once without any skill and once following this skill. Both get only the figure's data, read from the paper's vector paths, and the same task file describing the figure. Each figure is shown at its printed size (1 in = 96 px), so at 100% browser zoom it appears as it would on the page. Open an example to see both versions; click a figure to open it full size.

<details>
<summary><b>Line chart</b> (learning curve): DAPO, Figure 2 (left panel, single column)</summary>

[DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) (Yu et al., 2025)

**Without skill**

<a href="examples/dapo-fig2-without-skill.png"><img src="examples/dapo-fig2-without-skill.png" width="310"></a>

**With skill**

<a href="examples/dapo-fig2-with-skill.png"><img src="examples/dapo-fig2-with-skill.png" width="312"></a>

</details>

<details>
<summary><b>Line chart</b> (learning curve): DAPO, Figure 6 (1.5 column)</summary>

[DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) (Yu et al., 2025)

**Without skill**

<a href="examples/dapo-fig6-without-skill.png"><img src="examples/dapo-fig6-without-skill.png" width="437"></a>

**With skill**

<a href="examples/dapo-fig6-with-skill.png"><img src="examples/dapo-fig6-with-skill.png" width="486"></a>

</details>

<details>
<summary><b>Line chart</b> (4 × 4 grid, log₂ x axis): Does RL Really Incentivize Reasoning Capacity?, Figure 2 (double column)</summary>

[Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?](https://arxiv.org/abs/2504.13837) (Yue et al., 2025)

**Without skill**

<a href="examples/rlvr-fig2-without-skill.png"><img src="examples/rlvr-fig2-without-skill.png" width="647"></a>

**With skill**

<a href="examples/rlvr-fig2-with-skill.png"><img src="examples/rlvr-fig2-with-skill.png" width="648"></a>

</details>

<details>
<summary><b>Histogram</b> (counts per bin): Does RL Really Incentivize Reasoning Capacity?, Figure 5 (single column)</summary>

[Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?](https://arxiv.org/abs/2504.13837) (Yue et al., 2025)

**Without skill**

<a href="examples/rlvr-fig5-without-skill.png"><img src="examples/rlvr-fig5-without-skill.png" width="308"></a>

**With skill**

<a href="examples/rlvr-fig5-with-skill.png"><img src="examples/rlvr-fig5-with-skill.png" width="312"></a>

</details>

<details>
<summary><b>Box plot</b> (with every point): Does RL Really Incentivize Reasoning Capacity?, Figure 6, Problem 1 only (single column)</summary>

[Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?](https://arxiv.org/abs/2504.13837) (Yue et al., 2025)

**Without skill**

<a href="examples/rlvr-fig6-without-skill.png"><img src="examples/rlvr-fig6-without-skill.png" width="312"></a>

**With skill**

<a href="examples/rlvr-fig6-with-skill.png"><img src="examples/rlvr-fig6-with-skill.png" width="312"></a>

</details>

## Chart types

Guidelines for the 12 most common chart types in arXiv papers ([PaperUnPlot](https://tabular-data-analysis.github.io/tada2026/papers/TaDA26_13.pdf), Table 2), one file each in `skills/academic-figure/`. Each example was drawn by a Claude Code subagent with a clean context following the skill, from synthetic data and a task file in [`examples/chart-types/`](examples/chart-types), at printed size.

<details>
<summary><b>Line chart</b>: ROC curve, Scaling curve</summary>

Guidelines: [`line-chart.md`](skills/academic-figure/line-chart.md)

**ROC curve**

<a href="examples/chart-types/roc-curve.png"><img src="examples/chart-types/roc-curve.png" width="312"></a>

**Scaling curve**

<a href="examples/chart-types/scaling-curve.png"><img src="examples/chart-types/scaling-curve.png" width="312"></a>

</details>

<details>
<summary><b>Bar chart</b>: Grouped bar chart, Stacked bar chart</summary>

Guidelines: [`bar-chart.md`](skills/academic-figure/bar-chart.md)

**Grouped bar chart**

<a href="examples/chart-types/grouped-bar-chart.png"><img src="examples/chart-types/grouped-bar-chart.png" width="312"></a>

**Stacked bar chart**

<a href="examples/chart-types/stacked-bar-chart.png"><img src="examples/chart-types/stacked-bar-chart.png" width="312"></a>

</details>

<details>
<summary><b>Scatter plot</b>: Accuracy against model size, Pareto front, t-SNE embedding</summary>

Guidelines: [`scatter-plot.md`](skills/academic-figure/scatter-plot.md)

**Accuracy against model size, Pareto front**

<a href="examples/chart-types/accuracy-vs-parameters.png"><img src="examples/chart-types/accuracy-vs-parameters.png" width="312"></a>

**t-SNE embedding**

<a href="examples/chart-types/t-sne.png"><img src="examples/chart-types/t-sne.png" width="312"></a>

</details>

<details>
<summary><b>Box plot</b>: Grouped box plot</summary>

Guidelines: [`box-plot.md`](skills/academic-figure/box-plot.md)

**Grouped box plot**

<a href="examples/chart-types/grouped-box-plot.png"><img src="examples/chart-types/grouped-box-plot.png" width="312"></a>

</details>

<details>
<summary><b>Heatmap</b>: Confusion matrix, Hyperparameter grid</summary>

Guidelines: [`heatmap.md`](skills/academic-figure/heatmap.md)

**Confusion matrix**

<a href="examples/chart-types/confusion-matrix.png"><img src="examples/chart-types/confusion-matrix.png" width="312"></a>

**Hyperparameter grid**

<a href="examples/chart-types/hyperparameter-grid.png"><img src="examples/chart-types/hyperparameter-grid.png" width="312"></a>

</details>

<details>
<summary><b>Histogram</b>: Overlaid histograms</summary>

Guidelines: [`histogram.md`](skills/academic-figure/histogram.md)

**Overlaid histograms**

<a href="examples/chart-types/confidence-histogram.png"><img src="examples/chart-types/confidence-histogram.png" width="312"></a>

</details>

<details>
<summary><b>Error bar plot</b>: Means over seeds with ±1 std</summary>

Guidelines: [`error-bar-plot.md`](skills/academic-figure/error-bar-plot.md)

**Means over seeds with ±1 std**

<a href="examples/chart-types/error-bar-plot.png"><img src="examples/chart-types/error-bar-plot.png" width="312"></a>

</details>

<details>
<summary><b>Area chart</b>: Stacked area chart of data shares</summary>

Guidelines: [`area-chart.md`](skills/academic-figure/area-chart.md)

**Stacked area chart of data shares**

<a href="examples/chart-types/data-mixture.png"><img src="examples/chart-types/data-mixture.png" width="312"></a>

</details>

<details>
<summary><b>Contour plot</b>: Loss landscape</summary>

Guidelines: [`contour-plot.md`](skills/academic-figure/contour-plot.md)

**Loss landscape**

<a href="examples/chart-types/loss-landscape.png"><img src="examples/chart-types/loss-landscape.png" width="312"></a>

</details>

<details>
<summary><b>Radar chart</b>: Benchmark profiles</summary>

Guidelines: [`radar-chart.md`](skills/academic-figure/radar-chart.md)

**Benchmark profiles**

<a href="examples/chart-types/radar-chart.png"><img src="examples/chart-types/radar-chart.png" width="312"></a>

</details>

<details>
<summary><b>Pie chart</b>: Donut chart of a dataset's composition</summary>

Guidelines: [`pie-chart.md`](skills/academic-figure/pie-chart.md)

**Donut chart of a dataset's composition**

<a href="examples/chart-types/dataset-composition.png"><img src="examples/chart-types/dataset-composition.png" width="312"></a>

</details>

<details>
<summary><b>Violin plot</b>: Bimodal reward distributions</summary>

Guidelines: [`violin-plot.md`](skills/academic-figure/violin-plot.md)

**Bimodal reward distributions**

<a href="examples/chart-types/reward-distribution.png"><img src="examples/chart-types/reward-distribution.png" width="312"></a>

</details>

## Install

In Claude Code:

```
/plugin marketplace add bigohofone/academic-figure-skill
/plugin install academic-figure@academic-figure-skill
```

Update with `/plugin marketplace update academic-figure-skill`.

Without the plugin system, copy the skill folder into your skills directory:

```
git clone https://github.com/bigohofone/academic-figure-skill
cp -r academic-figure-skill/skills/academic-figure ~/.claude/skills/
```

For slides in the same style, see [academic-slides-skill](https://github.com/bigohofone/academic-slides-skill).

## License

MIT, except the bundled Inter fonts (SIL Open Font License, see `skills/academic-figure/assets/Inter-LICENSE.txt`).
