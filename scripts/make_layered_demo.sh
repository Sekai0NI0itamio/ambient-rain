#!/usr/bin/env bash
# Layered rain demo: drone shot + rain overlay + 3-layer audio (bed / drops / thunder).
#
#   ./scripts/make_layered_demo.sh              # 10 minutes
#   MINUTES=28800 ./scripts/make_layered_demo.sh
#
# Audio is a 10-minute bespoke mix (make_rain_mix.py) rather than a 60s loop, so
# thunder lands at chosen times instead of repeating every minute. Video stays a
# 60s seamless master and is looped; both are re-encoded once at the end.
set -euo pipefail
cd "$(dirname "$0")/.."

FOOTAGE="${FOOTAGE:-footage/pexels/pexels_30770305_1080.mp4}"
OVERLAY="${OVERLAY:-footage/pexels/pexels_36344044_rain_overlay.mp4}"
IN="${IN:-48}"
OUT="${OUT:-110}"
XF="${XF:-2}"
MINUTES="${MINUTES:-600}"
OVERLAY_OPACITY="${OVERLAY_OPACITY:-0.10}"
OVERLAY_SLOW="${OVERLAY_SLOW:-0.8333}"

SEG=$(python3 -c "print($OUT-$IN)")
M=$(python3 -c "print($SEG-$XF)")
MID_END=$(python3 -c "print($SEG-$XF)")
TAIL_START=$(python3 -c "print($SEG-$XF)")

# The plate has FOUR flashes (1.57, 3.03, 4.30, 11.97 s) — a 2 fps scan only
# finds the first. Only 4.45-11.95 s is clean. That 7.5 s is then crossfaded
# end-into-start to make a seamless 6.0 s loop: without the crossfade the streaks
# jump every loop, which reads as rain stuttering. Seam measures 0.97x the
# normal frame-to-frame difference, i.e. invisible.
if [ ! -f footage/pexels/rain_seamless_6s.mp4 ]; then
  echo "== building seamless rain plate"
  ffmpeg -y -v error -ss 4.45 -t 7.5 -i "$OVERLAY" -an \
    -c:v libx264 -preset veryfast -crf 14 -pix_fmt yuv420p /tmp/_plate_clean.mp4
  ffmpeg -y -v error -i /tmp/_plate_clean.mp4 -filter_complex "
    [0:v]split[a][b];
    [a]trim=0:6,setpts=PTS-STARTPTS[head];
    [b]trim=6:7.5,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=4.5[tail];
    [tail][head]blend=all_expr='A*(1-min(T/1.5,1))+B*min(T/1.5,1)',format=yuv420p[out]
  " -map "[out]" -t 6 -an -c:v libx264 -preset veryfast -crf 14 \
    footage/pexels/rain_seamless_6s.mp4
  rm -f /tmp/_plate_clean.mp4
fi

echo "== video master ${M}s (drone + rain overlay)"
ffmpeg -y -v warning -stats \
  -ss "$IN" -t "$SEG" -i "$FOOTAGE" \
  -stream_loop 11 -i footage/pexels/rain_seamless_6s.mp4 \
  -filter_complex "
    [0:v]split=3[v1][v2][v3];
    [v1]trim=start=${XF}:end=${MID_END},setpts=PTS-STARTPTS[mid];
    [v2]trim=start=${TAIL_START}:end=${SEG},setpts=PTS-STARTPTS[tail];
    [v3]trim=start=0:end=${XF},setpts=PTS-STARTPTS[head];
    [tail][head]xfade=transition=fade:duration=${XF}:offset=0[xf];
    [xf][mid]concat=n=2:v=1:a=0,
      scale=1920:1080:force_original_aspect_ratio=increase,
      crop=1920:1080,setsar=1,fps=60[drone];
    [1:v]setpts=${OVERLAY_SLOW}*PTS,fps=60,scale=960:540,
      curves=all='0/0 0.02/0 0.15/0.45 1/1',split=4[q1][q2][q3][q4];
    [q2]hflip[q2f];[q4]hflip[q4f];
    [q1][q2f][q3][q4f]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0,format=gbrp[rain];
    [drone]eq=brightness=-0.06:saturation=0.88:contrast=1.02,format=gbrp[drone_rgb];
    [drone_rgb][rain]blend=all_mode=screen:all_opacity=${OVERLAY_OPACITY},
      format=yuv420p[vout]
  " \
  -map "[vout]" -an -t "$M" \
  -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r 60 -movflags +faststart \
  "ambient_master_rain_${M}s.mp4"

