# academic-figure-skill

A Claude Code skill for academic paper figures made with matplotlib or seaborn: sized to the venue's column width, print typography, color-blind-safe colors, value labels where the paper makes its claim, and a paper-style caption, delivered as cells in a `figures/figures.ipynb` notebook in your project.

## Examples

Figures from published papers: as printed in the paper (left) and as redrawn by a Claude Code subagent with a clean context following the skill (right). The subagent gets only the figure's data, read from the paper's vector paths, and a task file describing the figure. Click a figure to see it full size.

<table>
<tr><th width="50%">Original</th><th width="50%">With skill</th></tr>
<tr><td colspan="2"><a href="https://arxiv.org/abs/2503.14476">DAPO</a> (Yu et al., 2025), Figure 2 (left panel, single column)<br>data: <a href="examples/dapo.json"><code>dapo.json</code></a>, task: <a href="examples/dapo-task.md"><code>dapo-task.md</code></a>, code: <a href="examples/dapo-with-skill.ipynb"><code>dapo-with-skill.ipynb</code></a></td></tr>
<tr><td><a href="examples/dapo-fig2-original.png"><img src="examples/dapo-fig2-original.png" width="100%"></a></td><td><a href="examples/dapo-fig2-with-skill.png"><img src="examples/dapo-fig2-with-skill.png" width="100%"></a></td></tr>
<tr><td colspan="2"><a href="https://arxiv.org/abs/2503.14476">DAPO</a> (Yu et al., 2025), Figure 6 (1.5 column)<br>data: <a href="examples/dapo.json"><code>dapo.json</code></a>, task: <a href="examples/dapo-task.md"><code>dapo-task.md</code></a>, code: <a href="examples/dapo-with-skill.ipynb"><code>dapo-with-skill.ipynb</code></a></td></tr>
<tr><td><a href="examples/dapo-fig6-original.png"><img src="examples/dapo-fig6-original.png" width="100%"></a></td><td><a href="examples/dapo-fig6-with-skill.png"><img src="examples/dapo-fig6-with-skill.png" width="100%"></a></td></tr>
<tr><td colspan="2"><a href="https://arxiv.org/abs/2504.13837">Does RL Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?</a> (Yue et al., 2025), Figure 2 (double column)<br>data: <a href="examples/rlvr.json"><code>rlvr.json</code></a>, task: <a href="examples/rlvr-task.md"><code>rlvr-task.md</code></a>, code: <a href="examples/rlvr-with-skill.ipynb"><code>rlvr-with-skill.ipynb</code></a></td></tr>
<tr><td><a href="examples/rlvr-fig2-original.png"><img src="examples/rlvr-fig2-original.png" width="100%"></a></td><td><a href="examples/rlvr-fig2-with-skill.png"><img src="examples/rlvr-fig2-with-skill.png" width="100%"></a></td></tr>
<tr><td colspan="2"><a href="https://arxiv.org/abs/2504.13837">Does RL Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?</a> (Yue et al., 2025), Figure 5 (single column)<br>data: <a href="examples/rlvr-fig5.json"><code>rlvr-fig5.json</code></a>, task: <a href="examples/rlvr-task.md"><code>rlvr-task.md</code></a>, code: <a href="examples/rlvr-with-skill.ipynb"><code>rlvr-with-skill.ipynb</code></a></td></tr>
<tr><td><a href="examples/rlvr-fig5-original.png"><img src="examples/rlvr-fig5-original.png" width="100%"></a></td><td><a href="examples/rlvr-fig5-with-skill.png"><img src="examples/rlvr-fig5-with-skill.png" width="100%"></a></td></tr>
<tr><td colspan="2"><a href="https://arxiv.org/abs/2504.13837">Does RL Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?</a> (Yue et al., 2025), Figure 6 (single column)<br>data: <a href="examples/rlvr-fig6.json"><code>rlvr-fig6.json</code></a>, task: <a href="examples/rlvr-task.md"><code>rlvr-task.md</code></a>, code: <a href="examples/rlvr-with-skill.ipynb"><code>rlvr-with-skill.ipynb</code></a></td></tr>
<tr><td><a href="examples/rlvr-fig6-original.png"><img src="examples/rlvr-fig6-original.png" width="100%"></a></td><td><a href="examples/rlvr-fig6-with-skill.png"><img src="examples/rlvr-fig6-with-skill.png" width="100%"></a></td></tr>
</table>

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
