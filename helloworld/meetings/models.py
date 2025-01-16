from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} available on {self.date} from {self.start_time} to {self.end_time}"

class Meeting(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    duration = models.FloatField(default=0)  # in hours
    participants = models.ManyToManyField(User, related_name="meetings")

    def __str__(self):
        return f"{self.name} on {self.date} at {self.start_time}"