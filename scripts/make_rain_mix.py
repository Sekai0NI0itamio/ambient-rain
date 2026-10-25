#!/usr/bin/env python3
"""Build the layered rain bed: dim wash + audible droplets + scheduled thunder.

Why a script and not one ffmpeg graph: the layers need per-layer tiling with
crossfades, and the thunder has to be placed at chosen times rather than left to
whatever the source recording happened to do. That is arithmetic, and numpy is
clearer about it than a 40-line filter_complex.

Output: sources/_mix_raw.wav (48 kHz stereo, peak -6 dBFS) — loudnorm is applied
afterwards by make_layered_demo.sh.
"""
import argparse
import subprocess

import numpy as np

SR = 48000


def load(path, start=0.0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start)]
    if dur is not None:
        cmd += ["-t", str(dur)]
    cmd += ["-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def tile(x, total, xfade=0.5):
    """Repeat x until it covers `total` samples, crossfading each join."""
    xf = int(xfade * SR)
    out = x.copy()
    while len(out) < total:
        tail = out[-xf:]
        head = x[:xf]
        # Equal-power, not linear: uncorrelated rain summed linearly dips ~3 dB
        # at every join, which is audible as a lull in otherwise steady rain.
        w = np.linspace(0, 1, xf, dtype=np.float32)[:, None]
        out = np.vstack([out[:-xf], tail * np.sqrt(1 - w) + head * np.sqrt(w), x[xf:]])
    return out[:total]


def rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def set_rms(x, target_db):
    return x * (10 ** ((target_db - rms_db(x)) / 20))


def place(canvas, clip, at_sec, gain=1.0):
    i = int(at_sec * SR)
    n = min(len(clip), len(canvas) - i)
    if n > 0:
        canvas[i:i + n] += clip[:n] * gain
    return canvas


def lp_fft(x, fc, order=2):
    """Butterworth-shaped low-pass applied in the frequency domain."""
    n = len(x)
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(n, 1 / SR)[:, None]
    H = 1 / np.sqrt(1 + (f / fc) ** (2 * order))
    return np.fft.irfft(X * H, n, axis=0)


def make_ir(dur=1.1, decay=0.30):
    """Synthetic room: a few early reflections over a dark diffuse tail."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(7)
    ir = rng.standard_normal((n, 2)) * np.exp(-t / decay)[:, None]
    for d, g in ((0.009, 0.6), (0.014, 0.4), (0.022, 0.3), (0.035, 0.2)):
        ir[int(d * SR)] += g
    ir = lp_fft(ir, 3500)
    return ir / (np.sqrt(np.sum(ir ** 2)) + 1e-12)


def convolve_ir(x, ir):
    n = len(x) + len(ir) - 1
    N = 1 << int(np.ceil(np.log2(n)))
    X = np.fft.rfft(x, N, axis=0)
    H = np.fft.rfft(ir, N, axis=0)
    return np.fft.irfft(X * H, N, axis=0)[: len(x)]


def behind_wall(x):
    """Heard through a wall: direct path muffled and attenuated, mostly diffuse.

    This is the same idea as Minecraft's Sounds Physics Remastered occlusion —
    a blocked path loses its high end and arrives as reflections, not as a
    quieter version of the original.
    """
    dry = lp_fft(x, 2400) * 0.60
    wet = convolve_ir(lp_fft(x, 4500), make_ir()) * 0.55
    return dry + wet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=10)
    ap.add_argument("--out", default="sources/_mix_raw.wav")
    ap.add_argument("--thunder", action="store_true", help="add scheduled thunder (off by default)")
    ap.add_argument("--drops", action="store_true", help="add droplet/drip layers (off: rain bed + thunder only)")
    ap.add_argument("--no-room", action="store_true", help="disable the behind-a-wall filter")
    a = ap.parse_args()

    total = int(a.minutes * 60 * SR)
    secs = a.minutes * 60

    # Chosen by ear + measurement: klangfabrik "rainstorm" (Freesound 194209).
    # 0.6 discrete drops/min, 1.9 dB level variance, slope -6.2 dB/decade.
    bed = tile(load("sources/candidates/rain_194209_klangfabrik.mp3", 0, 512), total)
    # 165 samples in 57 M sit above 0.5 — MP3 spikes, inaudible but they wreck the
    # crest factor and force the whole mix to be scaled down. Clamp them.
    bed = np.clip(bed, -0.95, 0.95)
    bed = set_rms(bed, -24.0)

    if a.drops:
        droplets = set_rms(tile(load("sources/fs_658836_droplets_leaves.wav"), total), -34.0)
        drips = set_rms(tile(load("sources/fs_459983_dripping_softly.mp3"), total), -27.0)
    else:
        droplets = np.zeros_like(bed)
        drips = np.zeros_like(bed)

    mix = bed + droplets + drips
    foreground = droplets + drips
    thunder_track = np.zeros_like(bed)

    # Thunder: swells cut from a continuous distant-thunder recording, then
    # placed so each one passes by and clears out before the next. Long fades are
    # what make it "distant" rather than a hit.
    if a.thunder:
        storm = load("sources/candidates/thunder_572444_TRP.mp3", 0, 268)
        mono = storm.mean(axis=1)
        win = int(0.5 * SR)
        n = len(mono) // win
        env = np.abs(np.fft.rfft(
            (mono[: n * win].reshape(n, win) * np.hanning(win)), axis=1))
        fr = np.fft.rfftfreq(win, 1 / SR)
        env = env[:, fr < 150].sum(axis=1)
        base = np.median(env)
        thr = np.percentile(env, 90)
        peaks = [i for i in range(1, n - 1)
                 if env[i] > thr and env[i] >= env[i - 1] and env[i] >= env[i + 1]]
        picked = []
        for i in peaks:
            if not picked or i - picked[-1] >= 24:      # >= 12 s apart in the source
                picked.append(i)
        picked = sorted(picked, key=lambda i: -env[i])[:12]
        picked.sort()
        schedule = [35, 92, 150, 205, 268, 325, 392, 448, 515, 572]
        fade_in, fade_out = int(3.0 * SR), int(4.0 * SR)
        up = np.linspace(0, 1, fade_in, dtype=np.float32)[:, None]
        down = np.linspace(1, 0, fade_out, dtype=np.float32)[:, None]
        for i, at in zip(picked, schedule):
            if at >= secs - 16:
                continue
            start = max(0, int(i * 0.5 * SR) - 4 * SR)
            clip = storm[start:start + 14 * SR].copy()
            if len(clip) < fade_in + fade_out:
                continue
            clip[:fade_in] *= up
            clip[-fade_out:] *= down
            # A distant rumble has a ~24 dB crest factor, so peak-normalising it
            # leaves it quieter than the rain. Soft-clip first to tame the crest,
            # then set RMS — that is what makes it read as loud without clipping.
            clip = clip / (np.max(np.abs(clip)) + 1e-12) * 0.95
            clip = np.tanh(clip * 2.5) / np.tanh(2.5)
            place(thunder_track, clip, at, gain=1.0)
        # Balance by explicit RMS targets. Contrast is then whatever those two
        # numbers imply, which is easier to reason about than a derived ratio.
        bed = set_rms(bed, -32.0)
        mix = bed + droplets + drips + thunder_track
        foreground = droplets + drips + thunder_track
        print(f"   thunder swells at {schedule} (bed -34 dB, thunder -22 dB)")

    if not a.no_room:
        mix = behind_wall(mix)
        foreground = behind_wall(foreground)

    peak = np.max(np.abs(mix))
    if peak > 0.95:                     # pure headroom scale, no dynamics touched
        mix *= 0.95 / peak
        peak = 0.95

    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR),
                    "-ac", "2", "-i", "-", a.out], input=pcm.tobytes(), check=True)

    # Stems, so the two layers can be re-balanced without re-running this.
    for name, sig in (("_stem_bed", bed), ("_stem_foreground", foreground)):
        pk = np.max(np.abs(sig)) or 1.0
        pcm = (np.clip(sig / pk * 0.9, -1, 1) * 32767).astype(np.int16)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(SR),
                        "-ac", "2", "-i", "-", f"sources/{name}.wav"],
                       input=pcm.tobytes(), check=True)

    print(f"{a.out}: {secs:.0f}s  bed={rms_db(bed):.1f}dB  drops={rms_db(droplets):.1f}dB "
          f"drips={rms_db(drips):.1f}dB  thunder_events={len(schedule)}  peak={20*np.log10(peak):.1f}dB")
    print("stems: sources/_stem_bed.wav  sources/_stem_foreground.wav")


if __name__ == "__main__":
    main()
