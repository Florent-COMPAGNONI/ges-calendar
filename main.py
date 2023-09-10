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


def get_agenda(access_token: str, start: str, end: str) -> dict:
    start: datetime = datetime.strptime(start, "%Y-%m-%d")
    end: datetime = datetime.strptime(end, "%Y-%m-%d")
    end += relativedelta(months=1)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT,
    }
    params = {
        "start": int(start.timestamp()) * 1000,
        "end": int(end.timestamp()) * 1000,
    }

    response = requests.get(url=AGENDA_ENDPOINT_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"error {response.status_code}")

    response_data = response.json()

    if not response_data:
        print("no data...")

    return response_data.get("result")


if __name__ == "__main__":
    access_token = get_access_token()
    agenda = get_agenda(access_token, "2023-09-11", "2023-09-17")
    print(agenda)
