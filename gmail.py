import os
import base64
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
from email.utils import parsedate_to_datetime
from datetime import datetime
import time

# If modifying the script, change this to your desired scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail(secret_file):
    """Authenticate with Google API using OAuth 2.0"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds, _ = google.auth.load_credentials_from_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                secret_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def list_messages(service, user_id='me', maxResults= 5):
    """List all email messages in the inbox."""
    try:
        # Call the Gmail API to fetch the list of email messages
        results = service.users().messages().list(userId=user_id, maxResults= maxResults).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return []
        print('Messages:')
        parse_msgs = []
        for message in messages:  # Fetch the first 5 messages
            msg = service.users().messages().get(userId=user_id, id=message['id'],format='full' ).execute()
            parse_msg = parse_email_msg(msg)
            parse_msg['msg_id'] = message['id']
            parse_msgs.append(parse_msg)
        return parse_msgs
    except HttpError as error:
        print(f'An error occurred: {error}')


def create_service(creds):
    service = build('gmail', 'v1', credentials=creds)
    return service

def parse_email_msg(email_data):
    headers = email_data['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), None)
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'unknown')
    recipients = next((h['value'] for h in headers if h['name'] == 'To'), 'unknown')
    date = next((h['value'] for h in headers if h['name'] == 'Date'), None)

    # Initialize variables
    body = ''
    attachments = []
    attachment_count = 0

    # Process email parts
    if 'parts' in email_data['payload']:
        for part in email_data['payload']['parts']:
            # Get email body (prefer text/plain over html)
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif part['mimeType'] == 'text/html' and 'data' in part['body'] and not body:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')

            # Handle attachments
            if part.get('filename') and part['body'].get('attachmentId'):
                attachment_count += 1
                attachments.append({
                    'file_name': part['filename'],
                    'file_type': part['mimeType'],
                    'file_size': part['body'].get('size', 0),
                    'attachment_data': part['body'].get('data'),
                    'attachment_id': part['body'].get('attachmentId')
                })
    else:
        # Simple email without parts
        if email_data['payload']['mimeType'] == 'text/plain' and 'data' in email_data['payload']['body']:
            body = base64.urlsafe_b64decode(email_data['payload']['body']['data']).decode('utf-8')
        elif email_data['payload']['mimeType'] == 'text/html' and 'data' in email_data['payload']['body']:
            body = base64.urlsafe_b64decode(email_data['payload']['body']['data']).decode('utf-8')

    # Parse sender and recipient (simplified version)
    sender_email = re.search(r'<(.+?)>', sender).group(1) if '<' in sender else sender
    recipient_email = re.search(r'<(.+?)>', recipients).group(1) if '<' in recipients else recipients

    # Convert email date to MySQL datetime format
    try:
        received_datetime = parsedate_to_datetime(date) if date else datetime.now()
    except:
        received_datetime = datetime.now()

    return {
        'msg_id': id,
        'sender': sender_email,
        'recipient': recipient_email,
        'subject': subject,
        'body': body,
        'timestamp': received_datetime,
        'attachment_count': attachment_count,
        'attachments': attachments
    }

