# academic-figure: before / after

Every figure from [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) (Yu et al., 2025): the original from the paper first, then the same data redrawn with `academic-figure`.

The data is read from the vector paths in the paper's PDF, so the redraws plot the exact same values. Both versions are shown at their printed width (1 in = 96 px), so at 100% browser zoom they appear at roughly real size. The originals are cropped from the paper's page, and the redraws use ICML widths: double column (6.75 in, 648 px) and 1.5 column (5.0625 in, 486 px).

Redraws are made by [`academic-figure.py`](academic-figure.py) from [`academic-figure/dapo.json`](academic-figure/dapo.json):

```
uv run -p 3.12 --with matplotlib --with tol-colors python examples/academic-figure.py
```

## On the page

Each original page (left) next to the same page with the redrawn figure dropped in at the width LaTeX would give it (`\textwidth`; 1.5 column for Figure 6), with the text below moved to fit. Pages are shown at about half size; click one to open it full size. Made by [`academic-figure-pages.py`](academic-figure-pages.py):

```
uv run -p 3.12 --with pymupdf python examples/academic-figure-pages.py
```

| Original | Redrawn |
|---|---|
| <a href="academic-figure/page1-before.png"><img src="academic-figure/page1-before.png" width="400"></a> | <a href="academic-figure/page1-after.png"><img src="academic-figure/page1-after.png" width="400"></a> |
| <a href="academic-figure/page2-before.png"><img src="academic-figure/page2-before.png" width="400"></a> | <a href="academic-figure/page2-after.png"><img src="academic-figure/page2-after.png" width="400"></a> |
| <a href="academic-figure/page3-before.png"><img src="academic-figure/page3-before.png" width="400"></a> | <a href="academic-figure/page3-after.png"><img src="academic-figure/page3-after.png" width="400"></a> |
| <a href="academic-figure/page4-before.png"><img src="academic-figure/page4-before.png" width="400"></a> | <a href="academic-figure/page4-after.png"><img src="academic-figure/page4-after.png" width="400"></a> |
| <a href="academic-figure/page5-before.png"><img src="academic-figure/page5-before.png" width="400"></a> | <a href="academic-figure/page5-after.png"><img src="academic-figure/page5-after.png" width="400"></a> |
| <a href="academic-figure/page6-before.png"><img src="academic-figure/page6-before.png" width="400"></a> | <a href="academic-figure/page6-after.png"><img src="academic-figure/page6-after.png" width="400"></a> |
| <a href="academic-figure/page7-before.png"><img src="academic-figure/page7-before.png" width="400"></a> | <a href="academic-figure/page7-after.png"><img src="academic-figure/page7-after.png" width="400"></a> |

## Figure 1: AIME 2024 scores of DAPO

<img src="academic-figure/fig1-before.png" width="577">

<img src="academic-figure/fig1-after.png" width="648">

## Figure 2: Clip-Higher

<img src="academic-figure/fig2-before.png" width="627">

<img src="academic-figure/fig2-after.png" width="648">

## Figure 3: Up-clipped probability and prompts with accuracy 1

<img src="academic-figure/fig3-before.png" width="627">

<img src="academic-figure/fig3-after.png" width="648">

## Figure 4: Token-level policy gradient loss

<img src="academic-figure/fig4-before.png" width="627">

<img src="academic-figure/fig4-after.png" width="648">

## Figure 5: Overlong filtering

<img src="academic-figure/fig5-before.png" width="627">

<img src="academic-figure/fig5-after.png" width="648">

## Figure 6: Dynamic sampling (1.5 column)

<img src="academic-figure/fig6-before.png" width="439">

<img src="academic-figure/fig6-after.png" width="486">

## Figure 7: Training dynamics of DAPO

<img src="academic-figure/fig7-before.png" width="627">

<img src="academic-figure/fig7-after.png" width="648">
