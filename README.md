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

### B. Refresh token (runs on your laptop, once)

```bash
pip install google-auth-oauthlib
python3 scripts/get_refresh_token.py --client-id YOUR_ID --client-secret YOUR_SECRET
```

Sign in with the Google account that owns the channel. It prints a token.

### C. Repo secrets (repo → Settings → Secrets and variables → Actions → New)

| Name | Value |
|---|---|
| `YOUTUBE_CLIENT_ID` | from step A4 |
| `YOUTUBE_CLIENT_SECRET` | from step A4 |
| `YOUTUBE_REFRESH_TOKEN` | from step B |

Nobody else can see them, not even in forks. The repo itself should be **public**
(public repos get unlimited free Actions minutes; code contains zero secrets).

## Usage

```bash
# 8-hour video, stays private until you approve it on YouTube Studio
python3 make_long.py --hours 8 \
  --title "Rain in the Woods for Deep Sleep | 8 Hours" \
  --privacy private --footage woods

# 1-hour test + local 60s preview first
python3 make_long.py --hours 1 --privacy unlisted --preview
```

## Preview gallery (pick on a website, then launch)

Don't guess which scenery works — watch and pick:

1. Repo → Settings → Pages → Source: **GitHub Actions** (one-time, 10 seconds).
2. Actions → *Preview gallery to Pages* → Run workflow (renders 60s window/woods/leaves previews, ~5 min).
3. Open the `github.io` link from the run summary. Each card has a **Copy 8h command** button.
4. Paste it on your laptop — the cloud renders the full 8h and uploads to YouTube.

To re-render previews with more rain seeds: Run workflow → `seeds: "7 21 42"`.

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
