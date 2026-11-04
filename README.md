# academic-skill

A Claude Code plugin of skills for academic papers.

- `academic-figure`: style rules for academic paper figures made with matplotlib or seaborn, delivered as cells in a `figures/figures.ipynb` notebook.
- `academic-slides`: argument, structure and design rules for research talks, built with python-pptx from a ready-made theme (`skills/academic-slides/assets/theme.pptx`) as .pptx files that open cleanly in Google Slides. Preview: `docs/academic-slides-theme.pdf`.

## Install

```
/plugin install academic-skill --marketplace bigohofone/academic-skill
```

On older Claude Code versions:

```
/plugin marketplace add bigohofone/academic-skill
/plugin install academic-skill@academic-skill
```

Update with `/plugin marketplace update academic-skill`.

## License

MIT, except the bundled Inter fonts (SIL Open Font License, see `skills/academic-figure/assets/Inter-LICENSE.txt` and `skills/academic-slides/assets/Inter-LICENSE.txt`).

`academic-slides` was inspired by [academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill). Its argument guidelines draw on David Hirshleifer's "Best Practices for Academic Presentations" (2026), itself prompted by [David Kasten's post](https://x.com/David_Kasten/status/2027063865742442521), and on Naegle (2021), "Ten simple rules for effective presentation slides", *PLOS Computational Biology*.
