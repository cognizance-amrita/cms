from django.shortcuts import render

def home(request):
    return render(request, 'panel/index.html')

def applications(request):
    return render(request, 'panel/applications.html')

def members(request):
    return render(request, 'panel/members.html')

def tasks(request):
    return render(request, 'panel/tasks.html')

def achievements(request):
    return render(request, 'panel/achievements.html')

def announcements(request):
    return render(request, 'panel/announcements.html')

def events(request):
    return render(request, 'panel/events.html')

def login(request):
    return render(request, 'panel/login.html')

def profile(request):
    return render(request, 'panel/profile.html')

def domains(request):
    return render(request, 'panel/domains.html')