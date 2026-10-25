# Ambient Rain — cloud renderer

Local laptop renders previews. GitHub renders the 1h/8h monsters and uploads
them straight to YouTube. Big bytes never touch your home internet.

## How it works

1. You run `python3 make_long.py --hours 8 ...` (or click *Run workflow* in Actions).
2. A GitHub runner downloads the CC0 sources itself (`scripts/download_assets.sh`),
   renders a 10-minute seamless master, loop-extends it to 8h, uploads to YouTube.
3. The YouTube link lands in the run summary + your terminal.

## One-time setup (15 min)

### A. Google Cloud (do this in your browser)

1. Go to https://console.cloud.google.com/ → new project, any name (e.g. `ambient-rain`).
2. *APIs & Services → Library* → enable **YouTube Data API v3**.
3. *APIs & Services → OAuth consent screen* → type **External**, fill app name + your
   email, add yourself as a **test user**, save.
4. *APIs & Services → Credentials → Create Credentials → OAuth client ID* →
   type **Desktop app** → Create. Copy the **Client ID** and **Client secret**.
5. Verify your YouTube channel for long uploads: https://www.youtube.com/verify
   (phone SMS — required for anything over 15 minutes).

### B. One credential (runs on your laptop, once)

You downloaded the OAuth client JSON from Google Cloud — feed it straight in:

```bash
pip install google-auth-oauthlib
python3 scripts/get_refresh_token.py --client-json-file ~/Downloads/client_secret*.json
# ...or paste the JSON string directly:
python3 scripts/get_refresh_token.py --client-json '{"installed": {...}}'
```

Sign in with the Google account that owns the channel. It prints **one line**.

### C. Repo secret (repo → Settings → Secrets and variables → Actions → New)

| Name | Value |
|---|---|
| `YOUTUBE_CLIENT_JSON` | the one line from step B — that's the only secret |

Nobody else can see it, not even in forks. This repo is **private**:
free-plan Actions include ~2000 runner minutes/month (one 8h render ≈ 30–60 min).

## Check samples locally first (everything is ~1 minute)

```bash
python3 make_long.py --preview-all   # renders preview_window/woods/leaves.mp4, no upload
```

Watch the three, pick your scenery, then launch the matching 8h command.

## Seamless ambient demos (new)

```bash
./scripts/make_loop_points.py footage/pexels/pexels_30770305_1080.mp4 --min-len 62 --max-len 62
./scripts/make_ambient_demo.sh                    # gentle rain, 60s master -> 10 min
PROFILE=deep ./scripts/make_ambient_demo.sh       # heavy/deep rain, darker + quieter
MINUTES=28800 ./scripts/make_ambient_demo.sh      # same master -> 8 hours
```

Two audio profiles, same footage and same loop point:

| | **gentle** | **deep** |
|---|---|---|
| Rain bed | Gentle Rain 01 (DRAGON-STUDIO) | Heavy Rain (DonRain) |
| Body | window rain @ 12 % | Bangkok storm @ 100 % |
| EQ | none | bass +9 dB @ 95 Hz, treble −5 dB @ 6 kHz, lowpass 12 kHz |
| Loudness | −26 LUFS | −28 LUFS |
| Picture | brightness −0.06, sat 0.88 | brightness −0.13, sat 0.62, contrast 1.08 |
| Result | 2.1 % below 200 Hz, 22 % hiss | **16.2 % below 200 Hz, 4 % hiss** |

Measured on the rendered files, not assumed: the deep version carries ~7× more low end and ~5× less top-end air, so it is heavier *and* softer — not just louder.

## Layered rain (drone + rain plate + 3-layer audio)

```bash
./scripts/make_layered_demo.sh                        # 10 min, thunder off
./scripts/make_layered_demo.sh                        # add thunder: --thunder in make_rain_mix
OVERLAY_OPACITY=0.25 ./scripts/make_layered_demo.sh   # if you want the rain more obvious
MINUTES=28800 ./scripts/make_layered_demo.sh
```

**Picture** — a black-background rain plate (`pexels_36344044`) screen-blended over the drone. To get fine, slow, dense rain rather than big visible streaks:

