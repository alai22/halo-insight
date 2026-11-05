#!/usr/bin/env python3
"""
One-time sign-in that lets the Gmail ingester read the ai_logs_ingest inbox.

Run it on a laptop, not the server. A browser opens: sign in as the inbox
(not your own account) and approve read-only Gmail access. It prints the three
LABELING_GMAIL_OAUTH_* lines to add to the server's .env.

Usage:
  pip install google-auth-oauthlib google-api-python-client
  python authorize_labeling_gmail.py client_secret.json
  python authorize_labeling_gmail.py client_secret.json --mailbox someone@halocollar.com

client_secret.json is the OAuth client (type Desktop app) downloaded from Google
Cloud Console. See docs/LABELING_GMAIL_INGEST.md.
"""

from __future__ import annotations

import argparse
import sys

GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
DEFAULT_MAILBOX = "ai_logs_ingest@halocollar.com"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("client_secret", help="OAuth client JSON (Desktop app) from Cloud Console")
    parser.add_argument("--mailbox", default=DEFAULT_MAILBOX, help=f"Inbox to authorize (default {DEFAULT_MAILBOX})")
    args = parser.parse_args(argv)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print("Run first: pip install google-auth-oauthlib google-api-python-client", file=sys.stderr)
        return 2

    flow = InstalledAppFlow.from_client_secrets_file(args.client_secret, scopes=[GMAIL_READONLY_SCOPE])
    print(f"A browser will open. Sign in as {args.mailbox} and approve read-only access.")
    # prompt=consent so Google always returns a refresh token, even on a repeat run.
    creds = flow.run_local_server(port=0, login_hint=args.mailbox, prompt="consent", access_type="offline")

    gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)
    actual = (gmail.users().getProfile(userId="me").execute().get("emailAddress") or "").lower()
    if actual != args.mailbox.lower():
        print(
            f"Signed in as {actual}, not {args.mailbox}. Nothing to save. Run again and pick "
            f"{args.mailbox} in the browser, or revoke this at https://myaccount.google.com/permissions.",
            file=sys.stderr,
        )
        return 1
    if not creds.refresh_token:
        print("Google returned no refresh token. Run again.", file=sys.stderr)
        return 1

    print(f"\nAuthorized {actual} (read-only). Add these to ~/halo-insight/.env on the server,")
    print("then redeploy. Treat them like a password; never commit them.\n")
    print(f"LABELING_GMAIL_OAUTH_CLIENT_ID={creds.client_id}")
    print(f"LABELING_GMAIL_OAUTH_CLIENT_SECRET={creds.client_secret}")
    print(f"LABELING_GMAIL_OAUTH_REFRESH_TOKEN={creds.refresh_token}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
