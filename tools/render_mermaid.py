#!/usr/bin/env python3
"""Render all Mermaid diagrams in a GitBook-style book to SVG (for the mobile reader).

Extracts ```mermaid blocks in SUMMARY.md order and renders them with mermaid-cli,
pointing puppeteer at a system Chrome (CHROME_BIN env or auto-detected). Chunked +
retried because a single large mmdc pass can crash headless Chrome. Diagrams that
still fail are simply left out — build_mobile_book.py shows their source as fallback.
Writes d-1.svg .. d-N.svg into --svg-out. Exits 0 even if some/all fail, so local
mobile-reader builds still work; pass --strict (CI does) to exit 1 instead.
"""
import os, re, sys, glob, time, shutil, subprocess, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--book-dir", default=".")
ap.add_argument("--svg-out", required=True)
ap.add_argument("--chunk", type=int, default=25)
ap.add_argument("--strict", action="store_true",
                help="exit 1 if Chrome is missing or any diagram fails to render")
a = ap.parse_args()
BOOK, SVG = os.path.abspath(a.book_dir), os.path.abspath(a.svg_out)
shutil.rmtree(SVG, ignore_errors=True); os.makedirs(SVG)

# extract mermaid sources in SUMMARY order (same order build_mobile_book.py uses)
srcs, seen = [], set()
sm = os.path.join(BOOK, "SUMMARY.md")
order = []
for line in open(sm, encoding="utf-8"):
    m = re.match(r'^\s*[-*]\s+\[.*?\]\(([^)]+?)\)', line)
    if m and m.group(1).endswith(".md"):
        p = m.group(1).strip()
        if p not in seen and os.path.isfile(os.path.join(BOOK, p)):
            seen.add(p); order.append(p)
for p in order:
    txt = open(os.path.join(BOOK, p), encoding="utf-8").read()
    for mm in re.finditer(r'```mermaid[ \t]*\n(.*?)\n[ \t]*```', txt, re.DOTALL):
        srcs.append(mm.group(1))
N = len(srcs)
print(f"mermaid diagrams found: {N}")
if N == 0:
    sys.exit(0)

chrome = os.environ.get("CHROME_BIN") or next(
    (shutil.which(n) for n in ["google-chrome-stable","google-chrome","chromium-browser","chromium","chrome"] if shutil.which(n)), None)
if not chrome:
    msg = "no Chrome found -> all diagrams would fall back to source"
    if a.strict:
        print(f"Mermaid rendering failed: {msg}", file=sys.stderr); sys.exit(1)
    print(f"WARNING: {msg}"); sys.exit(0)
print(f"using Chrome: {chrome}")
pptr = os.path.join(SVG, "_pptr.json")
open(pptr, "w").write('{"executablePath":"%s","args":["--no-sandbox","--disable-gpu","--disable-dev-shm-usage"]}' % chrome)
rc = os.path.join(SVG, "_rc.json"); open(rc, "w").write('{"theme":"default"}')
MMDC = shutil.which("mmdc") or "mmdc"

def render(indices):
    cm = os.path.join(SVG, "_chunk.md")
    open(cm, "w", encoding="utf-8").write("\n".join("```mermaid\n"+srcs[i]+"\n```\n" for i in indices))
    subprocess.run(["pkill", "-f", "enable-automation"], capture_output=True)  # only puppeteer Chrome
    time.sleep(1)
    subprocess.run([MMDC, "-i", cm, "-o", os.path.join(SVG, "_c.svg"), "-p", pptr, "-c", rc, "-b", "transparent"],
                   capture_output=True, text=True)
    for j, i in enumerate(indices, 1):
        sp = os.path.join(SVG, f"_c-{j}.svg")
        if os.path.isfile(sp) and os.path.getsize(sp) > 0:
            os.replace(sp, os.path.join(SVG, f"d-{i+1}.svg"))
    for st in glob.glob(os.path.join(SVG, "_c-*.svg")): os.remove(st)

def done(): return len([i for i in range(N) if os.path.isfile(os.path.join(SVG, f"d-{i+1}.svg"))])

for c in range((N + a.chunk - 1) // a.chunk):
    s, e = c*a.chunk, min(c*a.chunk + a.chunk, N)
    render(list(range(s, e)))
    print(f"  chunk {c+1}: {done()}/{N}", flush=True)
for att in range(4):
    miss = [i for i in range(N) if not os.path.isfile(os.path.join(SVG, f"d-{i+1}.svg"))]
    if not miss: break
    print(f"  retry {att+1}: {len(miss)} missing", flush=True)
    for b in range(0, len(miss), 8): render(miss[b:b+8])

for f in glob.glob(os.path.join(SVG, "*.json")) + glob.glob(os.path.join(SVG, "_chunk.md")):
    os.remove(f)
print(f"RENDERED {done()}/{N} diagrams")
if a.strict and done() < N:
    missing = [i + 1 for i in range(N) if not os.path.isfile(os.path.join(SVG, f"d-{i+1}.svg"))]
    print(f"Mermaid rendering failed for diagrams: {missing}", file=sys.stderr)
    sys.exit(1)
