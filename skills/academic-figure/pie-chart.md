# Pie chart

The composition of one whole with few parts (two to six), when the message is the composition itself: a dataset's makeup by source, domain or language. Read with `DESIGN.md`, whose rules all still apply. With more parts, parts close in size, or several wholes to compare, draw a (stacked) bar chart instead (`bar-chart.md`): angles are hard to compare.

- Donut chart (a pie with its center cut out, the common form in papers): `ax.pie(shares, colors=series_colors, startangle=90, counterclock=False, wedgeprops=dict(width=0.4, edgecolor="white", linewidth=0.5))`; parts from 12 o'clock clockwise, largest first, a small "Other" part last.
- Name each part next to its wedge with its share, instead of a legend: `labels=[f"{name}\n{share:.0%}" for ...]`, `labeldistance=1.15`, 9 pt; parts under ~3% join "Other".
- The whole's total (e.g. "1.2M examples") in the center, 9 pt: `ax.text(0, 0, "1.2M\nexamples", ha="center", va="center")`.
- No axes, ticks or grid (`ax.pie` hides them). `fit_height` sizes the circle to the width; the `aspect` argument is ignored. Two wholes (train and test splits): two donuts side by side, titled.
