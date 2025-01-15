from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('tasks/', views.tasks, name='tasks'),
    path('mail/', views.mail, name='mail'),
]
