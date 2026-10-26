"""Upload a video file to YouTube with resumable upload.

Auth: ONE repo secret, YOUTUBE_CLIENT_JSON:
  {"client_id": "...", "client_secret": "...", "refresh_token": "..."}
(Get it from scripts/get_refresh_token.py — paste the single line it prints.)

Usage:
  YOUTUBE_CLIENT_JSON='<paste>' python3 scripts/upload_youtube.py \
    --file long.mp4 --meta upload/metadata.json --thumbnail assets/thumbnail.jpg

Scheduling: pass --publish-at with an ISO timestamp and the video is uploaded
private with a scheduled release. YouTube requires >= 15 minutes in the future.
"""
import argparse
import json
import os
from datetime import datetime, timedelta, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--meta", help="JSON with title/description/tags/categoryId")
    ap.add_argument("--title")
    ap.add_argument("--description", default="")
    ap.add_argument("--tags", default="", help="comma separated")
    ap.add_argument("--category", default="10")
    ap.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    ap.add_argument("--publish-at", help="ISO 8601, e.g. 2026-10-30T19:00:00Z")
    ap.add_argument("--thumbnail", help="1280x720 JPEG/PNG")
    a = ap.parse_args()

    meta = {}
    if a.meta:
        with open(a.meta, encoding="utf-8") as fh:
            meta = json.load(fh)

    title = a.title or meta.get("title", "Ambient rain")
    description = a.description or meta.get("description", "")
    tags = [t.strip() for t in (a.tags.split(",") if a.tags else meta.get("tags", [])) if t.strip()]
    category = a.category if a.category != "10" else str(meta.get("categoryId", "10"))

    blob = os.environ.get("YOUTUBE_CLIENT_JSON", "")
    if blob:
        auth = json.loads(blob)
    else:
        auth = {"client_id": os.environ["YOUTUBE_CLIENT_ID"],
                "client_secret": os.environ["YOUTUBE_CLIENT_SECRET"],
                "refresh_token": os.environ["YOUTUBE_REFRESH_TOKEN"]}

    creds = Credentials(
        token=None,
        refresh_token=auth["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=auth["client_id"],
        client_secret=auth["client_secret"],
        scopes=SCOPES,
    )
    yt = build("youtube", "v3", credentials=creds)

    status = {
        "privacyStatus": a.privacy,
        "selfDeclaredMadeForKids": False,
        "license": "youtube",
        "embeddable": True,
    }
    if a.publish_at:
        when = datetime.fromisoformat(a.publish_at.replace("Z", "+00:00"))
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        if when < datetime.now(timezone.utc) + timedelta(minutes=15):
            raise SystemExit("--publish-at must be at least 15 minutes in the future")
        status["privacyStatus"] = "private"
        status["publishAt"] = when.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:4900],
            "tags": tags[:30],
            "categoryId": category,
            "defaultLanguage": "en",
            "defaultAudioLanguage": "en",
        },
        "status": status,
    }
    print(f"[upload] title: {body['snippet']['title']}")
    print(f"[upload] tags: {len(tags)} | privacy: {status['privacyStatus']}"
          + (f" | publishAt: {status.get('publishAt')}" if status.get("publishAt") else ""))

    media = MediaFileUpload(a.file, chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        chunk, resp = req.next_chunk()
        if chunk:
            print(f"[upload] {int(chunk.progress() * 100)}% ...")
    video_id = resp["id"]
    print(f"[upload] done: https://www.youtube.com/watch?v={video_id}")

    if a.thumbnail and os.path.exists(a.thumbnail):
        try:
            yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(a.thumbnail)).execute()
            print("[upload] thumbnail set")
        except Exception as exc:  # channel must be verified for custom thumbnails
            print(f"[upload] thumbnail failed: {exc}")


if __name__ == "__main__":
    main()
