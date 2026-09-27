#!/usr/bin/env bash
# Download source assets on the runner (nothing binary lives in git).
set -euo pipefail
mkdir -p sources
cd sources

fetch() {
  local out="$1"; local url="$2"
  if [ -f "$out" ]; then echo "cached: $out"; return; fi
  echo "downloading: $out"
  curl -L --fail --retry 3 -o "$out" "$url"
}

# Audio: Wikimedia Commons, Category:Sounds of rain (see SOURCES.md for licenses)
fetch "rain_bg.ogg"     "https://commons.wikimedia.org/wiki/Special:FilePath/Rain%20(1).ogg"
fetch "rain_window.ogg" "https://commons.wikimedia.org/wiki/Special:FilePath/Rain%20against%20the%20window.ogg"
fetch "rain_garden.ogg" "https://commons.wikimedia.org/wiki/Special:FilePath/Garden%20rainfall.ogg"
fetch "rain_heavy.ogg"  "https://commons.wikimedia.org/wiki/Special:FilePath/Heavy%20Rain%20in%20Summer.ogg"

# Video: Pexels, "Raindrops on a Glass Window" 720p (Pexels License, see SOURCES.md)
fetch "rain_window_home.mp4" "https://videos.pexels.com/video-files/5517022/5517022-hd_1280_720_30fps.mp4"

ls -lh
