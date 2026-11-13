"""Rebuild the paper examples with the current design: redraw each paper's figures, compile the paper as
published and with the new figures, and write the pages whose figures changed to docs/papers/.

Each paper lives in examples/papers/{arXiv id}/: paper.json names the figures it replaces (and any edit to a
figure's includegraphics line, for a figure split in two), figures/ holds
one script per figure (reading data/), and src/ caches the arXiv TeX source (not in git).

Run from anywhere: python examples/papers/build.py [arXiv id ...]
Needs tectonic, and pymupdf for the page images.
"""

import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
SITE = HERE.parents[1] / "docs/papers"


def fetch_source(paper_id, src):
    request = urllib.request.Request(f"https://arxiv.org/src/{paper_id}", headers={"User-Agent": "paper-figure-redraw/1.0"})
    data = urllib.request.urlopen(request).read()
    src.mkdir(parents=True)
    tarfile.open(fileobj=io.BytesIO(data)).extractall(src)


def prepare(tree, spec, paper_id):
    """Make a source tectonic can compile, the same for both builds: figures it cannot read (EPS) replaced by
    vector crops of the arXiv PDF, and the includegraphics lines pointed at the crops (`prepare` in paper.json)."""
    prep = spec.get("prepare", {})
    if prep.get("crops"):
        request = urllib.request.Request(f"https://arxiv.org/pdf/{paper_id}", headers={"User-Agent": "paper-figure-redraw/1.0"})
        published = pymupdf.open(stream=urllib.request.urlopen(request).read(), filetype="pdf")
        for crop in prep["crops"]:
            rect = pymupdf.Rect(crop["rect"])
            doc = pymupdf.open()
            doc.new_page(width=rect.width, height=rect.height).show_pdf_page(doc[0].rect, published, crop["page"] - 1, clip=rect)
            doc.save(tree / crop["target"])
    for edit in prep.get("edits", []):
        tex = tree / edit["file"]
        text = tex.read_text()
        if edit["from"] not in text:
            raise RuntimeError(f"{paper_id}: prepare edit not found in {edit['file']}: {edit['from']!r}")
        tex.write_text(text.replace(edit["from"], edit["to"]))


def compile_paper(tree, main):
    # arXiv sources target pdflatex; XeTeX stops on harmless clashes (xcolor options), so it goes on past them
    result = subprocess.run(["tectonic", "-X", "compile", "-Z", "continue-on-errors", main], cwd=tree, capture_output=True, text=True)
    pdf = tree / Path(main).with_suffix(".pdf")
    if not pdf.exists():
        raise RuntimeError(f"{tree}: no PDF\n{result.stderr[-2000:]}")
    return pymupdf.open(pdf)


def page_of(doc, caption):
    words = " ".join(caption.split())
    for n, page in enumerate(doc, 1):
        if words in " ".join(page.get_text().split()):
            return n
    raise RuntimeError(f"caption not found: {caption!r}")


def write_svg(page, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page.get_svg_image(text_as_path=True))
    return f"{path.relative_to(SITE).as_posix()}?v={hashlib.sha1(path.read_bytes()).hexdigest()[:10]}"


