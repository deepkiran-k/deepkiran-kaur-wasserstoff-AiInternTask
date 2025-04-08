import base64
from googleapiclient.discovery import build

def create_calendar_service(creds):
    service = build('calendar', 'v3', credentials=creds)
    return service

# Function to create an event on Google Calendar
def create_calendar_event(service, summary, description, starttime, endtime, timezone, attendees):
    # Event details
    attendee_list = []
    for attendee in attendees:
        email = {}
        email['email'] = attendee
        attendee_list.append(email)

    event = {
        'summary': summary,
        'location': 'Virtual',
        'description': description,
        'start': {
            'dateTime': starttime,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': endtime,
            'timeZone': timezone,
        },
        'attendees': attendee_list,
        'reminders': {
            'useDefault': True,
        },
    }

    # Create the event
    event_result = service.events().insert(
        calendarId='primary',
        body=event
    ).execute()

    print(f'Event created: {event_result["htmlLink"]}')



