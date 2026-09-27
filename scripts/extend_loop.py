"""Loop a seamless master file to an exact target length via stream copy.

The master must already loop seamlessly by itself (our mixer crossfades the
end into the start), so plain concatenation is clickless and instant.
Usage: python3 scripts/extend_loop.py --src master.mp4 --out long.mp4 --seconds 28800
"""
import argparse
import math
import subprocess


def probe_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seconds", type=float, required=True)
    a = ap.parse_args()
    master = probe_duration(a.src)
    loops = max(1, math.ceil(a.seconds / master))
    print(f"[extend] master={master:.1f}s target={a.seconds:.0f}s loops={loops}")
    subprocess.run([
        "ffmpeg", "-y",
        "-stream_loop", str(loops), "-i", a.src,
        "-t", str(a.seconds),
        "-c", "copy", "-movflags", "+faststart", a.out,
    ], check=True)
    print(f"[extend] wrote {a.out} ({probe_duration(a.out):.1f}s)")


if __name__ == "__main__":
    main()
