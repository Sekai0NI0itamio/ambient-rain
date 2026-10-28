#!/usr/bin/env bash
# Long version from the 60 s master, without re-encoding the whole thing.
#
# Re-encoding 8 hours would take hours and produce a worse file than the master.
# Instead: the first minute is re-encoded once (it carries the title), the rest
# is the same 60 s master repeated through the concat demuxer as a stream copy.
# Measured seam: 2.4x the normal frame delta (a stream_loop copy gave 10.6x —
# it duplicates a frame at every join).
#
#   ./scripts/make_long_version.sh 28800
set -euo pipefail
cd "$(dirname "$0")/.."

TARGET="${1:-28800}"
MASTER="ambient_master_rain_60s.mp4"
AUDIO="audio_master_rain_600s.wav"
OUT="ambient_demo_${TARGET}s_rain.mp4"
REPEATS=$(( (TARGET + 59) / 60 ))

[ -f "$MASTER" ] || { echo "missing $MASTER — run make_layered_demo.sh first" >&2; exit 1; }
[ -f "$AUDIO" ]  || { echo "missing $AUDIO" >&2; exit 1; }

echo "== long version ${TARGET}s ($REPEATS x 60 s)"

# 0. delivery copy of the master. The master is crf 18 (~7 Mbps); copying that
#    for 8 hours would be a 26 GB file. One 60 s transcode, then everything is a
#    stream copy of it.
ffmpeg -y -nostdin -v error -threads 2 -i "$MASTER" -an -frames:v 3600 \
  -c:v libx264 -preset veryfast -crf 26 -pix_fmt yuv420p -r 60 /tmp/_delivery60.mp4

# 1. first minute with the title burned in (same encoder settings as delivery)
ffmpeg -y -nostdin -v error -threads 2 -i /tmp/_delivery60.mp4 -loop 1 -framerate 60 -i assets/title.png \
  -filter_complex "
    [1:v]scale=1920:1080:flags=lanczos,format=rgba,
      fade=t=in:st=2:d=2:alpha=1,
      fade=t=out:st=9:d=5:alpha=1[t];
    [0:v][t]overlay=0:0:format=auto[v]
  " -map "[v]" -frames:v 3600 -an \
  -threads 2 -c:v libx264 -preset veryfast -crf 26 -pix_fmt yuv420p -r 60 /tmp/_titled60.mp4

# 2. concat list: titled minute, then repeats of the clean master
printf "file '/tmp/_titled60.mp4'\n" > /tmp/_cat.txt
i=1
while [ "$i" -lt "$REPEATS" ]; do
  printf "file '/tmp/_delivery60.mp4'\n" >> /tmp/_cat.txt
  i=$((i + 1))
done
ffmpeg -y -nostdin -v error -f concat -safe 0 -i /tmp/_cat.txt -c copy -t "$TARGET" /tmp/_video_long.mp4

# free intermediates before the audio mux
rm -f /tmp/_delivery60.mp4 /tmp/_titled60.mp4 /tmp/_cat.txt

# 3+4. mux: copy video, encode audio in one pass (avoids a separate 8h audio file)
ffmpeg -y -nostdin -v error -i /tmp/_video_long.mp4 -stream_loop -1 -i "$AUDIO" -t "$TARGET" \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart "$OUT"

rm -f /tmp/_video_long.mp4
echo "== $OUT"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
