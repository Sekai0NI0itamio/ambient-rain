"""Upload a video file to YouTube with resumable upload.

Auth: ONE repo secret, YOUTUBE_CLIENT_JSON:
  {"client_id": "...", "client_secret": "...", "refresh_token": "..."}
(Get it from scripts/get_refresh_token.py — paste the single line it prints.)
Legacy fallback: YOUTUBE_CLIENT_ID / YOUTUBE_CLIENT_SECRET / YOUTUBE_REFRESH_TOKEN.
Usage:
  YOUTUBE_CLIENT_JSON='<paste>' \
  python3 scripts/upload_youtube.py --file long.mp4 \
    --title "Rain ..." --description "..." --privacy private
"""
import argparse
import json
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--description", default="")
    ap.add_argument("--privacy", default="private",
                    choices=["private", "unlisted"],
                    help="private = draft, visible only to you")
    a = ap.parse_args()

    blob = os.environ.get("YOUTUBE_CLIENT_JSON", "")
    if blob:
        auth = json.loads(blob)
    else:  # legacy three-secret fallback
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

    body = {
        "snippet": {"title": a.title, "description": a.description,
                    "categoryId": "10"},
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(a.file, chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"[upload] {int(status.progress() * 100)}% ...")
    video_id = resp["id"]
    print(f"[upload] done: https://www.youtube.com/watch?v={video_id}")


if __name__ == "__main__":
    main()
