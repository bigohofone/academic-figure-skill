# Task: win-rate

Draw a win rate chart (horizontal stacked bars) from `win-rate.json`, for an ICLR paper.

Data: `opponents` (five baselines that LIMA, ours, is compared against, in a fixed order), `categories` ("LIMA wins", "Tie", "LIMA Loses"), and one list per category aligned with `opponents`: the percentage of 300 test prompts with that outcome (each opponent's three values sum to 100).

Deliverable: the figure in the figures folder with its caption, as `win-rate.png` and `win-rate.pdf`.
