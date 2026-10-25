# LICENSED ASSETS — audit 2026-10-25 (corrected)

Every license below was opened on the source page in-session. Audio character was **measured**, not assumed — see the spectral table.

## The correction

I previously called `gravity_rain_delay.wav` / `gravity_rain_drops.wav` "real field recordings". That was inferred from the filename and the CC BY badge, never from listening. They are **music/tonal**, not rain. Measured proof:

| File | Spectral flatness | Peak energy | Verdict |
|---|---|---|---|
| `rain_bg.ogg` | 0.776 | 0.067 | rain |
| `fs_56307_light_rain.wav` | **0.901** | 0.052 | rain |
| `fs_856405_bangkok_storm.wav` | 0.792 | 0.053 | rain |
| `fs_640650_hard_rain.wav` | 0.721 | 0.056 | rain |
| `fs_158690_rain_window.aiff` | 0.597 | 0.085 | rain |
| `rain_window.ogg` | 0.437 | 0.086 | rain |
| `gravity_rain_drops.wav` | 0.345 | **0.169** | tonal |
| `gravity_rain_delay.wav` | **0.111** | **0.228** | **music** |

Method: 20 s mono @16 kHz, 1 s windows, mean magnitude spectrum. *Flatness* ≈ 1.0 means broadband noise (rain). Low flatness + high narrow-peak energy means tonal content (music). Both Gravity files failed; both are now quarantined.

## ✅ Audio — real rain (Freesound, CC0)

Downloaded while logged in. All four are **Creative Commons 0** — verified on each sound page, not just from the search filter.

