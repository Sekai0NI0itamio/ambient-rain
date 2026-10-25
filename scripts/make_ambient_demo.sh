#!/usr/bin/env bash
# Build a seamless ambient master, then extend it.
#
#   ./scripts/make_ambient_demo.sh                    # gentle rain, 60s master + 10 min
#   PROFILE=deep ./scripts/make_ambient_demo.sh       # heavy/deep rain, dimmer + darker
#   MINUTES=28800 ./scripts/make_ambient_demo.sh      # 8 hours
#   IN=48 OUT=110 ./scripts/make_ambient_demo.sh      # override the loop point
#
# The loop point is measured, not guessed: make_loop_points.py finds the frame
# pair in the footage whose structure matches best. The same "rotate at the seam"
# trick is applied to the audio, so the master loops with no visible cut and no
# audible click — which is what lets one clip run for hours.
set -euo pipefail
cd "$(dirname "$0")/.."

FOOTAGE="${FOOTAGE:-footage/pexels/pexels_30770305_1080.mp4}"
IN="${IN:-48}"          # loop in-point, seconds   (from make_loop_points.py)
OUT="${OUT:-110}"       # loop out-point, seconds
XF="${XF:-2}"           # crossfade, seconds
MINUTES="${MINUTES:-600}"
PROFILE="${PROFILE:-gentle}"

case "$PROFILE" in
  gentle)
    RAIN="sources/pixabay_gentle_rain_01.mp3"
    BODY="sources/fs_158690_rain_window.aiff"
    BODY_GAIN="0.12"
    AFX=""
    LUFS="-26"
    VEQ="eq=brightness=-0.06:saturation=0.88:contrast=1.02"
    SUFFIX=""
    ;;
  deep)
    # Heavy downpour for density + the Bangkok storm recording for real low-end
    # weight (it carries ~20% of its energy below 200 Hz vs 0.5% for gentle rain).
    # Then cut the air out of it: bass up, treble down, lowpass — heavier, but dim.
    RAIN="sources/pixabay_heavy_rain.mp3"
    BODY="sources/fs_856405_bangkok_storm.wav"
    BODY_GAIN="1.0"
    AFX="bass=g=9:f=95:w=0.8,treble=g=-5:f=6000:w=0.7,lowpass=f=12000,"
    LUFS="-28"
    VEQ="eq=brightness=-0.13:saturation=0.62:contrast=1.08"
    SUFFIX="_deep"
    ;;
  *) echo "unknown PROFILE=$PROFILE (gentle|deep)"; exit 1 ;;
esac

SEG=$(python3 -c "print($OUT-$IN)")
M=$(python3 -c "print($SEG-$XF)")
MID_END=$(python3 -c "print($SEG-$XF)")   # trim takes a duration, not an expression
TAIL_START=$(python3 -c "print($SEG-$XF)")
AEND=$(python3 -c "print(round($M+0.5,3))")
AHALF=$(python3 -c "print(round($AEND/2,3))")

echo "== profile=$PROFILE  master ${M}s  (source ${IN}s→${OUT}s, xfade ${XF}s, ${LUFS} LUFS)"

ffmpeg -y -v warning -stats \
  -ss "$IN" -t "$SEG" -i "$FOOTAGE" \
  -ss 120 -t "$AEND" -i "$RAIN" \
  -ss 120 -t "$AEND" -i "$BODY" \
  -filter_complex "
    [0:v]split=3[v1][v2][v3];
    [v1]trim=start=${XF}:end=${MID_END},setpts=PTS-STARTPTS[mid];
    [v2]trim=start=${TAIL_START}:end=${SEG},setpts=PTS-STARTPTS[tail];
    [v3]trim=start=0:end=${XF},setpts=PTS-STARTPTS[head];
    [tail][head]xfade=transition=fade:duration=${XF}:offset=0[xf];
    [xf][mid]concat=n=2:v=1:a=0,
      scale=1920:1080:force_original_aspect_ratio=increase,
      crop=1920:1080,setsar=1,fps=30,
      ${VEQ},format=yuv420p[vout];

    [1:a]atrim=start=0:end=${AEND},asetpts=PTS-STARTPTS,asplit=2[p1][p2];
    [p1]atrim=start=${AHALF}:end=${AEND},asetpts=PTS-STARTPTS[pb];
    [p2]atrim=start=0:end=${AHALF},asetpts=PTS-STARTPTS[pa];
    [pb][pa]acrossfade=d=0.5:c1=tri:c2=tri[pr];

    [2:a]atrim=start=0:end=${AEND},asetpts=PTS-STARTPTS,asplit=2[b1][b2];
    [b1]atrim=start=${AHALF}:end=${AEND},asetpts=PTS-STARTPTS[bb];
    [b2]atrim=start=0:end=${AHALF},asetpts=PTS-STARTPTS[ba];
    [bb][ba]acrossfade=d=0.5:c1=tri:c2=tri[br];

    [pr][br]amix=inputs=2:weights=1 ${BODY_GAIN}:normalize=0,
      aformat=sample_rates=48000:channel_layouts=stereo,
      ${AFX}loudnorm=I=${LUFS}:TP=-3:LRA=11[aout]
  " \
  -map "[vout]" -map "[aout]" -t "$M" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart \
  "ambient_master_${PROFILE}_${M}s.mp4"

echo "== extending to ${MINUTES}s"
LOOPS=$(python3 -c "import math; print(max(0, math.ceil($MINUTES/$M)-1))")
ffmpeg -y -v warning -stats -stream_loop "$LOOPS" -i "ambient_master_${PROFILE}_${M}s.mp4" \
  -t "$MINUTES" \
  -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -movflags +faststart \
  "ambient_demo_${MINUTES}s${SUFFIX}.mp4"

echo "== done"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "ambient_demo_${MINUTES}s${SUFFIX}.mp4"
