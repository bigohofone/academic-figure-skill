"""Run every chart-type example and copy its SVG to docs/charts/img/with/, the landing site's Charts page.

Run from anywhere: python examples/build_charts.py
"""

import hashlib
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE / "chart-types/scripts"
SITE = HERE.parent / "docs/charts/img/with"
PAGE = HERE.parent / "docs/charts/index.html"
ASSETS = HERE.parent / "skills/paper-figure/assets"


def newest(*paths):
    """The latest change time among these files and everything under these folders."""
    files = [f for p in paths for f in ([p] if p.is_file() else p.rglob("*")) if f.is_file() and f.suffix != ".pyc"]
    return max(f.stat().st_mtime for f in files)


def run(script):
    """Draw one chart unless its SVG is newer than the script, the data and the skill's assets."""
    svg = HERE / "chart-types/outputs" / f"{script.stem}.svg"
    if svg.exists() and svg.stat().st_mtime > newest(script, HERE / "chart-types/data", ASSETS):
        return script.stem, None, []
    result = subprocess.run([sys.executable, script.name], cwd=SCRIPTS, capture_output=True, text=True)
    warned = [line for line in result.stderr.splitlines() if "Warning" in line or "Error" in line]
    return script.stem, result.returncode, warned


if __name__ == "__main__":
    with ThreadPoolExecutor() as pool:
        results = list(pool.map(run, sorted(SCRIPTS.glob("*.py"))))
    for name, code, warned in results:
        svg = HERE / "chart-types/outputs" / f"{name}.svg"
        if code is None:
            print(f"{name}: unchanged")
            continue
        if code == 0 and (SITE / f"{name}.svg").exists():
            shutil.copy(svg, SITE / f"{name}.svg")
        print(f"{name}: {'failed' if code else 'ok'}{', ' + str(len(warned)) + ' warnings' if warned else ''}")
    # each image's ?v= is its content hash, so a browser that cached the old drawing loads the new one
    version = lambda m: f'{m.group(1)}?v={hashlib.sha1((PAGE.parent / m.group(1)).read_bytes()).hexdigest()[:10]}"'
    PAGE.write_text(re.sub(r'(img/with[a-z]*/[\w.-]+\.svg)(\?v=\w+)?"', version, PAGE.read_text()))
