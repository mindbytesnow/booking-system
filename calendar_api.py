from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def create_event(data):

    creds = service_account.Credentials.from_service_account_file(
        "credentials.json",
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    service = build("calendar", "v3", credentials=creds)

    start = datetime.strptime(f"{data['date']} {data['time']}", "%Y-%m-%d %H:%M")
    end = start + timedelta(hours=1)

    event = {
        "summary": f"{data['service']} - {data['name']}",
        "description": data["email"],
        "start": {"dateTime": start.isoformat(), "timeZone": "Pacific/Auckland"},
        "end": {"dateTime": end.isoformat(), "timeZone": "Pacific/Auckland"}
    }

    service.events().insert(calendarId="primary", body=event).execute()
