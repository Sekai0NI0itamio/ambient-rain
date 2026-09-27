"""One-time helper: mint a YouTube refresh token on your laptop.

You need a Google Cloud OAuth client first (README.md part A), then run:
  pip install google-auth-oauthlib
  python3 scripts/get_refresh_token.py --client-id ID --client-secret SECRET
A browser window opens, you sign in with the Google account that owns the
YouTube channel, and the script prints YOUTUBE_REFRESH_TOKEN. Paste it into
the repo secret of the same name. Run once; the token lives in GitHub after.
"""
import argparse

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--client-id", required=True)
    ap.add_argument("--client-secret", required=True)
    a = ap.parse_args()
    flow = InstalledAppFlow.from_client_config(
        {"installed": {"client_id": a.client_id,
                       "client_secret": a.client_secret,
                       "redirect_uris": ["http://localhost"],
                       "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                       "token_uri": "https://oauth2.googleapis.com/token"}},
        SCOPES)
    creds = flow.run_local_server(port=0)
    print("\nPut this in the repo secret YOUTUBE_REFRESH_TOKEN:")
    print(creds.refresh_token)


if __name__ == "__main__":
    main()
