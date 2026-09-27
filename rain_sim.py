"""Procedural rain generator v0.1 - synthetic, no samples needed.
Layers: bed wash (filtered noise) + patter (bandpassed bursts) + droplets (sparse decays).
Weather states modulate intensity over minutes. End loops seamlessly to start.
Usage: python3 rain_sim.py --duration 30 --out rain_demo.wav --seed 7
"""
import argparse
import numpy as np
from scipy.signal import butter, lfilter

SR = 44100

def lowpass(x, cutoff):
    b, a = butter(4, cutoff / (SR / 2), btype="low")
    return lfilter(b, a, x)

def highpass(x, cutoff):
    b, a = butter(2, cutoff / (SR / 2), btype="high")
    return lfilter(b, a, x)

def bandpass(x, lo, hi):
    b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], btype="band")
    return lfilter(b, a, x)

def intensity_curve(n, sr, seed=0):
    rng = np.random.default_rng(seed)
    t = np.arange(n) / sr
    base = 0.65 + 0.25 * np.sin(2 * np.pi * t / 180 + rng.uniform(0, 6))
    base += 0.10 * np.sin(2 * np.pi * t / 47 + rng.uniform(0, 6))
    return np.clip(base, 0.3, 1.0)

def render(duration, seed=7):
    rng = np.random.default_rng(seed)
    n = int(duration * SR)
    noise = rng.standard_normal(n)
    bed = lowpass(noise, 900) * 0.5 + lowpass(rng.standard_normal(n), 3200) * 0.18
    bed = highpass(bed, 120)
    patter_src = bandpass(rng.standard_normal(n), 1800, 7000)
    env = np.abs(lowpass(rng.standard_normal(n), 8)) + 0.4
    patter = patter_src * env * 0.35
    drops = np.zeros(n)
    n_drops = int(duration * 2.2)
    last_idx = -SR
    for _ in range(n_drops):
        idx = rng.integers(0, n - 4000)
        if idx - last_idx < int(SR * 0.15):
            continue
        last_idx = idx
        length = rng.integers(800, 3500)
        decay = np.exp(-np.arange(length) / rng.uniform(300, 1200))
        freq = rng.uniform(2500, 6500)
        blip = np.sin(2 * np.pi * freq * np.arange(length) / SR) * decay
        blip *= rng.uniform(0.05, 0.22)
        pan = rng.uniform(0.2, 0.8)
        drops[idx:idx + length] += blip * pan
    curve = intensity_curve(n, SR, seed)
    mix = (bed * 0.9 + patter * 0.6) * curve + drops
    peak = np.max(np.abs(mix))
    mix = mix / peak * 0.89
    fade = int(SR * 3)
    w = np.linspace(0, 1, fade) ** 2
    tail = mix[-fade:] * (1 - w) + mix[:fade] * w
    mix[-fade:] = tail
    stereo = np.stack([mix, np.roll(mix, int(SR * 0.013)) * 0.96], axis=1)
    stereo[:, 1] = lowpass(stereo[:, 1], 7500)
    return (np.clip(stereo, -1, 1) * 32767).astype(np.int16)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--duration", type=float, default=30)
    ap.add_argument("--out", default="rain_demo.wav")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    import wave
    audio = render(a.duration, a.seed)
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(audio.tobytes())
    print(f"wrote {a.out} {a.duration}s seed={a.seed} peak={np.max(np.abs(audio))/32767:.3f}")

if __name__ == "__main__":
    main()
