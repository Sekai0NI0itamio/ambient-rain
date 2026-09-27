"""Build the static preview-gallery site.

Reads manifest.json (list of {file, id, footage, seed, title}) next to the
preview mp4s and writes index.html: one card per preview with a watchable
<video>, its ID, and a click-to-copy 8h upload command.
Usage: python3 scripts/build_gallery.py --dir site --channel "Ambientful Ambient Sounds"
"""
import argparse
import json
import os

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{channel} — preview gallery</title>
<style>
  body {{ background: #0a0e1e; color: #ebe6d7; font-family: system-ui, sans-serif;
         max-width: 900px; margin: 0 auto; padding: 24px; }}
  h1 {{ font-size: 1.4em; }} p.sub {{ color: #7db4dc; }}
  .card {{ background: #12182e; border-radius: 12px; padding: 16px; margin: 20px 0; }}
  video {{ width: 100%; border-radius: 8px; background: #000; }}
  .meta {{ color: #7db4dc; font-size: .9em; margin: 8px 0; }}
  code.cmd {{ display: block; background: #000; padding: 10px; border-radius: 8px;
              font-size: .8em; white-space: pre-wrap; margin: 8px 0; }}
  button {{ background: #7db4dc; color: #0a0e1e; border: 0; border-radius: 8px;
            padding: 10px 16px; font-weight: 700; cursor: pointer; }}
  button.done {{ background: #6fbf73; }}
</style>
</head>
<body>
<h1>{channel} — preview gallery</h1>
<p class="sub">Watch each 60s preview, pick a winner, copy its 8-hour command,
run it on your laptop. The cloud renders + uploads to YouTube.</p>
{cards}
<script>
function copyCmd(id) {{
  const el = document.getElementById('cmd-' + id);
  navigator.clipboard.writeText(el.innerText).then(() => {{
    const b = document.getElementById('btn-' + id);
    b.innerText = 'Copied!'; b.classList.add('done');
    setTimeout(() => {{ b.innerText = 'Copy 8h command'; b.classList.remove('done'); }}, 2000);
  }});
}}
</script>
</body>
</html>
"""

CARD = """<div class="card">
<h2>{title}</h2>
<video controls preload="metadata" src="{file}"></video>
<div class="meta">id: <b>{id}</b> &nbsp;•&nbsp; footage: {footage} &nbsp;•&nbsp; seed: {seed}</div>
<code class="cmd" id="cmd-{id}">{cmd}</code>
<button id="btn-{id}" onclick="copyCmd('{id}')">Copy 8h command</button>
</div>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="site")
    ap.add_argument("--channel", default="Ambientful Ambient Sounds")
    a = ap.parse_args()
    with open(os.path.join(a.dir, "manifest.json")) as fh:
        items = json.load(fh)
    cards = []
    for it in items:
        cmd = (f"python3 make_long.py --from-id {it['id']} "
               f"--hours 8 --privacy private")
        cards.append(CARD.format(cmd=cmd, **it))
    html = PAGE.format(channel=a.channel, cards="\n".join(cards))
    out = os.path.join(a.dir, "index.html")
    with open(out, "w") as fh:
        fh.write(html)
    print(f"[gallery] wrote {out} with {len(items)} cards")


if __name__ == "__main__":
    main()
