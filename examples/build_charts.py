"""Run every chart-type example and copy its SVG to docs/charts/img/with/, the landing site's Charts page.

Run from anywhere: python examples/build_charts.py
"""

import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE / "chart-types/scripts"
SITE = HERE.parent / "docs/charts/img/with"


def run(script):
    result = subprocess.run([sys.executable, script.name], cwd=SCRIPTS, capture_output=True, text=True)
    warned = [line for line in result.stderr.splitlines() if "Warning" in line or "Error" in line]
    return script.stem, result.returncode, warned


if __name__ == "__main__":
    with ThreadPoolExecutor() as pool:
        results = list(pool.map(run, sorted(SCRIPTS.glob("*.py"))))
    for name, code, warned in results:
        svg = HERE / "chart-types/outputs" / f"{name}.svg"
        if code == 0 and (SITE / f"{name}.svg").exists():
            shutil.copy(svg, SITE / f"{name}.svg")
        print(f"{name}: {'failed' if code else 'ok'}{', ' + str(len(warned)) + ' warnings' if warned else ''}")
