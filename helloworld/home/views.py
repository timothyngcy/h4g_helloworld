from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, 'home/base.html')

def schedule(request):
    return render(request, 'home/schedule.html')

def tasks(request):
    return render(request, 'home/tasks.html')

def mail(request):
    return render(request, 'home/mail.html')