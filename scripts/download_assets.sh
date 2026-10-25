#!/usr/bin/env bash
# Download source assets on the runner (nothing binary lives in git).
# Licences: see sources/LICENSED-ASSETS.md — PD / CC0 / Pexels only.
set -euo pipefail
mkdir -p sources footage/pexels
cd sources

# Where the Freesound originals are mirrored. Freesound needs a login, so the
# runner cannot fetch them directly. Upload sources/fs_*.{wav,aiff} once to a
# GitHub Release on this repo and point this at it, e.g.
#   export FREESOUND_RELEASE_BASE="https://github.com/USER/REPO/releases/download/assets-v1"
# Until then the render falls back to the public-domain files only.
FS_BASE="${FREESOUND_RELEASE_BASE:-}"

fetch() {
  local out="$1"; local url="$2"
  if [ -f "$out" ]; then echo "cached: $out"; return; fi
  echo "downloading: $out"
  curl -L --fail --retry 3 -o "$out" "$url"
}

# ---------------------------------------------------------------- audio: public domain
fetch "rain_bg.ogg"     "https://commons.wikimedia.org/wiki/Special:FilePath/Rain%20(1).ogg"
fetch "rain_window.ogg" "https://commons.wikimedia.org/wiki/Special:FilePath/Rain%20against%20the%20window.ogg"

# ---------------------------------------------------------------- audio: Pixabay
# Content License: commercial use, no attribution required (credited anyway).
fetch "pixabay_gentle_rain_01.mp3" "https://cdn.pixabay.com/download/audio/2025/11/15/audio_3f7ff9f3e2.mp3?filename=dragon-studio-gentle-rain-01-437305.mp3"
fetch "pixabay_heavy_rain.mp3"     "https://cdn.pixabay.com/download/audio/2022/07/10/audio_be2a209861.mp3?filename=donrain-heavy-rain-114710.mp3"
fetch "pixabay_night_thunder.mp3"  "https://cdn.pixabay.com/download/audio/2025/04/01/audio_18c9b25c48.mp3?filename=mindmist-night-rain-with-distant-thunder-321446.mp3"
fetch "pixabay_distant_thunder.mp3" "https://cdn.pixabay.com/download/audio/2022/03/09/audio_3781816d23.mp3?filename=freesound_community-distant-continuous-thunder-25005.mp3"

# ---------------------------------------------------------------- audio: Freesound CC0
# Real field recordings, 5-6 minutes each. Mirrored via release asset (see above).
if [ -n "$FS_BASE" ]; then
  fetch "fs_158690_rain_window.aiff" "$FS_BASE/fs_158690_rain_window.aiff"   # RutgerMuller, 5:08, 48k/24
  fetch "fs_56307_light_rain.wav"    "$FS_BASE/fs_56307_light_rain.wav"      # Q.K., 5:22
  fetch "fs_640650_hard_rain.wav"    "$FS_BASE/fs_640650_hard_rain.wav"      # barkenov, 5:24
  fetch "fs_856405_bangkok_storm.wav" "$FS_BASE/fs_856405_bangkok_storm.wav" # kijjaz, 6:00
  fetch "fs_658836_droplets_leaves.wav" "$FS_BASE/fs_658836_droplets_leaves.wav" # mariannadeoliveira, 1:30
  fetch "fs_459983_dripping_softly.mp3" "$FS_BASE/fs_459983_dripping_softly.mp3" # florianreichelt, 3:58
else
  echo "note: FREESOUND_RELEASE_BASE unset — using public-domain rain only"
fi

# REMOVED 2026-10-25 — do not re-add:
#   gravity_rain_*.wav  (CC BY 4.0 but MUSIC, not rain — spectral flatness 0.11)
#   rain_garden.ogg     (Lionel Allorge, FAL — copyleft)
#   rain_heavy.ogg      (Fiver, der Hellseher, CC BY-SA 3.0 — share-alike)

# ---------------------------------------------------------------- video: Pexels
# Commercial use, no attribution required (credited anyway — see LICENSED-ASSETS.md).
fetch_v() {
  local out="$1"; local url="$2"
  if [ -f "$out" ]; then echo "cached: $out"; return; fi
  echo "downloading: $out"
  curl -L --fail --retry 3 -o "$out" "$url"
}

fetch_v "../footage/pexels/pexels_30770305_1080.mp4" "https://videos.pexels.com/video-files/30770305/13162097_1920_1080_30fps.mp4"  # Vũ Ngọc Long, 120s
fetch_v "../footage/pexels/pexels_36400524_1080.mp4" "https://videos.pexels.com/video-files/36400524/15436567_1920_1080_30fps.mp4"  # Aaron Burden, 62s
fetch_v "../footage/pexels/pexels_29039743_1080.mp4" "https://videos.pexels.com/video-files/29039743/12554116_1920_1080_30fps.mp4"  # Tom Fisk, 48s
fetch_v "../footage/pexels/pexels_13340258_1080.mp4" "https://videos.pexels.com/video-files/13340258/13340258-hd_1920_1080_30fps.mp4"  # Tom Fisk, 44s
fetch_v "../footage/pexels/pexels_34698830_1080.mp4" "https://videos.pexels.com/video-files/34698830/14707304_1920_1080_60fps.mp4"  # OvO Films, 26s
fetch_v "../footage/pexels/pexels_30120287_1080.mp4" "https://videos.pexels.com/video-files/30120287/12918302_1920_1080_30fps.mp4"  # Joshua Woroniecki, 27s
fetch_v "../footage/pexels/pexels_4287975_1080.mp4" "https://videos.pexels.com/video-files/4287975/4287975-hd_1920_1080_24fps.mp4"  # K, 22s
fetch_v "../footage/pexels/pexels_30228546_1080.mp4" "https://videos.pexels.com/video-files/30228546/12960134_1920_1080_60fps.mp4"  # EJ Merl, 12s
fetch_v "../footage/pexels/pexels_36344044_rain_overlay.mp4" "https://videos.pexels.com/video-files/36344044/15415146_1920_1080_60fps.mp4"  # Zaheer Ahmad, rain plate

ls -lh . ../footage/pexels
