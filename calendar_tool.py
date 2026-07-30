# calendar_tool.py
import os
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events',
]

def get_calendar_service():
    """Connect to Google Calendar API."""
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(days=7, max_results=10):
    """Get upcoming events for the next N days."""
    service = get_calendar_service()

    now = datetime.utcnow()
    future = now + timedelta(days=days)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now.isoformat() + 'Z',
        timeMax=future.isoformat() + 'Z',
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        return []

    result = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        result.append({
            'id': event['id'],
            'title': event.get('summary', 'No title'),
            'start': start,
            'end': end,
            'location': event.get('location', ''),
            'description': event.get('description', ''),
            'attendees': [
                a['email'] for a in event.get('attendees', [])
            ],
        })

    return result


def create_event(title: str, date: str, start_time: str, end_time: str, description: str = '', attendees: list = []):
    """Create a calendar event.
    
    Args:
        title: Event title
        date: Date in YYYY-MM-DD format
        start_time: Start time in HH:MM format (24hr)
        end_time: End time in HH:MM format (24hr)
        description: Optional event description
        attendees: Optional list of email addresses
    """
    service = get_calendar_service()

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': f'{date}T{start_time}:00',
            'timeZone': 'America/Los_Angeles',  # change to your timezone
        },
        'end': {
            'dateTime': f'{date}T{end_time}:00',
            'timeZone': 'America/Los_Angeles',
        },
    }

    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]

    created = service.events().insert(
        calendarId='primary',
        body=event,
        sendUpdates='none'  # don't email attendees yet
    ).execute()

    return f"✅ Event '{title}' created on {date} from {start_time} to {end_time}. Event ID: {created['id']}"