echo "== audio master (bed + drops + thunder)"
python3 scripts/make_rain_mix.py --minutes 10 --out sources/_mix_raw.wav --thunder
# No EQ: the chosen bed is used exactly as auditioned.
# Peak-normalised, not loudness-normalised. A loudness target forces the gain
# down until the loudest thunder fits inside it — that is the "suppression" this
# build removes. Peaks now land at -1.5 dBTP and the dynamics stay as recorded;
# set LOUDNESS_TARGET=-26 to get the quiet, level-matched variant instead.
ffmpeg -y -v error -i sources/_mix_raw.wav -af "lowpass=f=18000" -c:a pcm_f32le /tmp/_mix_eq.wav
PEAK=$(ffmpeg -hide_banner -i /tmp/_mix_eq.wav -af loudnorm=I=-26:TP=-3:print_format=json -f null - 2>&1 | grep '"input_tp"' | grep -o '[-0-9.]*')
if [ -n "${LOUDNESS_TARGET:-}" ]; then
  LOUD=$(ffmpeg -hide_banner -i /tmp/_mix_eq.wav -af loudnorm=I=-26:TP=-3:print_format=json -f null - 2>&1 | grep '"input_i"' | grep -o '[-0-9.]*')
  GAIN=$(python3 -c "print(round(${LOUDNESS_TARGET} - ($LOUD), 2))")
  echo "   loudness mode: ${LOUD} LUFS -> gain ${GAIN} dB"
else
  GAIN=$(python3 -c "print(round(-1.5 - ($PEAK), 2))")
  echo "   peak mode: ${PEAK} dBTP -> gain ${GAIN} dB (dynamics untouched)"
fi
ffmpeg -y -v error -i /tmp/_mix_eq.wav -af "volume=${GAIN}dB" -c:a pcm_s16le "audio_master_rain_600s.wav"
rm -f /tmp/_mix_eq.wav
rm -f sources/_mix_raw.wav

echo "== combining to ${MINUTES}s"
VLOOPS=$(python3 -c "import math; print(max(0, math.ceil($MINUTES/$M)-1))")
ALOOPS=$(python3 -c "import math; print(max(0, math.ceil($MINUTES/600)-1))")
# Title lives here, not in the master: the master loops every 60 s and would
# re-show it. Fade in 2-4 s, hold 5 s, fade out 9-14 s, nothing after.
ffmpeg -y -v warning -stats \
  -stream_loop "$VLOOPS" -i "ambient_master_rain_${M}s.mp4" \
  -stream_loop "$ALOOPS" -i "audio_master_rain_600s.wav" \
  -loop 1 -framerate 60 -i assets/title.png \
  -filter_complex "
    [2:v]format=rgba,
      fade=t=in:st=2:d=2:alpha=1,
      fade=t=out:st=9:d=5:alpha=1[t];
    [0:v][t]overlay=0:0:format=auto[v]
  " \
  -map "[v]" -map 1:a \
  -t "$MINUTES" \
  -c:v libx264 -preset veryfast -crf 26 -pix_fmt yuv420p -r 60 \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart \
  "ambient_demo_${MINUTES}s_rain.mp4"

echo "== done"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "ambient_demo_${MINUTES}s_rain.mp4"
