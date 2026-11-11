# Task: attention-map

Please make a figure from `attention-map.json`. It is Figure 3(a) of "Neural Machine Translation by Jointly Learning to Align and Translate" by Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio (ICLR 2015), https://arxiv.org/abs/1409.0473. The figure shows the soft alignment (attention weights) found by RNNsearch-50 when it translates one English sentence into French.

The data:
- `source_tokens`: the 14 words of the English source sentence (one per column).
- `target_tokens`: the 15 words of the generated French translation (one per row).
- `weights`: a 15 x 14 matrix. `weights[i][j]` is the weight alpha_ij that the model gives to source word j when it generates target word i. Each row sums to about 1.

What the paper wants this figure to show: the alignment between English and French is mostly monotonic, with strong weights along the diagonal, but the model also finds non-trivial, non-monotonic alignments. Adjectives and nouns are ordered differently in the two languages: the model aligns [zone] with [Area], jumping over [European] and [Economic], and then looks one word back at a time to finish the phrase [zone économique européenne].

Width: the original is one panel of a 2 × 2 grid in a single-column layout; in ICLR this is half the text width (2.75 in).

Venue: ICLR (single-column layout, 5.5 in text width). Size the figure for it, whatever the original paper's layout was.

Deliverable: the figure in the figures folder with its caption, as `attention-map.png` and `attention-map.pdf`.
