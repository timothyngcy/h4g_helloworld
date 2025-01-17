import os
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from googleapiclient.discovery import build
import datetime
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Create your views here.
def home(request):
    return render(request, 'home/base.html')

def schedule(request):
    return render(request, 'home/schedule.html')

def tasks(request):
    return render(request, 'home/tasks.html')

def mail(request):
    return render(request, 'home/mail.html')

# Redirect to Google OAuth
def google_auth(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/gmail.send"],
        redirect_uri="https://127.0.0.1:8000/oauth2callback",
    )
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

# Callback to handle OAuth response
def oauth2callback(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/gmail.send"],
        redirect_uri="https://127.0.0.1:8000/oauth2callback",
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
    }
    return redirect('schedule')

def find_meeting_time(request):
    if request.method == "POST":
        if 'credentials' not in request.session:
            return redirect('google_auth')

        credentials = Credentials(**request.session['credentials'])

        # form data
        meeting_name = request.POST['meeting_name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        duration = float(request.POST['duration'])
        emails = request.POST.getlist('emails[]')

        # convert time to SGT
        tz = pytz.timezone('Asia/Singapore')
        start_datetime = tz.localize(datetime.datetime.fromisoformat(f"{start_date}T{start_time}"))
        end_datetime = tz.localize(datetime.datetime.fromisoformat(f"{end_date}T{end_time}"))
        duration_delta = datetime.timedelta(hours=duration)

        # Google Calendar API
        service = build('calendar', 'v3', credentials=credentials)

        # check availability of invitees (including user's availability)
        freebusy_query = {
            "timeMin": start_datetime.isoformat(),
            "timeMax": end_datetime.isoformat(),
            "items": [{"id": "primary"}] + [{"id": email} for email in emails],
        }
        freebusy_result = service.freebusy().query(body=freebusy_query).execute()

        # add busy times to a list
        all_busy_intervals = []
        for calendar_id, calendar_data in freebusy_result['calendars'].items():
            if 'errors' in calendar_data:
                continue
            all_busy_intervals.extend([
                (datetime.datetime.fromisoformat(busy['start']),
                 datetime.datetime.fromisoformat(busy['end']))
                for busy in calendar_data.get('busy', [])
            ])
        all_busy_intervals.sort()

        # a meeting can only begin after 9am, end latest 5pm, only on weekdays
        def is_valid_time(dt):
            return 9 <= dt.hour < 17 and dt.weekday() < 5

        # find the first available time slot
        current_time = max(start_datetime, tz.localize(datetime.datetime.combine(start_datetime.date(), datetime.time(9, 0))))
        available_slot = None

        while current_time + duration_delta <= end_datetime:
            if not is_valid_time(current_time) or not is_valid_time(current_time + duration_delta):
                # move to 9am the next day if the current time is invalid
                current_time += datetime.timedelta(days=1)
                current_time = tz.localize(datetime.datetime.combine(current_time.date(), datetime.time(9, 0)))
                continue

            conflict = any(start < current_time + duration_delta and end > current_time
                           for start, end in all_busy_intervals)
            if not conflict:
                available_slot = current_time
                break

            current_time += datetime.timedelta(minutes=30)

        if not available_slot:
            return JsonResponse({"error": "No available time slots"}, status=400)

        # schedule the event
        event = {
            "summary": meeting_name,
            "start": {"dateTime": available_slot.isoformat(), "timeZone": "Asia/Singapore"},
            "end": {"dateTime": (available_slot + duration_delta).isoformat(), "timeZone": "Asia/Singapore"},
            "attendees": [{"email": email} for email in emails],
        }
        created_event = service.events().insert(calendarId='primary', body=event, sendUpdates="all").execute()

        return JsonResponse({"message": "Meeting scheduled", "event": created_event})

    return JsonResponse({"error": "Invalid request"}, status=400)

def schedule(request):
    if 'credentials' not in request.session:
        return redirect('google_auth')
    return render(request, 'home/schedule.html')