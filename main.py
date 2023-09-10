import os
import requests
import argparse
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from ics import Calendar, Event

load_dotenv()

CLIENT_ID = "skolae-app"
USER_AGENT = "skolae-app-ios/3.5.0 (com.reseauges.skolae.app; build:26; iOS 15.0.1) Alamofire/4.9.1"
OAUTH_AUTHORIZE_URL = f"https://authentication.kordis.fr/oauth/authorize?client_id={CLIENT_ID}&response_type=token"
AGENDA_ENDPOINT_URL = "https://api.kordis.fr/me/agenda"
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")


def get_access_token() -> str:
    response = requests.get(
        url=OAUTH_AUTHORIZE_URL,
        auth=(LOGIN, PASSWORD),
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
        raise Exception(f"Unable to get the agenda, error {response.status_code}")

    response_data = response.json()

    if not response_data:
        raise Exception("No data in the agenda for date {start} to {end}")

    return response_data.get("result")


def create_ics(agenda: dict, start: str, end: str):
    calendar = Calendar()
    for items in agenda:
        event = Event()
        event.name = items["name"]
        event.description = items["teacher"]

        start_date = datetime.fromtimestamp(items["start_date"] / 1000.0)
        end_date = datetime.fromtimestamp(items["end_date"] / 1000.0)

        event.begin = start_date
        event.end = end_date

        if items["rooms"]:
            room = items["rooms"][0]
            event.location = f"{room['name']}, {room['campus']}"

        calendar.events.add(event)

    with open(f"ges_calendar_from_{start}_to_{end}.ics", "w") as f:
        f.writelines(calendar)


def parse_arguments() -> argparse.Namespace:
    default_start_date = datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    next_month = datetime.now().replace(day=28) + timedelta(days=4)
    default_end_date = next_month - timedelta(days=next_month.day)

    default_start_date = default_start_date.strftime("%Y-%m-%d")
    default_end_date = default_end_date.strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", type=str, default=default_start_date)
    parser.add_argument("--end-date", type=str, default=default_end_date)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    access_token = get_access_token()
    agenda = get_agenda(access_token, args.start_date, args.end_date)
    create_ics(agenda, args.start_date, args.end_date)
