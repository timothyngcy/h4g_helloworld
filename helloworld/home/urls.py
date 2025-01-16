from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('find_meeting_time/', views.find_meeting_time, name='find_meeting_time'),
    path('tasks/', views.tasks, name='tasks'),
    path('mail/', views.mail, name='mail'),
    path('google_calendar_auth/', views.google_calendar_auth, name='google_calendar_auth'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
]
