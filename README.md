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

## Usage

```bash
# 8-hour 1080p video, stays private until you approve it on YouTube Studio
python3 make_long.py --from-id woods-7 --hours 8 --privacy private \
  --title "Rain in the Woods for Deep Sleep | 8 Hours"

# 1-hour test
python3 make_long.py --hours 1 --footage leaves --preview
```

Speed design: the cloud renders one 10-min seamless master (1080p, `veryfast`),
then extends it to 8h with a stream **copy** (no re-encode) — total target ≤40 min,
guarded by a 45-min job timeout. Audio is AAC 256k.

Every video opens with a 5s branded intro card (channel icon + subscribe pill,
`scripts/make_intro.py`) — human-made branding that also signals originality
to reviewers. To use your own hand-drawn avatar instead: save it over
`avatars/icon.png` and change `--icon` in the workflow + `make_intro` default.

Or trigger by hand: repo → *Actions → Render long ambient video → Run workflow*.

New rain "performance"? Change `--seed` (or `audio_seed` in the UI) — same
sources, different weather. Keep a note of which seed made which video.

## Things to know

- **YouTube quota:** uploads cost ~1600 API units; fresh projects get 10,000/day,
  so ~6 long uploads per day max. Publishing/private→public flips are free.
- **Sizes:** 720p rain ≈ 7 MB/min → 1h ≈ 430 MB, 8h ≈ 3.4 GB. Upload runs from
  the GitHub datacenter, not your home connection.
- **Reused-content rule:** YouTube can demonetize channels that mass-upload
  near-identical ambience. Vary titles, descriptions, footage and seeds, and
  space out uploads.
- **Licenses:** every source + its license is logged in `sources/SOURCES.md`.
  Re-read each file page before monetizing.