def build(paper_dir):
    spec = json.loads((paper_dir / "paper.json").read_text())
    paper_id = paper_dir.name
    src, out, work = paper_dir / "src", paper_dir / "out", paper_dir / "build"
    if not src.exists():
        fetch_source(paper_id, src)
    out.mkdir(exist_ok=True)
    for figure in spec["figures"]:
        result = subprocess.run([sys.executable, figure["script"]], cwd=paper_dir / "figures", capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f"{paper_id}/{figure['script']}:\n{result.stderr[-2000:]}")
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(src, work / "original")
    prepare(work / "original", spec, paper_id)
    shutil.copytree(work / "original", work / "redrawn")
    for figure in spec["figures"]:
        shutil.copy(out / Path(figure["script"]).with_suffix(".pdf"), work / "redrawn" / figure["target"])
    # a figure split in two (one takeaway each) needs its includegraphics line changed; captions stay
    for edit in spec.get("edits", []):
        tex = work / "redrawn" / edit["file"]
        text = tex.read_text()
        if edit["from"] not in text:
            raise RuntimeError(f"{paper_id}: edit not found in {edit['file']}: {edit['from']!r}")
        tex.write_text(text.replace(edit["from"], edit["to"]))
    original = compile_paper(work / "original", spec["main"])
    redrawn = compile_paper(work / "redrawn", spec["main"])

    shutil.rmtree(SITE / paper_id, ignore_errors=True)
    pages, seen = [], set()
    for figure in spec["figures"]:
        o, r = page_of(original, figure["caption"]), page_of(redrawn, figure["caption"])
        if (o, r) in seen:
            continue
        seen.add((o, r))
        pages.append({"n": r, "on": o,
                      "o": write_svg(original[o - 1], SITE / paper_id / "original" / f"p{o}.svg"),
                      "r": write_svg(redrawn[r - 1], SITE / paper_id / "redrawn" / f"p{r}.svg")})
    pages.sort(key=lambda p: p["n"])
    width, height = redrawn[0].rect.width, redrawn[0].rect.height
    entry = {"id": paper_id, "pages": pages, "ratio": f"{width} / {height}", "credit": spec["credit"],
             "title": spec["title"], "venue": spec["venue"], "order": spec["order"]}
    (SITE / paper_id / "pages.json").write_text(json.dumps(entry))
    return entry


def write_viewer():
    """The papers page's viewer: its list and page data, from every built paper's pages.json."""
    papers = sorted((json.loads(f.read_text()) for f in SITE.glob("*/pages.json")), key=lambda p: p["order"])
    write_viewer_page(SITE / "index.html", papers, "")


def write_viewer_page(page, papers, prefix):
    html = page.read_text()
    buttons = "".join(f'<button type="button" role="tab" data-i="{i}" aria-selected="{str(i == 0).lower()}"><b>{p["title"]}</b>'
                      f'<span>{p["venue"]}</span></button>' for i, p in enumerate(papers))
    html = re.sub(r'(<div class="pv-list" role="tablist" aria-label="Paper">).*?(</div>)', lambda m: m.group(1) + buttons + m.group(2), html, flags=re.S)
    data = [{"id": p["id"], "ratio": p["ratio"], "credit": p["credit"],
             "pages": [{**pg, "o": prefix + pg["o"], "r": prefix + pg["r"]} for pg in p["pages"]]} for p in papers]
    html = re.sub(r"const PAPERS = \[.*?\];", lambda m: "const PAPERS = " + json.dumps(data) + ";", html, flags=re.S)
    page.write_text(html)


def export_hero():
    """The landing page's before / after shows the first paper's figures alone, without their pages: its
    redrawn figures as SVG in docs/hero/with/ (docs/hero/without/ holds the same figures drawn without the skill)."""
    first = min((json.loads(f.read_text()) for f in SITE.glob("*/pages.json")), key=lambda p: p["order"])["id"]
    hero = SITE.parent / "hero" / "with"
    hero.mkdir(parents=True, exist_ok=True)
    for pdf in (HERE / first / "out").glob("*.pdf"):
        (hero / pdf.with_suffix(".svg").name).write_text(pymupdf.open(pdf)[0].get_svg_image(text_as_path=True))


if __name__ == "__main__":
    wanted = set(sys.argv[1:])
    dirs = [d for d in sorted(HERE.iterdir()) if (d / "paper.json").exists() and (not wanted or d.name in wanted)]
    with ThreadPoolExecutor() as pool:
        built = list(pool.map(build, dirs))
    for p in built:
        print(p["id"], "pages", [(x["on"], x["n"]) for x in p["pages"]])
    write_viewer()
    export_hero()
