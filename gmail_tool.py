import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Permissions we need to send emails
# SCOPES = [
#    'https://www.googleapis.com/auth/gmail.readonly',
#    'https://www.googleapis.com/auth/gmail.send',
# ]

# Draft Permissions and calendar permissions
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events',
]

def get_gmail_service():
    """Connect to Gmail API — handles auth automatically."""
    creds = None

    # Load saved token if exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid token, log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next time
        with open('token.json', 'w') as f:
            f.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def read_emails(max_results=5):
    """Read latest emails from inbox."""
    service = get_gmail_service()

    results = service.users().messages().list(
        userId='me',
        maxResults=max_results,
        labelIds=['INBOX']
    ).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        # Get full message details
        message = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='full'
        ).execute()

        headers = message['payload']['headers']

        # Extract subject, from, date
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
        sender  = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date    = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

        # Extract body
        body = ''
        payload = message['payload']
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
        elif 'body' in payload:
            data = payload['body'].get('data', '')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8')

        emails.append({
            'id': msg['id'],
            'subject': subject,
            'from': sender,
            'date': date,
            'body': body[:500]  # first 500 chars
        })

    return emails

def create_draft(to: str, subject: str, body: str):
    """Create a draft email instead of sending directly."""

    # Clean the email address — remove any name prefix like "John <john@email.com>"
    import re
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', to)
    if match:
        to = match.group(0)  # extract just the email address

    service = get_gmail_service()
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft = service.users().drafts().create(
        userId='me',
        body={'message': {'raw': raw}}
    ).execute()

    return f"✅ Draft created for {to} with subject '{subject}'. Draft ID: {draft['id']}"

def send_email(to: str, subject: str, body: str):
    """Send an email."""
    service = get_gmail_service()

    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

    return f"Email sent to {to} with subject '{subject}'"