| File | Title | Recordist | Length | Format | Page |
|---|---|---|---|---|---|
| `fs_158690_rain_window.aiff` | Rain from Half Open Window 1 | **RutgerMuller** (rutgermuller.nl) | **5:08** | 48 kHz / 24-bit stereo, RØDE NT4 XY | [158690](https://freesound.org/people/RutgerMuller/sounds/158690/) |
| `fs_56307_light_rain.wav` | Rain_02 | **Q.K.** | **5:22** | 44.1 kHz / 16-bit stereo | [56307](https://freesound.org/people/Q.K./sounds/56307/) |
| `fs_640650_hard_rain.wav` | Hard rain and thunder | **barkenov** | **5:24** | 44.1 kHz / 24-bit stereo | [640650](https://freesound.org/people/barkenov/sounds/640650/) |
| `fs_856405_bangkok_storm.wav` | 20260531 Raining in Bangkok 01 | **kijjaz** | **6:00** | 48 kHz / 24-bit stereo, LOM Ucho → Volt 2 | [856405](https://freesound.org/people/kijjaz/sounds/856405/) |

That's the upgrade the channel actually needed: four continuous takes of 5–6 minutes, professional mics, covering the whole intensity range — gentle drizzle, window rain, heavy rain, full thunderstorm.

### Audio — public domain (Wikimedia Commons / PDSounds)

| File | Recordist | Length | Page |
|---|---|---|---|
| `rain_bg.ogg` | **ezwa** | 45 s | [Rain (1).ogg](https://commons.wikimedia.org/wiki/File:Rain_(1).ogg) |
| `rain_window.ogg` | **cori** | 82 s | [Rain against the window.ogg](https://commons.wikimedia.org/wiki/File:Rain_against_the_window.ogg) |

### Audio — Pixabay Content License

Licence read at https://pixabay.com/service/license-summary/ : free, **commercial use allowed**, **attribution not required**, modification allowed. Prohibited: selling/redistributing the content *standalone*, trademark use, misleading use.

| File | Title | Author | Length | Format | Page |
|---|---|---|---|---|---|
| `pixabay_gentle_rain_01.mp3` | Gentle Rain 01 | **DRAGON-STUDIO** | **10:00** | MP3 256 kbps, 48 kHz stereo | [437305](https://pixabay.com/sound-effects/nature-gentle-rain-01-437305/) |
| `pixabay_heavy_rain.mp3` | Heavy Rain | **DonRain** | **15:00** | MP3 255 kbps, 44.1 kHz stereo | [114710](https://pixabay.com/sound-effects/nature-heavy-rain-114710/) |
| `pixabay_night_thunder.mp3` | Night Rain with Distant Thunder | **MindMist** | **15:00** | MP3 255 kbps, 44.1 kHz stereo | [321446](https://pixabay.com/sound-effects/nature-night-rain-with-distant-thunder-321446/) |
| `pixabay_distant_thunder.mp3` | Distant continuous thunder | **Simon Spiers** (via freesound_community) | **18:36** | MP3 160 kbps, 22.05 kHz stereo | [25005](https://pixabay.com/sound-effects/nature-distant-continuous-thunder-25005/) |

Measured character (why each one exists):

| File | Flatness | <200 Hz | <60 Hz | Mean | Role |
|---|---|---|---|---|---|
| `pixabay_gentle_rain_01` | 0.888 | **0.5 %** | 0.2 % | −36.9 dB | bright drizzle — thin, needs a body layer |
| `pixabay_heavy_rain` | 0.694 | 7.5 % | 0.3 % | −31.6 dB | dense downpour — the base of the deep mix |
| `pixabay_night_thunder` | 0.864 | 2.2 % | 0.1 % | −22.8 dB | loudest, rolling thunder — spare bed |
| `fs_856405_bangkok_storm` | 0.697 | **20.5 %** | **4.0 %** | −37.5 dB | the real depth: 20 % of its energy is under 200 Hz |

The gentle bed's low end is thin (0.5 % below 200 Hz), so the gentle profile adds `fs_158690` at 12 % as a body layer — otherwise it reads as hiss on phone speakers. The deep profile instead uses the storm recording at unity and leans on EQ.

> **Correction:** an earlier note in this file said Pixabay was blocked by Cloudflare. That was wrong — the page loads normally in Chrome. My read had caught a transient interstitial. Pixabay is fully usable.

## ❌ Not usable

| File | License | Problem |
|---|---|---|
| `gravity_rain_delay.wav` | CC BY 4.0 | **it's music, not rain** + would force an attribution we don't need |
| `gravity_rain_drops.wav` | CC BY 4.0 | same |
| `rain_garden.ogg` | **FAL** | copyleft — derivative video must be FAL |
| `rain_heavy.ogg` | **CC BY-SA 3.0** | share-alike — the whole video inherits the license |

All four are in `sources/_quarantine/`. Never publish with them.

### Audio — foreground layer (Freesound, CC0)

These exist to be *heard*: the bed is a wash, these are individual drops.

| File | Title | Recordist | Length | Measured character | Page |
|---|---|---|---|---|---|
| `fs_658836_droplets_leaves.wav` | Droplets hitting leaves | **mariannadeoliveira** | 1:30 | 133 transients/40 s, crest 28.4 dB, 23.5 % under 200 Hz — dense, wet leaf texture | [658836](https://freesound.org/people/mariannadeoliveira/sounds/658836/) |
| `fs_459983_dripping_softly.mp3` | Rain Water Dripping Softly | **florianreichelt** | 3:58 | 8 transients/40 s, crest 19.4 dB — sparse, distinct drips | [459983](https://freesound.org/people/florianreichelt/sounds/459983/) |

Both confirmed **Creative Commons 0** on their own pages.

## ✅ Footage — Pexels License

Read at https://www.pexels.com/license/ : commercial use allowed, **attribution not required** (credited anyway), modification allowed. Not allowed: selling unaltered copies, redistributing as stock, implying endorsement.

| File | Creator | Link | Length | Max res | Loop |
|---|---|---|---|---|---|
| `pexels_30770305_1080.mp4` | **Vũ Ngọc Long** | [page](https://www.pexels.com/video/misty-rainforest-aerial-view-in-dense-fog-30770305/) | **120 s** | 4K | ★★★★★ |
| `pexels_36400524_1080.mp4` | **Aaron Burden** | [page](https://www.pexels.com/video/aerial-view-of-foggy-winter-forest-36400524/) | 62 s | 4K | ★★★★★ |
| `pexels_29039743_1080.mp4` | **Tom Fisk** | [page](https://www.pexels.com/video/misty-forest-with-dense-fog-aerial-view-29039743/) | 48 s | 4K | ★★★★★ |
| `pexels_13340258_1080.mp4` | **Tom Fisk** | [page](https://www.pexels.com/video/fog-over-trees-13340258/) | 44 s | 4K | ★★★★☆ |
| `pexels_34698830_1080.mp4` | **OvO Films** | [page](https://www.pexels.com/video/moody-aerial-view-of-kerala-s-lush-forest-34698830/) | 26 s | 4K | ★★★★☆ |
| `pexels_30120287_1080.mp4` | **Joshua Woroniecki** | [page](https://www.pexels.com/video/serene-pine-needles-with-raindrops-in-forest-30120287/) | 27 s | 4K | ★★★☆☆ |
| `pexels_4287975_1080.mp4` | **K** | [page](https://www.pexels.com/video/drone-footage-of-a-forest-in-the-morning-4287975/) | 22 s | 4K | ★★★☆☆ |
| `pexels_30228546_1080.mp4` | **EJ Merl** | [page](https://www.pexels.com/video/misty-forest-aerial-view-in-oregon-30228546/) | 12 s | 4K | B-roll only |
| `pexels_36344044_rain_overlay.mp4` | **Zaheer Ahmad** | [page](https://www.pexels.com/video/heavy-rain-falling-on-black-background-36344044/) | 14.8 s | 1080p60 | rain plate — screen-blended over the drone |

**Why the overlay exists:** the drone clip contains no rain. Screen-blending a black-background rain plate adds streaks without changing exposure. The flash at ~1.5 s is cut out and the rest trimmed to exactly 10.0 s.

Current settings: slowed 1.5×, scaled to 960×540 and tiled 2×2 (half-size drops, 4× density), blended in **RGB** at **0.10 opacity**. Measured: mean luma 95.3 → 95.5 (unchanged), edge detail +3 % — present as atmosphere, not as visible streaks.

4K master for the lead clip: `https://videos.pexels.com/video-files/30770305/13162099_3840_2160_30fps.mp4` (471 MB / 2:00, HTTP 200 verified).

## Attribution block (paste into every description)

```
Footage — Pexels License (commercial use, no attribution required;
credited because these people deserve it):
• "Misty Rainforest Aerial View in Dense Fog" — Vũ Ngọc Long
  https://www.pexels.com/video/misty-rainforest-aerial-view-in-dense-fog-30770305/
• "Aerial View of Foggy Winter Forest" — Aaron Burden
  https://www.pexels.com/video/aerial-view-of-foggy-winter-forest-36400524/
• "Misty Forest with Dense Fog Aerial View" — Tom Fisk
  https://www.pexels.com/video/misty-forest-with-dense-fog-aerial-view-29039743/
• "Fog Over Trees" — Tom Fisk
  https://www.pexels.com/video/fog-over-trees-13340258/
• "Moody Aerial View of Kerala's Lush Forest" — OvO Films
  https://www.pexels.com/video/moody-aerial-view-of-kerala-s-lush-forest-34698830/
• "Serene Pine Needles with Raindrops in Forest" — Joshua Woroniecki
  https://www.pexels.com/video/serene-pine-needles-with-raindrops-in-forest-30120287/

Rain recordings (CC0 / public domain — credited anyway):
• "Rain from Half Open Window 1" — RutgerMuller
  https://freesound.org/people/RutgerMuller/sounds/158690/
• "Rain_02" — Q.K.
  https://freesound.org/people/Q.K./sounds/56307/
• "Hard rain and thunder" — barkenov
  https://freesound.org/people/barkenov/sounds/640650/
• "20260531 Raining in Bangkok 01" — kijjaz
  https://freesound.org/people/kijjaz/sounds/856405/
• "Rain (1)" — ezwa (public domain)
  https://commons.wikimedia.org/wiki/File:Rain_(1).ogg
• "Rain against the window" — cori (public domain)
  https://commons.wikimedia.org/wiki/File:Rain_against_the_window.ogg
```

## About YouTube as a source

You suggested pulling rain sounds from YouTube videos that allow reuse. The honest position:

1. **CC BY videos** (YouTube has a licence filter: *Filters → Features → Creative Commons*) genuinely permit reuse **with attribution**. That part is fine.
2. **Downloading** from YouTube still breaks YouTube's Terms of Service, even when the content itself is CC-licensed. The copyright is clear; the *access* isn't. Risk is account-level, not legal — but it is a rule, and this channel is the asset.
3. **"Free to use" in a description is not a licence.** It's one person's sentence, usually written for "repost on your channel with credit", and it says nothing about monetised use, sublicensing, or Content ID. Treat it as ambiguous unless they state a licence.
4. **Better move:** ask the channel owner directly. Rain channels get asked constantly and often say yes — and a written "yes, credit me" email is stronger evidence than a scraped file, and gives you a relationship you can reuse.

If we ever do use a YouTube CC BY clip: record the exact title, channel URL, and the licence line from the description in this file before publishing.

## Gain / loudness — measured, because the files are not mastered

Raw levels of the four recordings (first 60 s each):

| File | Mean | Peak | Character |
|---|---|---|---|
| `fs_158690_rain_window.aiff` | −32.1 dB | −5.4 dB | loudest, close-mic'd window |
| `fs_856405_bangkok_storm.wav` | −36.8 dB | −12.3 dB | storm, wide dynamics |
| `fs_56307_light_rain.wav` | −34.7 dB | −15.6 dB | very quiet drizzle |
| `fs_640650_hard_rain.wav` | **−47.1 dB** | −17.7 dB | quiet despite the name — distant capture |

Straight mix sums to ~−36 dB mean, which is unusably quiet on YouTube. Normalise per file, then mix:

```bash
-af "aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-16:TP=-1.5:LRA=11"
```

Measured after that filter: **mean −20.5 dB, peak −2.0 dB** — healthy for ambient, no clipping, and the spectral character survives AAC encoding (flatness stayed 0.90 on the rendered MP4).

If a bed needs to sit under another, lower `I` by 3–4 dB rather than adding a compressor; compression makes rain pump, which is the one thing listeners notice.

## Pipeline consequence (action needed)

The GitHub Action runner **cannot log in to Freesound**, so it can't reproduce these four files. Two options:

1. **Recommended:** upload them once to a GitHub **Release** on this repo (2 GB per file allowed), then have `scripts/download_assets.sh` fetch the public release URLs. No secret, works forever.
2. Commit them (they're ~320 MB total) — works, but bloats the repo permanently.

The script currently leaves a `FREESOUND_RELEASE_BASE` hook for option 1. Until one of these is done, cloud renders fall back to the two PD Commons files only.

## Rules going forward

1. No asset enters `sources/` without its licence page opened in-session.
2. Reject **SA** and **NC** on sight.
3. **Measure audio, don't trust the filename.** Flatness + peak energy on every new file, logged here.
4. Credit is not a licence.
