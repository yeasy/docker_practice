#!/usr/bin/env python3
"""Build a single self-contained, GitBook-style PAGED mobile reader — offline-robust.

Works even where JavaScript is disabled (iOS Files/Quick Look): pages are a readable
scroll by default; JS (Safari, Documents app, etc.) upgrades to one-page-at-a-time.
- Math: pandoc --mathml (native WebKit, no JS)
- Mermaid: PRE-RENDERED to static SVG (no JS, no mermaid.js) — pass --svg-dir
- TOC drawer: CSS checkbox hack (opens without JS); prev/next are static anchors
- Images/CSS embedded (--embed-resources) -> one offline file
"""
import argparse, os, re, subprocess, sys, posixpath

def esc(s):  return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def escattr(s): return s.replace("&","&amp;").replace('"',"&quot;").replace("<","&lt;")

def parse_summary(book_dir):
    items, seen = [], set()
    with open(os.path.join(book_dir, "SUMMARY.md"), encoding="utf-8") as f:
        for line in f:
            m = re.match(r'^##\s+(.+?)\s*$', line)
            if m: items.append(("part", m.group(1))); continue
            m = re.match(r'^(\s*)[-*]\s+\[(.*?)\]\(([^)]+?)\)', line)
            if m:
                indent, title, path = m.group(1), m.group(2).strip(), m.group(3).strip()
                if path.endswith(".md") and path not in seen and os.path.isfile(os.path.join(book_dir, path)):
                    seen.add(path)
                    items.append(("file", path, title, min(len(indent.replace("\t","  "))//2, 2)))
    return items

def fix_inline_dollar(text):
    def repl(m):
        s, e = m.start(), m.end(); inner = m.group(1)
        if "\n" in inner: return m.group(0)
        ls = text.rfind("\n", 0, s) + 1
        le = text.find("\n", e); le = len(text) if le < 0 else le
        if text[ls:s].strip() == "" and text[e:le].strip() == "": return m.group(0)
        return "$" + inner.strip() + "$"
    return re.sub(r'\$\$(.+?)\$\$', repl, text, flags=re.DOTALL)

def process_file(text, reldir, mermaid_store, path_to_id):
    def grab(m):
        idx = len(mermaid_store); mermaid_store.append(m.group(1))
        return f"\n\nMERMAIDZZ{idx}ZZ\n\n"
    text = re.sub(r'```mermaid[ \t]*\n(.*?)\n[ \t]*```', grab, text, flags=re.DOTALL)
    text = fix_inline_dollar(text)
    text = re.sub(r'\[!\[[^\]]*\]\(https?://[^)]*\)\]\([^)]*\)', '', text)
    text = re.sub(r'!\[[^\]]*\]\(https?://[^)]*\)', '', text)
    text = re.sub(r'^\s*\[\]\([^)]*\)\s*$', '', text, flags=re.M)
    def md_img(m):
        alt, url = m.group(1), m.group(2).strip()
        if url.startswith(("http://","https://","/","data:")): return m.group(0)
        return f"![{alt}]({posixpath.normpath(posixpath.join(reldir, url))})"
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', md_img, text)
    def html_img(m):
        src = m.group(1)
        if src.startswith(("http://","https://","/","data:")): return m.group(0)
        return m.group(0).replace(f'src="{src}"', f'src="{posixpath.normpath(posixpath.join(reldir, src))}"')
    text = re.sub(r'<img\s+[^>]*src="([^"]+)"[^>]*>', html_img, text)
    def md_link(m):
        label, target = m.group(1), m.group(2).strip()
        if "#" in target: target = target.split("#", 1)[0]
        if not target.endswith(".md"): return m.group(0)
        pid = path_to_id.get(posixpath.normpath(posixpath.join(reldir, target)))
        return f"[{label}](#{pid})" if pid else m.group(0)
    text = re.sub(r'(?<!\!)\[([^\]]*)\]\(([^)]+?\.md(?:#[^)]*)?)\)', md_link, text)
    return text

TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="$title$">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0d1117" media="(prefers-color-scheme: dark)">
<title>$title$</title>
<style>
:root{--bg:#fdfdfb;--fg:#1f2328;--muted:#656d76;--link:#0969da;--border:#d8dee4;--code-bg:#eef0ee;--pre-bg:#f6f8fa;--accent:#8250df;--bar:#ffffffe6;--sb:#f7f7f5}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--muted:#9198a1;--link:#4493f8;--border:#30363d;--code-bg:#1c2128;--pre-bg:#161b22;--accent:#bc8cff;--bar:#0d1117e6;--sb:#10141a}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font-family:-apple-system,BlinkMacSystemFont,"SF Pro SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",system-ui,sans-serif;font-size:17px;line-height:1.8;letter-spacing:.01em;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased}
a{color:var(--link);text-decoration:none}a:active{opacity:.6}
.nav-toggle{position:absolute;opacity:0;pointer-events:none}
.topbar{position:sticky;top:0;z-index:30;display:flex;align-items:center;gap:.6rem;padding:.5rem .8rem;padding-top:max(.5rem,env(safe-area-inset-top));background:var(--bar);backdrop-filter:saturate(180%) blur(12px);-webkit-backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid var(--border)}
#tocBtn{font-size:1.3rem;color:var(--fg);padding:.1rem .4rem;cursor:pointer;line-height:1;user-select:none}
#crumb{font-size:.95rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1}
#prog{font-size:.8rem;color:var(--muted);white-space:nowrap}
#content{max-width:44rem;margin:0 auto;padding:1rem 1.1rem 2rem}
/* default = readable scroll (works with NO JavaScript). JS upgrades to paged. */
body.js .page{display:none}
body.js .page.active{display:block;animation:fade .2s ease}
body.js .page:not(.active) .pn-wrap{display:none}
@keyframes fade{from{opacity:.4}to{opacity:1}}
h1,h2,h3,h4{line-height:1.35;font-weight:700;scroll-margin-top:4rem}
h1{font-size:1.6rem;margin:1rem 0 1rem;padding-bottom:.4rem;border-bottom:2px solid var(--border)}
h2{font-size:1.32rem;margin:1.8rem 0 .9rem}h3{font-size:1.12rem;margin:1.5rem 0 .7rem}h4{font-size:1rem;color:var(--muted);margin:1.2rem 0 .6rem}
p{margin:.9rem 0}
code{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;font-size:.88em}
:not(pre)>code{background:var(--code-bg);padding:.15em .4em;border-radius:6px;word-break:break-word}
pre{background:var(--pre-bg);border:1px solid var(--border);border-radius:10px;padding:.9rem 1rem;overflow-x:auto;line-height:1.5;font-size:.84rem;-webkit-overflow-scrolling:touch}
pre code{background:none;padding:0;font-size:inherit}
.diagram{text-align:center;margin:1.3rem 0;overflow-x:auto;-webkit-overflow-scrolling:touch}
.diagram svg{max-width:100%;height:auto}
.diagram-fallback{display:block;text-align:left;white-space:pre;overflow-x:auto;background:var(--pre-bg);border:1px dashed var(--border);border-radius:10px;padding:.9rem 1rem;font-size:.8rem;color:var(--muted)}
math{font-size:1.02em}
math[display="block"]{display:block;overflow-x:auto;overflow-y:hidden;max-width:100%;padding:.4rem 0;-webkit-overflow-scrolling:touch}
#content table{display:block;width:max-content;max-width:100%;overflow-x:auto;border-collapse:collapse;font-size:.9rem;margin:1rem 0;-webkit-overflow-scrolling:touch}
th,td{border:1px solid var(--border);padding:.5rem .7rem;text-align:left}th{background:var(--pre-bg);font-weight:600}
img{max-width:100%;height:auto;display:block;margin:1rem auto;border-radius:8px}
blockquote{margin:1rem 0;padding:.3rem 1rem;border-left:4px solid var(--accent);color:var(--muted);background:var(--pre-bg);border-radius:0 8px 8px 0}
hr{border:none;border-top:1px solid var(--border);margin:2rem 0}
ul,ol{padding-left:1.4rem}li{margin:.3rem 0}
.pn-wrap{display:flex;gap:.6rem;margin:2.5rem 0 1rem;border-top:1px solid var(--border);padding-top:1.2rem}
.pn{flex:1;display:flex;flex-direction:column;gap:.2rem;padding:.7rem .9rem;border:1px solid var(--border);border-radius:12px;background:var(--pre-bg);min-width:0}
.pn-next{text-align:right}.pn-empty{visibility:hidden;border:none;background:none}
.pn-dir{font-size:.75rem;color:var(--muted)}
.pn-t{font-size:.9rem;font-weight:600;color:var(--fg);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#sidebar{position:fixed;top:0;left:0;z-index:50;width:84%;max-width:340px;height:100%;background:var(--sb);border-right:1px solid var(--border);overflow-y:auto;transform:translateX(-102%);transition:transform .26s ease;padding-bottom:3rem;-webkit-overflow-scrolling:touch;box-shadow:2px 0 24px #00000022}
.nav-toggle:checked ~ #sidebar{transform:none}
.toc-head{font-weight:700;font-size:1.1rem;padding:max(1rem,env(safe-area-inset-top)) 1.2rem 1rem;border-bottom:1px solid var(--border);position:sticky;top:0;background:var(--sb)}
#sidebar ul{list-style:none;padding:0;margin:.4rem 0}
.toc-part{font-size:.78rem;font-weight:700;color:var(--muted);padding:1rem 1.2rem .3rem;margin-top:.3rem}
.toc-link a{display:block;padding:.4rem 1.2rem;color:var(--fg);font-size:.92rem;line-height:1.4;border-left:3px solid transparent}
.toc-link.lvl1 a{padding-left:2rem;color:var(--muted);font-size:.88rem}
.toc-link.lvl2 a{padding-left:2.8rem;color:var(--muted);font-size:.85rem}
.toc-link a.active{color:var(--accent);border-left-color:var(--accent);background:var(--pre-bg);font-weight:700}
#backdrop{position:fixed;inset:0;z-index:40;background:#00000055;opacity:0;visibility:hidden;transition:opacity .26s}
.nav-toggle:checked ~ #backdrop{opacity:1;visibility:visible}
@media (min-width:1024px){
 #sidebar{transform:none;box-shadow:none}#tocBtn{display:none}#backdrop{display:none}
 .topbar{padding-left:calc(340px + .8rem)}#content{margin-left:340px}
}
</style>
</head>
<body>
<input type="checkbox" id="navToggle" class="nav-toggle">
<header class="topbar"><label for="navToggle" id="tocBtn" aria-label="目录">&#9776;</label><span id="crumb">$title$</span><span id="prog"></span></header>
<label for="navToggle" id="backdrop"></label>
<aside id="sidebar"><!--SIDEBAR--></aside>
<main id="content">
$body$
</main>
<script>
(function(){
 document.body.classList.add('js');
 var pages=[].slice.call(document.querySelectorAll('.page'));
 if(!pages.length)return;
 var order=pages.map(function(p){return p.id});
 var titleById={}; pages.forEach(function(p){titleById[p.id]=p.getAttribute('data-title')||p.id});
 var sb=document.getElementById('sidebar'),crumb=document.getElementById('crumb'),prog=document.getElementById('prog'),toggle=document.getElementById('navToggle');
 function curId(){var a=document.querySelector('.page.active');return a?a.id:order[0]}
 function setToc(id){var ls=sb.querySelectorAll('a[data-target]');for(var i=0;i<ls.length;i++){var on=ls[i].getAttribute('data-target')===id;ls[i].classList.toggle('active',on);if(on)ls[i].scrollIntoView({block:'nearest'})}}
 function show(id){var i=order.indexOf(id);if(i<0){i=0;id=order[0]}for(var k=0;k<pages.length;k++)pages[k].classList.toggle('active',pages[k].id===id);crumb.textContent=titleById[id];prog.textContent=(i+1)+' / '+order.length;setToc(id);if(toggle)toggle.checked=false;var de=document.documentElement,sbv=de.style.scrollBehavior;de.style.scrollBehavior='auto';window.scrollTo(0,0);de.style.scrollBehavior=sbv;if(location.hash!=='#'+id)history.replaceState(null,'','#'+id)}
 document.addEventListener('click',function(e){var a=e.target.closest('a[href^="#"]');if(a){var id=a.getAttribute('href').slice(1);if(titleById[id]){e.preventDefault();show(id)}}});
 window.addEventListener('keydown',function(e){if(e.target.tagName==='INPUT')return;if(e.key==='ArrowRight'){var i=order.indexOf(curId());if(i<order.length-1)show(order[i+1])}else if(e.key==='ArrowLeft'){var j=order.indexOf(curId());if(j>0)show(order[j-1])}});
 window.addEventListener('hashchange',function(){var id=location.hash.slice(1);if(id&&titleById[id]&&id!==curId())show(id)});
 var h=location.hash.slice(1);show(h&&titleById[h]?h:order[0]);
})();
</script>
</body>
</html>
'''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book-dir", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--svg-dir", required=True, help="dir with pre-rendered d-1.svg .. d-N.svg")
    a = ap.parse_args()
    book_dir = os.path.abspath(a.book_dir)

    items = parse_summary(book_dir)
    page_meta, path_to_id, pidc = [], {}, 0
    for it in items:
        if it[0] == "file":
            _, path, title, lvl = it
            page_meta.append((f"p{pidc}", path, title, lvl))
            path_to_id[posixpath.normpath(path)] = f"p{pidc}"; pidc += 1
    id_to_title = {pi: ti for (pi, _, ti, _) in page_meta}

    mermaid_store, chunks, pi = [], [], 0
    for it in items:
        if it[0] != "file": continue
        _, path, title, lvl = it
        with open(os.path.join(book_dir, path), encoding="utf-8") as f: txt = f.read()
        txt = process_file(txt, posixpath.dirname(path), mermaid_store, path_to_id)
        chunks.append(f'\n\nPGBKZZp{pi}ZZ\n\n{txt}\n\n'); pi += 1
    combined = "\n".join(chunks)
    print(f"  pages: {len(page_meta)}, mermaid blocks: {len(mermaid_store)}")

    # load pre-rendered SVGs, namespace ids to avoid collisions; fall back to source on miss
    svgs, missing = [], 0
    for i in range(len(mermaid_store)):
        p = os.path.join(a.svg_dir, f"d-{i+1}.svg")
        if os.path.isfile(p) and os.path.getsize(p) > 0:
            s = open(p, encoding="utf-8").read()
            j = s.find("<svg"); s = s[j:] if j > 0 else s
            s = s.replace("my-svg", f"mmd{i}")
            svgs.append(s)
        else:
            missing += 1
            svgs.append('<pre class="diagram-fallback">' + esc(mermaid_store[i]) + '</pre>')
    if missing: print(f"  WARNING: {missing}/{len(mermaid_store)} diagrams failed to render -> showing source as fallback")

    # sidebar TOC
    sb = ['<div class="toc-head">目录</div><ul>']; fi = 0
    for it in items:
        if it[0] == "part": sb.append(f'<li class="toc-part">{esc(it[1])}</li>')
        else:
            pidi, _, title, lvl = page_meta[fi]; fi += 1
            sb.append(f'<li class="toc-link lvl{lvl}"><a data-target="{pidi}" href="#{pidi}">{esc(title)}</a></li>')
    sb.append('</ul>'); sidebar_html = "".join(sb)

    tmp_md = os.path.join(book_dir, "_combined_tmp.md")
    tpl = "/tmp/_book_template.html"; out_tmp = "/tmp/_book_out.html"
    with open(tmp_md, "w", encoding="utf-8") as f: f.write(combined)
    with open(tpl, "w", encoding="utf-8") as f: f.write(TEMPLATE)
    cmd = ["pandoc", "_combined_tmp.md", "-f", "markdown", "-t", "html5",
           "--standalone", "--embed-resources", "--mathml",
           "--template", tpl, "--metadata", f"title={a.title}", "-o", out_tmp]
    print("  running pandoc ...")
    r = subprocess.run(cmd, cwd=book_dir, capture_output=True, text=True)
    if os.path.exists(tmp_md): os.remove(tmp_md)
    if r.returncode != 0:
        print("PANDOC FAILED:\n", r.stderr[:4000]); sys.exit(1)

    with open(out_tmp, encoding="utf-8") as f: html = f.read()
    # swap mermaid placeholders -> pre-rendered inline SVG (2nd pass catches any not in <p>)
    def mrepl(m): return f'<figure class="diagram">{svgs[int(m.group(1))]}</figure>'
    html = re.sub(r'<p>\s*MERMAIDZZ(\d+)ZZ\s*</p>', mrepl, html)
    html = re.sub(r'MERMAIDZZ(\d+)ZZ', mrepl, html)
    # split <main> into pages, append static prev/next nav per page
    mm = re.search(r'(<main id="content">)(.*?)(</main>)', html, flags=re.DOTALL)
    segs = re.split(r'<p>\s*PGBKZZ(p\d+)ZZ\s*</p>', mm.group(2))
    def navhtml(i):
        out = ['<nav class="pn-wrap">']
        if i > 0:
            pid, _, pt, _ = page_meta[i-1]
            out.append(f'<a class="pn pn-prev" href="#{pid}"><span class="pn-dir">&#8592; 上一页</span><span class="pn-t">{esc(pt)}</span></a>')
        else: out.append('<span class="pn pn-empty"></span>')
        if i < len(page_meta)-1:
            nid, _, nt, _ = page_meta[i+1]
            out.append(f'<a class="pn pn-next" href="#{nid}"><span class="pn-dir">下一页 &#8594;</span><span class="pn-t">{esc(nt)}</span></a>')
        out.append('</nav>'); return "".join(out)
    pages_html = []
    for k in range(1, len(segs), 2):
        pid, seg = segs[k], segs[k+1]
        idx = order_idx = [pm[0] for pm in page_meta].index(pid)
        pages_html.append(f'<section class="page" id="{pid}" data-title="{escattr(id_to_title[pid])}">{seg}{navhtml(idx)}</section>')
    new_main = mm.group(1) + '<div id="pages">' + "".join(pages_html) + '</div>' + mm.group(3)
    html = html[:mm.start()] + new_main + html[mm.end():]
    html = html.replace("<!--SIDEBAR-->", sidebar_html)

    leftover = len(re.findall(r'MERMAIDZZ\d+ZZ|PGBKZZ', html))
    with open(a.out, "w", encoding="utf-8") as f: f.write(html)
    size = os.path.getsize(a.out) / 1048576
    n_svg = html.count('class="diagram"'); n_math = html.count('<math'); n_img = html.count('data:image')
    print(f"  pages: {len(pages_html)} | inline svg: {n_svg} | <math>: {n_math} | images: {n_img} | leftover: {leftover}")
    print(f"  OUTPUT: {a.out}  ({size:.2f} MB)")

if __name__ == "__main__":
    main()
