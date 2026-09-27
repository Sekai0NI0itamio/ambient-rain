"""Burn a PNG-sequence overlay template onto a video's opening seconds.

Usage:
  python3 scripts/apply_overlay.py --video in.mp4 --frames overlay_frames --out out.mp4
Video is re-encoded (veryfast); audio copied untouched.
"""
import argparse
import json
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--frames", required=True,
                    help="Dir with f04d.png sequence + manifest.json from make_overlay.py")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    with open(f"{a.frames}/manifest.json") as fh:
        m = json.load(fh)
    subprocess.run([
        "ffmpeg", "-y", "-i", a.video,
        "-framerate", str(m["fps"]), "-i", f"{a.frames}/f%04d.png",
        "-filter_complex",
        "[1:v][0:v]scale2ref[ov][base];[base][ov]overlay=0:0:eof_action=pass[v]",
        "-map", "[v]", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-c:a", "copy", "-movflags", "+faststart", "-shortest", a.out,
    ], check=True)
    print(f"[overlay] wrote {a.out}")


if __name__ == "__main__":
    main()
