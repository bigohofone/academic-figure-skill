# Scatter: relationship between two quantities, embeddings

One point per sample or model, two quantities against each other; or a 2-D embedding (t-SNE, UMAP). Read with `SKILL.md`, whose rules all still apply.

- **Scatter**: `ax.scatter(x, y, s=5, color=color, edgecolors="none", alpha=0.5)`, dots the size of the style's markers, translucent so dense regions read darker. Gridlines in both directions.
- **Embedding** (t-SNE, UMAP): as scatter, with ticks hidden and no gridlines (`ax.grid(False)`), and no axis labels.
