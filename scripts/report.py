#!/usr/bin/env python3
"""Renders the catalog's reviews (catalog.json + reviews/*.md) into one HTML page.

    python3 scripts/report.py [out.html] [--open]

Writes review-report.html in the repository root by default (git ignores it);
--open opens it in the browser. Addons needing a look or flagged come first.
"""
import html
import json
import subprocess
import sys
from pathlib import Path

args = [a for a in sys.argv[1:] if a != "--open"]
repo = Path(__file__).resolve().parent.parent
out = Path(args[0]) if args else repo / "review-report.html"
catalog = json.loads((repo / "catalog.json").read_text())

rows, sections, pending = [], [], []
for e in catalog["addons"]:
    reviews = e.get("reviews", [])
    if not reviews:
        pending.append(e["name"])
        continue
    r = reviews[0]
    c, x = r["claude"], r["codex"]
    signed = r.get("signoff")
    state = "pass" if c == x == "pass" or signed else ("fail" if "fail" in (c, x) else "check")
    label = {"pass": "Reviewed", "fail": "Flagged", "check": "Needs a look"}[state]
    if signed and not c == x == "pass":
        label = "Signed off"
    anchor = e["id"]
    rows.append(
        f'<tr class="{state}"><td><a href="#{anchor}">{html.escape(e["name"])}</a></td>'
        f'<td>{html.escape(r["tag"])}</td><td><span class="v {c}">{c}</span></td>'
        f'<td><span class="v {x}">{x}</span></td><td><span class="pill {state}">{label}</span></td></tr>'
    )
    report = (repo / r["report"]).read_text() if (repo / r["report"]).exists() else "(report missing)"
    sections.append(
        f'<details id="{anchor}" class="{state}" {"open" if state != "pass" else ""}>'
        f'<summary><span class="pill {state}">{label}</span> {html.escape(e["name"])} '
        f'<span class="muted">{html.escape(r["tag"])} · {html.escape(e["repo"])}</span></summary>'
        f'<div class="md" data-md="{html.escape(json.dumps(report))}"></div></details>'
    )

order = {"fail": 0, "check": 1, "pass": 2}
rows.sort(key=lambda s: order[s.split('"')[1]])
sections.sort(key=lambda s: order[s.split('class="')[1].split('"')[0]])
counts = {k: sum(1 for s in rows if f'class="{k}"' in s) for k in order}

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Packmule Reviews</title>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<style>
:root {{ --bg:#15171c; --panel:#1d2027; --border:#323744; --text:#e6e2d6; --muted:#8d93a3;
  --accent:#d4a73c; --ok:#5fb96a; --warn:#e0a43a; --err:#e0605a; }}
@media (prefers-color-scheme: light) {{ :root:not([data-theme="dark"]) {{ --bg:#f6f4ee; --panel:#fff; --border:#dcd8cc;
  --text:#22242a; --muted:#666b78; --accent:#9a7414; --ok:#2e7d3a; --warn:#9a6a10; --err:#b3362f; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:15px/1.55 system-ui, sans-serif; }}
main {{ max-width:960px; margin:0 auto; padding:32px 16px 64px; }}
h1 {{ margin:0 0 4px; font-size:26px; }} h1 span {{ color:var(--accent); }}
.muted {{ color:var(--muted); font-size:13px; font-weight:normal; }}
.stats {{ display:flex; gap:12px; margin:20px 0; flex-wrap:wrap; }}
.stat {{ background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:12px 16px; min-width:130px; }}
.stat b {{ display:block; font-size:24px; }}
.table-wrap {{ overflow-x:auto; }}
table {{ width:100%; border-collapse:collapse; background:var(--panel); border:1px solid var(--border); border-radius:10px; overflow:hidden; }}
th, td {{ text-align:left; padding:8px 12px; border-bottom:1px solid var(--border); white-space:nowrap; }}
th {{ color:var(--muted); font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:.04em; }}
a {{ color:var(--accent); }}
.pill {{ display:inline-block; padding:1px 9px; border-radius:10px; font-size:12px; font-weight:600; }}
.pill.pass {{ color:var(--ok); background:color-mix(in srgb, var(--ok) 16%, transparent); }}
.pill.check {{ color:var(--warn); background:color-mix(in srgb, var(--warn) 16%, transparent); }}
.pill.fail {{ color:var(--err); background:color-mix(in srgb, var(--err) 16%, transparent); }}
.v.pass {{ color:var(--ok); }} .v.unsure {{ color:var(--warn); }} .v.fail, .v.error {{ color:var(--err); }}
details {{ background:var(--panel); border:1px solid var(--border); border-radius:10px; margin:12px 0; }}
details.check {{ border-left:4px solid var(--warn); }} details.fail {{ border-left:4px solid var(--err); }}
summary {{ cursor:pointer; padding:12px 16px; font-weight:600; }}
.md {{ padding:0 20px 16px; overflow-wrap:anywhere; }}
.md h1 {{ font-size:20px; }} .md h2 {{ font-size:18px; border-top:1px solid var(--border); padding-top:14px; }}
.md code {{ font-size:13px; background:color-mix(in srgb, var(--muted) 15%, transparent); padding:1px 4px; border-radius:4px; }}
.md pre {{ background:var(--bg); padding:10px; border-radius:6px; overflow-x:auto; }}
.md pre code {{ background:none; }}
.pending {{ color:var(--muted); }}
</style></head><body><main>
<h1><span>Packmule</span> catalog reviews</h1>
<div class="muted">Claude and Codex read each release looking for malicious code. Both must pass for "Reviewed".</div>
<div class="stats">
<div class="stat"><b style="color:var(--ok)">{counts['pass']}</b>Reviewed</div>
<div class="stat"><b style="color:var(--warn)">{counts['check']}</b>Needs a look</div>
<div class="stat"><b style="color:var(--err)">{counts['fail']}</b>Flagged</div>
<div class="stat"><b>{len(pending)}</b>Not reviewed yet</div>
</div>
<div class="table-wrap"><table><tr><th>Addon</th><th>Release</th><th>Claude</th><th>Codex</th><th>Result</th></tr>
{''.join(rows)}</table></div>
{f'<p class="pending">Not reviewed yet: {html.escape(", ".join(pending))}</p>' if pending else ''}
<h2>Reports</h2>
{''.join(sections)}
</main>
<script>
// Reports quote untrusted addon code: show raw HTML as text, keep only web links.
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
if (window.marked) marked.use({{ renderer: {{
  html(text) {{ return esc(typeof text === 'object' ? text.text : text); }},
  link(href, title, text) {{
    if (typeof href === 'object') {{ ({{ href, text }} = href); }}
    return /^https?:\\/\\//i.test(href || '') ? `<a href="${{esc(href)}}" rel="noreferrer">${{text}}</a>` : text;
  }},
  image(href, title, text) {{ return esc(typeof href === 'object' ? href.text : text); }},
}} }});
for (const el of document.querySelectorAll('.md')) {{
  const text = JSON.parse(el.dataset.md);
  if (window.marked) {{ el.innerHTML = marked.parse(text); }}
  else {{ const pre = document.createElement('pre'); pre.textContent = text; el.appendChild(pre); }}
}}
</script></body></html>
"""
out.write_text(page)
print(out)
if "--open" in sys.argv:
    subprocess.Popen(["xdg-open", str(out)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
