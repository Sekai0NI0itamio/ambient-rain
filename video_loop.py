"""Video looper v0.1 - seamless xfade loop + mux with generated rain.
Usage:
  python3 video_loop.py --src input.mp4 --audio rain_demo.wav --out ambient_demo.mp4 --loop-sec 12 --total 60
If no --src given, builds a synthetic rainy-gradient test source with ffmpeg.
"""
import argparse, subprocess, shlex, os

def run(cmd):
    print("+", cmd)
    r = subprocess.run(cmd, shell=True)
    if r.returncode != 0:
        raise SystemExit(r.returncode)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="")
    ap.add_argument("--audio", default="rain_demo.wav")
    ap.add_argument("--out", default="ambient_demo.mp4")
    ap.add_argument("--loop-sec", type=float, default=12)
    ap.add_argument("--total", type=float, default=60)
    ap.add_argument("--xfade", type=float, default=1.0)
    ap.add_argument("--height", type=int, default=720,
                    help="Output height (720, or 1080 to upscale). Width auto.")
    ap.add_argument("--preset", default="veryfast",
                    help="x264 speed preset (veryfast = fast cloud renders)")
    ap.add_argument("--crf", type=int, default=21)
    ap.add_argument("--abr", default="192k",
                    help="AAC audio bitrate (use 256k for best)")
    a = ap.parse_args()
    src = a.src
    if not src:
        src = "_testsrc.mp4"
        run(f"ffmpeg -y -f lavfi -i testsrc=size=1280x720:rate=30:duration=20 -f lavfi -i \"gradients=size=1280x720:rate=30:duration=20\" -filter_complex \"[0][1]blend=all_mode=overlay:all_opacity=0.35\" -c:v libx264 -pix_fmt yuv420p {shlex.quote(src)}")
    L, X = a.loop_sec, a.xfade
    looped = "_looped.mp4"
    loop_dur = L - X
    import math
    n_loops = max(1, math.ceil(a.total / loop_dur))
    run(f"ffmpeg -y -i {shlex.quote(src)} -filter_complex \"[0:v]trim=0:{L},setpts=PTS-STARTPTS[v0];[0:v]trim={X}:{L},setpts=PTS-STARTPTS[v1];[v0][v1]xfade=transition=fade:duration={X}:offset={L - 2*X},scale=-2:{a.height}[v]\" -map \"[v]\" -c:v libx264 -preset {a.preset} -crf {a.crf} -pix_fmt yuv420p {shlex.quote(looped)}")
    run(f"ffmpeg -y -stream_loop {n_loops} -i {shlex.quote(looped)} -i {shlex.quote(a.audio)} -map 0:v -map 1:a -t {a.total} -c:v copy -c:a aac -b:a {a.abr} -movflags +faststart -shortest {shlex.quote(a.out)}")
    print(f"wrote {a.out}")

if __name__ == "__main__":
    main()
