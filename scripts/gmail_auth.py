"""One-time local script: log in with the job mailbox and print a Gmail refresh token.

Usage: py scripts/gmail_auth.py client_secret.json
Log in with the mailbox that holds the 'Candidatures' label. Read-only scope only.
"""
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    sys.argv[1], scopes=["https://www.googleapis.com/auth/gmail.readonly"]
)
creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
print("\nGOOGLE_CLIENT_ID    =", creds.client_id)
print("GOOGLE_CLIENT_SECRET =", creds.client_secret)
print("GOOGLE_REFRESH_TOKEN =", creds.refresh_token)
print("\nCopie ces 3 valeurs dans GitHub > Settings > Secrets and variables > Actions.")
