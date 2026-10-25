#!/usr/bin/env python3
"""Find the best loop point in a clip: the pair of frames that look most alike.

Prints the in/out seconds to feed make_ambient_demo.sh. Comparing normalised
grayscale frames means brightness drift over the shot doesn't skew the match.
"""
import argparse
import subprocess
import sys

import numpy as np


def frames(path, fps=2, w=160, h=90):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path,
         "-vf", f"fps={fps},scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
        capture_output=True, check=True).stdout
    n = len(raw) // (w * h)
    f = np.frombuffer(raw, dtype=np.uint8)[: n * w * h].reshape(n, h, w).astype(np.float32)
    f = (f - f.mean(axis=(1, 2), keepdims=True)) / (f.std(axis=(1, 2), keepdims=True) + 1e-6)
    return f.reshape(n, -1), n, fps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--min-len", type=float, default=55)
    ap.add_argument("--max-len", type=float, default=75)
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()

    f, n, fps = frames(a.video)
    lo, hi = int(a.min_len * fps), int(a.max_len * fps)
    rows = []
    for i in range(0, n - hi - 1, 2):
        for d in range(lo, hi + 1, 2):
            j = i + d
            if j >= n:
                continue
            rows.append((float(np.mean((f[i] - f[j]) ** 2)), i, j))
    if not rows:
        sys.exit("clip too short for those bounds")
    rows.sort()
    print(f"{n} frames @ {fps}fps")
    for mse, i, j in rows[: a.top]:
        print(f"  mse={mse:7.4f}  in={i / fps:6.1f}s  out={j / fps:6.1f}s  len={(j - i) / fps:4.1f}s")


if __name__ == "__main__":
    main()
