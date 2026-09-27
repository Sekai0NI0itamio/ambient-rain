"""Sample-based rain mixer v0.2 - uses REAL downloaded rain recordings.
Layers: bed loop (bg) + texture loop (garden, offset) + window patter + heavy-drop grains.
Usage: python3 rain_sample_mix.py --duration 60 --out rain_real.wav --seed 7
Requires: ffmpeg on PATH, numpy, sources/*.ogg present.
"""
import argparse, subprocess, os, wave
import numpy as np

SR = 44100
SRC = os.path.join(os.path.dirname(__file__), "sources")

def decode(name):
    path = os.path.join(SRC, name)
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-acodec", "pcm_f32le", "-"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"decode failed for {name}: {p.stderr.decode()[:300]}")
    return np.frombuffer(p.stdout, dtype=np.float32).reshape(-1, 2).copy()

def loop_fill(audio, n, xfade_sec=2.0):
    if len(audio) >= n:
        start = 0
        return audio[start:start + n].copy()
    x = int(SR * xfade_sec)
    out = audio.copy()
    while len(out) < n + x:
        tail = out[-x:]
        head = audio[:x]
        w = np.linspace(0, 1, x)[:, None] ** 2
        blend = tail * (1 - w) + head * w
        out = np.concatenate([out[:-x], blend, audio[x:]])
    return out[:n].copy()

def grains(src, n, count, seed, gain_lo=0.05, gain_hi=0.2, min_gap_s=0.4):
    rng = np.random.default_rng(seed)
    out = np.zeros((n, 2), dtype=np.float64)
    last = -10 * SR
    placed = 0
    tries = 0
    while placed < count and tries < count * 20:
        tries += 1
        idx = rng.integers(0, n - SR)
        if idx - last < int(SR * min_gap_s):
            continue
        glen = rng.integers(int(SR * 0.25), int(SR * 0.7))
        s0 = rng.integers(0, max(1, len(src) - glen))
        g = src[s0:s0 + glen].astype(np.float64)
        fade = int(0.02 * SR)
        w = np.ones(len(g))
        w[:fade] = np.linspace(0, 1, fade)
        w[-fade:] = np.linspace(1, 0, fade)
        g *= w[:, None] * rng.uniform(gain_lo, gain_hi)
        if rng.random() < 0.5:
            g = g[:, ::-1]
        pan = rng.uniform(0.25, 0.75)
        g[:, 0] *= (1 - pan) * 1.4
        g[:, 1] *= pan * 1.4
        out[idx:idx + len(g)] += g
        last = idx
        placed += 1
    return out

def weather(n, seed):
    rng = np.random.default_rng(seed + 99)
    t = np.arange(n) / SR
    c = 0.72 + 0.20 * np.sin(2 * np.pi * t / 150 + rng.uniform(0, 6))
    c += 0.08 * np.sin(2 * np.pi * t / 41 + rng.uniform(0, 6))
    return np.clip(c, 0.4, 1.0)[:, None]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, default=60)
    ap.add_argument("--out", default="rain_real.wav")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    n = int(a.duration * SR)
    print(f"[mix] decoding sources...")
    bg = decode("rain_bg.ogg")
    garden = decode("rain_garden.ogg")
    window = decode("rain_window.ogg")
    heavy = decode("rain_heavy.ogg")
    print(f"[mix] lens: bg={len(bg)/SR:.1f}s garden={len(garden)/SR:.1f}s window={len(window)/SR:.1f}s heavy={len(heavy)/SR:.1f}s")
    bed = loop_fill(bg, n) * 0.85
    tex = np.roll(loop_fill(garden, n, 3.0), SR * 17) * 0.35
    pat = np.roll(loop_fill(window, n, 2.5), SR * 41) * 0.30
    acc = grains(heavy, n, count=int(a.duration * 1.2), seed=a.seed)
    acc += grains(window, n, count=int(a.duration * 0.8), seed=a.seed + 1, gain_lo=0.03, gain_hi=0.12)
    mix = (bed + tex + pat) * weather(n, a.seed) + acc
    peak = np.max(np.abs(mix))
    mix = mix / peak * 0.89
    f = int(SR * 3)
    w = (np.linspace(0, 1, f) ** 2)[:, None]
    mix[-f:] = mix[-f:] * (1 - w) + mix[:f] * w
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    with wave.open(a.out, "wb") as fh:
        fh.setnchannels(2)
        fh.setsampwidth(2)
        fh.setframerate(SR)
        fh.writeframes(pcm.tobytes())
    print(f"[mix] wrote {a.out} {a.duration}s peak={np.max(np.abs(pcm))/32767:.3f}")

if __name__ == "__main__":
    main()
