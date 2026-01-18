"""
Google Calendar API integration
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GoogleCalendarClient:
    """Google Calendar API client for scheduling reminders"""

    def __init__(self, credentials_path: str):
        self.credentials = Credentials.from_authorized_user_file(credentials_path)
        self.service = build("calendar", "v3", credentials=self.credentials)

    def create_reminder(
        self,
        title: str,
        description: str,
        start_time: datetime,
        duration_minutes: int = 15,
    ) -> Dict[str, Any]:
        """Create a calendar reminder"""

        end_time = start_time + timedelta(minutes=duration_minutes)

        event = {
            "summary": title,
            "description": description,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "UTC",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        event = self.service.events().insert(calendarId="primary", body=event).execute()
        return event

    def list_upcoming_events(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """List upcoming calendar events"""

        now = datetime.utcnow().isoformat() + "Z"

        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return events_result.get("items", [])
