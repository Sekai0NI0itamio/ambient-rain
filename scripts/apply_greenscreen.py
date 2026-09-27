"""Chroma-key a green-screen clip (e.g. from Canva) over a video.

Usage:
  python3 scripts/apply_greenscreen.py --video in.mp4 --green canva_anim.mp4 --out out.mp4
Keys out pure green, despills edges, overlays from --start for --dur seconds.
Video re-encoded (veryfast); audio copied.
Canva spec for clean keys: solid #00FF00 background (no gradients/shadows),
nothing green in the subject, export 1920x1080 MP4 highest quality.
"""
import argparse
import subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--green", required=True,
                    help="Green-screen clip (solid #00FF00 bg)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--dur", type=float, default=6.0)
    ap.add_argument("--color", default="0x00FF00")
    ap.add_argument("--similarity", type=float, default=0.3)
    ap.add_argument("--blend", type=float, default=0.1)
    a = ap.parse_args()
    subprocess.run([
        "ffmpeg", "-y", "-i", a.video, "-i", a.green,
        "-filter_complex",
        f"[1:v]scale2ref=w=iw:h=ih[fg][base];"
        f"[fg]chromakey=color={a.color}:similarity={a.similarity}:blend={a.blend}[key];"
        f"[base][key]overlay=0:0:enable='between(t,{a.start},{a.start + a.dur})'[v]",
        "-map", "[v]", "-map", "0:a?",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-c:a", "copy", "-movflags", "+faststart", "-shortest", a.out,
    ], check=True)
    print(f"[green] wrote {a.out}")


if __name__ == "__main__":
    main()
