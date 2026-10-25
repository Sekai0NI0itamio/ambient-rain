# Sources

> **2026-10-25 audit (corrected):** two original audio files are copyleft and must never ship in a monetized video, and two "rain" WAVs turned out to be **music**. Full evidence, spectral measurements and credits: `LICENSED-ASSETS.md`. Downloads: `../scripts/download_assets.sh`.

## Audio — real rain, CC0 (Freesound)
| File | Title | Recordist | Length | Format | Page |
|---|---|---|---|---|---|
| `fs_158690_rain_window.aiff` | Rain from Half Open Window 1 | RutgerMuller | 5:08 | 48 kHz/24-bit | https://freesound.org/people/RutgerMuller/sounds/158690/ |
| `fs_56307_light_rain.wav` | Rain_02 | Q.K. | 5:22 | 44.1 kHz/16-bit | https://freesound.org/people/Q.K./sounds/56307/ |
| `fs_640650_hard_rain.wav` | Hard rain and thunder | barkenov | 5:24 | 44.1 kHz/24-bit | https://freesound.org/people/barkenov/sounds/640650/ |
| `fs_856405_bangkok_storm.wav` | 20260531 Raining in Bangkok 01 | kijjaz | 6:00 | 48 kHz/24-bit | https://freesound.org/people/kijjaz/sounds/856405/ |

All four verified **Creative Commons 0** on their individual pages. Freesound requires a login to download — the GitHub runner cannot reproduce these; host them as a release asset (see LICENSED-ASSETS.md → Pipeline consequence).

## Audio — Pixabay Content License (commercial OK, no attribution required)
- `pixabay_gentle_rain_01.mp3` — "Gentle Rain 01" — **DRAGON-STUDIO** — 10:00, MP3 256 kbps / 48 kHz. https://pixabay.com/sound-effects/nature-gentle-rain-01-437305/
- `pixabay_heavy_rain.mp3` — "Heavy Rain" — **DonRain** — 15:00, heavy downpour with distant thunder. https://pixabay.com/sound-effects/nature-heavy-rain-114710/
- `pixabay_night_thunder.mp3` — "Night Rain with Distant Thunder" — **MindMist** — 15:00, rolling thunder (spare). https://pixabay.com/sound-effects/nature-night-rain-with-distant-thunder-321446/
- `candidates/rain_194209_klangfabrik.mp3` — **rainstorm** — **klangfabrik** — 8:32, CC0. Chosen bed: 0.6 drops/min, 1.9 dB variance. https://freesound.org/people/klangfabrik/sounds/194209
- `candidates/thunder_572444_TRP.mp3` — **Thunder, rolling med distant constant, light rain** — **TRP** — 4:28, CC0. Chosen thunder: 9 swells, 28.9 s apart. https://freesound.org/people/TRP/sounds/572444
- `pixabay_distant_thunder.mp3` — "Distant continuous thunder" — **Simon Spiers (Freesound)** — **18:36**, 42 rumble swells, used for the pass-by thunder layer. https://pixabay.com/sound-effects/nature-distant-continuous-thunder-25005/
- Licence read in-session: https://pixabay.com/service/license-summary/

## Audio — public domain (Wikimedia Commons / PDSounds)
- `rain_bg.ogg` — File:Rain (1).ogg, 45s, **public domain**, **ezwa**, PDSounds #682. https://commons.wikimedia.org/wiki/File:Rain_(1).ogg
- `rain_window.ogg` — File:Rain against the window.ogg, 1m22s, **public domain**, **cori**. https://commons.wikimedia.org/wiki/File:Rain_against_the_window.ogg

## ❌ QUARANTINED — do not publish
- `gravity_rain_delay.wav` — Gravity Sound, CC BY 4.0, but **it is music, not rain** (spectral flatness 0.11). https://commons.wikimedia.org/wiki/File:Rain_delay_(Gravity_Sound).wav
- `gravity_rain_drops.wav` — Gravity Sound, CC BY 4.0, **tonal** (flatness 0.34, peak 0.17). https://commons.wikimedia.org/wiki/File:Rain_drops_(Gravity_Sound).wav
- `rain_garden.ogg` — Lionel Allorge, **FAL** (copyleft). https://commons.wikimedia.org/wiki/File:Garden_rainfall.ogg
- `rain_heavy.ogg` — Fiver, der Hellseher, **CC BY-SA 3.0** (share-alike). https://commons.wikimedia.org/wiki/File:Heavy_Rain_in_Summer.ogg

## Audio — foreground layer, CC0 (Freesound)
- `fs_658836_droplets_leaves.wav` — "Droplets hitting leaves" — **mariannadeoliveira** — 1:30, 44.1 kHz stereo, 133 transients/40 s. https://freesound.org/people/mariannadeoliveira/sounds/658836/
- `fs_459983_dripping_softly.mp3` — "Rain Water Dripping Softly" — **florianreichelt** — 3:58, 44.1 kHz, 8 transients/40 s (sparse, distinct drips). https://freesound.org/people/florianreichelt/sounds/459983/
- Both verified **Creative Commons 0** on their own pages.

## Video — rain overlay, Pexels License
- `pexels_36344044_rain_overlay.mp4` — "Heavy Rain Falling on Black Background" — **Zaheer Ahmad** — 14.8 s, 1080p60, near-black (mean luma 4.9) so it screen-blends cleanly over the drone. Flash at ~1.5 s removed; looped as 10.0 s. https://www.pexels.com/video/heavy-rain-falling-on-black-background-36344044/

## Video — Pexels License (commercial use, no attribution required)
- `pexels_30770305_1080.mp4` — Misty Rainforest Aerial View in Dense Fog — **Vũ Ngọc Long** — 120s (4K master available)
- `pexels_36400524_1080.mp4` — Aerial View of Foggy Winter Forest — **Aaron Burden** — 62s
- `pexels_29039743_1080.mp4` — Misty Forest with Dense Fog Aerial View — **Tom Fisk** — 48s
- `pexels_13340258_1080.mp4` — Fog Over Trees — **Tom Fisk** — 44s
- `pexels_34698830_1080.mp4` — Moody Aerial View of Kerala's Lush Forest — **OvO Films** — 26s
- `pexels_30120287_1080.mp4` — Serene Pine Needles with Raindrops — **Joshua Woroniecki** — 27s
- `pexels_4287975_1080.mp4` — Drone Footage of a Forest in the Morning — **K** — 22s
- `pexels_30228546_1080.mp4` — Misty Forest Aerial View in Oregon — **EJ Merl** — 12s

Pexels license read in-session: https://www.pexels.com/license/

## Unsuitable / blocked
- **BBC Sound Effects** — personal/educational licence only, **not commercial**. Never use.
- **Mixkit** — free licence, 720p only, thin catalogue. Fallback only.
- **YouTube CC BY** — content licence permits reuse with attribution, but downloading breaks YouTube's ToS. Prefer asking the channel owner (see `../OUTREACH.md`).

> Pixabay was previously listed here as blocked. It is not — the page loads fine in Chrome; an earlier read caught a transient interstitial.

## Rules
- Keep this file updated with creator + licence URL per asset.
- Reject **SA** and **NC** on sight.
- **Measure audio before trusting it** — a file called "rain" can be a piano track.
- Re-read each file page before a monetization review; licences change.
