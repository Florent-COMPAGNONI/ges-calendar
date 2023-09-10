import os
import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from ics import Calendar, Event

load_dotenv()

CLIENT_ID = "skolae-app"
USER_AGENT = "skolae-app-ios/3.5.0 (com.reseauges.skolae.app; build:26; iOS 15.0.1) Alamofire/4.9.1"
OAUTH_AUTHORIZE_URL = f"https://authentication.kordis.fr/oauth/authorize?client_id={CLIENT_ID}&response_type=token"
AGENDA_ENDPOINT_URL = "https://api.kordis.fr/me/agenda"
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


def get_access_token() -> str:
    response = requests.get(
        url=OAUTH_AUTHORIZE_URL,
        auth=(USERNAME, PASSWORD),
        allow_redirects=False,
    )

    if response.status_code == 401:
        raise Exception("Wrong credentials")

    access_token = extract_access_token(response.headers)

    return access_token


def extract_access_token(headers: dict) -> str:
    location = headers.get("Location")

    if not location:
        raise Exception("Location header not found")

    location_url = urlparse(location)

    if not location_url.fragment:
        raise Exception("Impossible to extract fragment")

    query_params = parse_qs(location_url.fragment)
    access_token = query_params.get("access_token")

    if not access_token:
        raise Exception("Impossible to extract access token")

    return access_token[0]


if __name__ == "__main__":
    access_token = get_access_token()
    print(access_token)
