import json
import os
import pathlib

import stravalib.client

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
TOKEN_FILE = pathlib.Path(__file__).parents[1] / "strava_tokens.json"


def authenticate() -> None:
    """Authenticate with the Strava API and save the tokens."""
    client = stravalib.client.Client()
    auth_url = client.authorization_url(
        client_id=STRAVA_CLIENT_ID,
        redirect_uri="http://localhost",
        scope=["activity:read_all"],
    )
    print(f"Please visit this URL to authorize access: {auth_url}")

    auth_code = input("Enter the authorization code from the URL: ")
    token_response = client.exchange_code_for_token(
        client_id=STRAVA_CLIENT_ID,
        client_secret=STRAVA_CLIENT_SECRET,
        code=auth_code,
    )

    with pathlib.Path.open(TOKEN_FILE, "w") as f:
        json.dump(token_response, f, indent=2)
    print("Authentication successful. Tokens saved.")


if __name__ == "__main__":
    authenticate()