- slowed to **0.8333×** (`setpts`) — 12 passes of 5.0 s land exactly on the 60 s master
- the 6 s plate is **crossfaded end-into-start** so the loop point measures 0.97× a normal frame change; without it the streaks jump every pass and read as rain stuttering
- scaled to **960×540 and tiled 2×2** (horizontal mirror only — `vflip` makes rain fall *upward*) — every drop is half size and the count quadruples
- blended in **RGB (`format=gbrp`)**, not YUV — see the bug note below
- at **0.10 opacity**, so it reads as atmosphere: mean luma 95.3 → 95.5, edge detail only **+3 %**

The plate contains **four** lightning flashes (1.57 s, 3.03 s, 4.30 s, 11.97 s). A 2 fps scan only catches the first — scan at full frame rate or you will ship the others. Only 4.45–11.95 s is clean; that 7.5 s is slowed 2× to 15 s, and 4 loops land exactly on the 60 s master.

> **Blend bug worth remembering:** blending in YUV lifts the whole frame and wrecks colour, because `screen` applied to the U/V planes (neutral 128) pushes chroma to ~191. Measured: mean luma jumped 95.7 → 126 at 0.35 opacity. Converting both inputs to `gbrp` first fixed it (95.7 → 96.7). Any future compositing here must blend in RGB.

**Sound** — three layers, built by `scripts/make_rain_mix.py`:

| Layer | Source | Level | Role |
|---|---|---|---|
| Rain bed | rainstorm — klangfabrik (Freesound 194209) | −32 dB RMS target | the background wash |
| Thunder | Distant rolling constant — TRP (Freesound 572444) | peak −3 dBFS per swell, 10 events | passes by every 55–67 s |

The droplet layers are gone (`--drops` re-enables them). Beds are chosen by measurement, not by name: **discrete drops per minute** is the dripping-tap test. Gentle Rain 01 scored 52/min, Heavy Rain (DonRain) 0.5/min, and the chosen klangfabrik rainstorm **0.6/min** with the flattest level (1.9 dB variance) of everything auditioned. If a plink comes back, check the bed first, not the foreground layers.

Unused candidates are kept in `sources/candidates/` — four auditions and six more not yet downloaded, listed in `sources/AUDIO-CANDIDATES.md`.

Thunder is cut from **42 rumble swells** in an 18-minute distant-thunder recording (Simon Spiers), soft-clipped to tame a 24 dB crest factor, and given a **3 s fade in / 4 s fade out** so it rolls in and clears out. Placed at 35, 92, 150, 205, 268, 325, 392, 448, 515 and 572 s — gaps of 55–67 s.

Measured in the delivered file: rain −35.5 dB RMS, thunder −18.2 dB, **contrast 17.3 dB**, thunder peaks −1.9 dBFS, **0.2 drop events/min**.

Audio is **peak-normalised, not loudness-normalised** — peaks land at −1.5 dBTP and the dynamics stay as recorded. A loudness target forces the gain down until the loudest thunder fits inside it, which is the suppression this build removes. `LOUDNESS_TARGET=-26 ./scripts/make_layered_demo.sh` restores the quiet, level-matched variant.

Also removed: the soft-clip that used to tame thunder's 24 dB crest factor (it was flattening the swells), and the limiter. The only processing left on the bed is a clamp on **165 samples out of 57 million** (MP3 overs, −0.0003 %) and a uniform headroom scale.

**LRA is now 18.6 LU**, well outside the 4–8 LU that the sleep literature recommends — an unavoidable consequence of loud thunder occupying 23 % of the timeline. The no-thunder build sits near 4. Worth testing both on real listeners before the 8-hour upload.

**Final:** −20.4 LUFS, peak −1.5 dBTP, LRA 18.6, 1.15 Mbps — an 8-hour render lands around 4.2 GB. The louder level is the direct cost of not suppressing: peaks had to be allowed to reach −1.5 dBTP.

Why those numbers: see `sources/AUDIO-RESEARCH.md`. The spectral slope is now **−15.9 dB/decade** (pink is −9, brown −18) because the heavy bed is naturally darker; the earlier gentle bed sat at −7.4.
