# academic-figure-skill

A Claude Code skill for academic paper figures made with matplotlib or seaborn: sized to the venue's column width, print typography, color-blind-safe colors, value labels where the paper makes its claim, and a paper-style caption, delivered as cells in a `figures/figures.ipynb` notebook in your project.

## Examples

Figures from published papers, redrawn by Claude Code subagents with a clean context: once without any skill and once following this skill. Both get only the figure's data, read from the paper's vector paths, and the same task file describing the figure. Each figure is shown at its printed size (1 in = 96 px), so at 100% browser zoom it appears as it would on the page. Open an example to see both versions; click a figure to open it full size.

<details>
<summary><b>Trend</b> (line plot): DAPO, Figure 2 (left panel, single column)</summary>

[DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) (Yu et al., 2025)

**Without skill**

<a href="examples/dapo-fig2-without-skill.png"><img src="examples/dapo-fig2-without-skill.png" width="310"></a>

**With skill**

<a href="examples/dapo-fig2-with-skill.png"><img src="examples/dapo-fig2-with-skill.png" width="312"></a>

</details>

<details>
<summary><b>Trend</b> (line plot): DAPO, Figure 6 (1.5 column)</summary>

[DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) (Yu et al., 2025)

**Without skill**

<a href="examples/dapo-fig6-without-skill.png"><img src="examples/dapo-fig6-without-skill.png" width="437"></a>

**With skill**

<a href="examples/dapo-fig6-with-skill.png"><img src="examples/dapo-fig6-with-skill.png" width="486"></a>

</details>

<details>
<summary><b>Trend</b> (4 × 4 grid of line plots, log₂ x axis): Does RL Really Incentivize Reasoning Capacity?, Figure 2 (double column)</summary>

[Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?](https://arxiv.org/abs/2504.13837) (Yue et al., 2025)

**Without skill**

<a href="examples/rlvr-fig2-without-skill.png"><img src="examples/rlvr-fig2-without-skill.png" width="647"></a>

**With skill**

<a href="examples/rlvr-fig2-with-skill.png"><img src="examples/rlvr-fig2-with-skill.png" width="648"></a>

</details>

<details>
<summary><b>Distribution</b> (histogram of counts per bin): Does RL Really Incentivize Reasoning Capacity?, Figure 5 (single column)</summary>

[Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?](https://arxiv.org/abs/2504.13837) (Yue et al., 2025)

**Without skill**

<a href="examples/rlvr-fig5-without-skill.png"><img src="examples/rlvr-fig5-without-skill.png" width="308"></a>

**With skill**

<a href="examples/rlvr-fig5-with-skill.png"><img src="examples/rlvr-fig5-with-skill.png" width="312"></a>

</details>

<details>
<summary><b>Distribution</b> (box plot with points): Does RL Really Incentivize Reasoning Capacity?, Figure 6, Problem 1 only (single column)</summary>

[Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?](https://arxiv.org/abs/2504.13837) (Yue et al., 2025)

**Without skill**

<a href="examples/rlvr-fig6-without-skill.png"><img src="examples/rlvr-fig6-without-skill.png" width="312"></a>

**With skill**

<a href="examples/rlvr-fig6-with-skill.png"><img src="examples/rlvr-fig6-with-skill.png" width="312"></a>

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
