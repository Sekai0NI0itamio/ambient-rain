"""Local orchestrator: heavy render + YouTube upload happen on GitHub.

Your laptop only: (optionally) renders a 60s preview from local assets,
pushes nothing big, triggers the cloud workflow, watches it, prints the link.

Prereqs: `gh` logged in (`gh auth status`), repo pushed (see README.md).
Usage:
  python3 make_long.py --hours 8 --title "Rain on Glass | 8 Hours Cozy Sleep Sounds"
  python3 make_long.py --hours 1 --privacy unlisted --preview
"""
import argparse
import re
import subprocess
import sys
import time


def run(cmd, capture=False):
    print("+", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=capture, text=True)
    if r.returncode != 0:
        if capture:
            print(r.stdout[-3000:])
            print(r.stderr[-3000:], file=sys.stderr)
        sys.exit(r.returncode)
    return r.stdout if capture else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", choices=["1", "8"], default="1")
    ap.add_argument("--title", default="Rain on Glass Window | Cozy Ambient Sleep Sounds")
    ap.add_argument("--description", default="Soft rain falling on a glass window. Loopable ambient rain for sleep, study and relaxation.")
    ap.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    ap.add_argument("--footage", choices=["window", "woods", "leaves"], default="woods")
    ap.add_argument("--seed", default="7")
    ap.add_argument("--from-id", default="",
                    help="Gallery ID like woods-7 (sets footage + seed, overrides --footage/--seed)")
    ap.add_argument("--preview", action="store_true",
                    help="Render a 60s local preview first (uses sources/ in this folder)")
    a = ap.parse_args()

    if a.from_id:
        try:
            a.footage, a.seed = a.from_id.rsplit("-", 1)
        except ValueError:
            sys.exit("--from-id must look like woods-7")
        if a.footage not in ("window", "woods", "leaves"):
            sys.exit(f"unknown footage in --from-id: {a.footage}")

    if a.preview:
        run([sys.executable, "rain_sample_mix.py", "--duration", "60",
             "--out", "preview_audio.wav", "--seed", a.seed])
        run([sys.executable, "video_loop.py", "--src", "sources/rain_window_home.mp4",
             "--audio", "preview_audio.wav", "--out", "preview.mp4",
             "--loop-sec", "55", "--total", "60"])
        print("preview ready: preview.mp4 (check it before paying for cloud minutes)")

    out = run(["gh", "workflow", "run", "render-upload.yml",
               "-f", f"hours={a.hours}", "-f", f"title={a.title}",
               "-f", f"description={a.description}", "-f", f"privacy={a.privacy}",
               "-f", f"footage={a.footage}", "-f", f"seed={a.seed}"], capture=True)
    time.sleep(8)
    runs = run(["gh", "run", "list", "--workflow", "render-upload.yml",
                "--limit", "1", "--json", "databaseId", "-q", ".[0].databaseId"],
               capture=True).strip()
    print(f"run id: {runs} — watching (Ctrl+C to stop watching, the cloud keeps going)...")
    run(["gh", "run", "watch", runs])
    log = run(["gh", "run", "view", runs, "--log"], capture=True)
    m = re.search(r"https://www\.youtube\.com/watch\?v=[\w-]+", log)
    if m:
        print(f"\nYouTube: {m.group(0)}")
    else:
        print("\nNo video link in logs — open the run summary, or the upload step failed.")


if __name__ == "__main__":
    main()
