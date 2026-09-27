"""One-time helper: mint the single-line YouTube credential on your laptop.

Feed it the OAuth client JSON you downloaded from Google Cloud
(Client secrets file, looks like {"installed": {"client_id": ...}}),
either as a pasted string or a file path:

  pip install google-auth-oauthlib
  python3 scripts/get_refresh_token.py --client-json-file ~/Downloads/client_secret.json
  python3 scripts/get_refresh_token.py --client-json '{"installed": {...}}'

A browser window opens, you sign in with the Google account that owns the
YouTube channel, and the script prints ONE line. Paste that whole line into
the repo secret YOUTUBE_CLIENT_JSON. Run once; the secret lives in GitHub after.
"""
import argparse
import json

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--client-json", default="",
                   help="Pasted client-secrets JSON string")
    g.add_argument("--client-json-file", default="",
                   help="Path to downloaded client_secret.json")
    g.add_argument("--client-id", default="")
    ap.add_argument("--client-secret", default="")
    a = ap.parse_args()

    if a.client_json_file:
        with open(a.client_json_file) as fh:
            raw = json.load(fh)
    elif a.client_json:
        raw = json.loads(a.client_json)
    else:
        raw = {"installed": {"client_id": a.client_id,
                             "client_secret": a.client_secret}}
    inner = raw.get("installed", raw.get("web", raw))
    flow = InstalledAppFlow.from_client_config(
        {"installed": {
            "client_id": inner["client_id"],
            "client_secret": inner["client_secret"],
            "redirect_uris": ["http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"}},
        SCOPES)
    creds = flow.run_local_server(port=0)
    one_line = json.dumps({"client_id": inner["client_id"],
                           "client_secret": inner["client_secret"],
                           "refresh_token": creds.refresh_token})
    print("\nPut this ONE line in the repo secret YOUTUBE_CLIENT_JSON:")
    print(one_line)


if __name__ == "__main__":
    main()
