import os
from django.shortcuts import redirect, render
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
from datetime import datetime, timedelta

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

def get_credentials():
    # Load credentials from the token.pickle file if it exists
    try:
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    except FileNotFoundError:
        credentials = None

    # If the credentials are invalid or missing, initiate OAuth
    if not credentials or credentials.expired or credentials.refresh_token is None:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credentials = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return credentials

def google_calendar_auth(request):
    # Step 1: Redirect the user to Google's OAuth page
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    flow.redirect_uri = 'http://127.0.0.1:8000/oauth2callback/'
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

def oauth2callback(request):
    # Step 2: Handle Google's OAuth response
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    flow.redirect_uri = 'http://127.0.0.1:8000/oauth2callback/'

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # Save credentials for later use
    credentials = flow.credentials
    with open('token.pickle', 'wb') as token:
        pickle.dump(credentials, token)

    return redirect('home')  # Redirect to your app's home page

def get_free_busy(request):
    # Use get_credentials() instead of directly loading from the pickle file
    credentials = get_credentials()  

    service = build('calendar', 'v3', credentials=credentials)

    # Define the date range and emails
    emails = ['person1@example.com', 'person2@example.com']
    time_min = datetime.utcnow().isoformat() + 'Z'  # Current time in UTC
    time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'  # 7 days later

    body = {
        "timeMin": time_min,
        "timeMax": time_max,
        "items": [{"id": email} for email in emails]
    }

    # Fetch free/busy information
    freebusy_result = service.freebusy().query(body=body).execute()

    busy_times = {}
    for email, calendar in freebusy_result['calendars'].items():
        busy_times[email] = calendar['busy']

    return busy_times

def find_common_free_time(busy_times, start_time, end_time):
    busy_intervals = []
    
    for intervals in busy_times.values():
        for interval in intervals:
            busy_intervals.append((datetime.fromisoformat(interval['start']), datetime.fromisoformat(interval['end'])))
    
    busy_intervals.sort(key=lambda x: x[0])  # Sort by start time

    merged_intervals = []
    for start, end in busy_intervals:
        if not merged_intervals or merged_intervals[-1][1] < start:
            merged_intervals.append([start, end])
        else:
            merged_intervals[-1][1] = max(merged_intervals[-1][1], end)

    # Find free slots
    free_slots = []
    current_time = start_time
    for start, end in merged_intervals:
        if current_time < start:
            free_slots.append((current_time, start))
        current_time = max(current_time, end)
    
    if current_time < end_time:
        free_slots.append((current_time, end_time))

    return free_slots

def find_meeting_time(request):
    if request.method == 'POST':
        # Extract form data
        meeting_name = request.POST.get('meeting_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Convert to datetime objects (handling time properly)
        try:
            start_datetime = datetime.strptime(start_date + ' ' + start_time, '%Y-%m-%d %H:%M')
            end_datetime = datetime.strptime(end_date + ' ' + end_time, '%Y-%m-%d %H:%M')
        except ValueError as e:
            # Handle parsing error gracefully
            return render(request, 'home/schedule.html', {'error': 'Invalid date or time format.'})

        # Get busy times
        try:
            busy_times = get_free_busy(request)
        except Exception as e:
            return render(request, 'home/schedule.html', {'error': 'Failed to fetch calendar data.'})

        # Find common free time slots
        free_slots = find_common_free_time(busy_times, start_datetime, end_datetime)

        return render(request, 'home/meeting_times.html', {'free_slots': free_slots})

    return render(request, 'home/schedule.html')