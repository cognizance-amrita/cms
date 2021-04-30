from django.shortcuts import render
from .models import Member, Domain, Task, Application, DomainMember

def home(request):
    members_count = Member.objects.count
    domains_count = Domain.objects.count
    tasks_count = Task.objects.count
    applications_count = Application.objects.count
    data = {
        'members_count': members_count,
        'domains_count': domains_count, 
        'tasks_count': tasks_count, 
        'applications_count': applications_count
    }
    return render(request, 'panel/index.html', data)

def applications(request):
    return render(request, 'panel/applications.html')

def members(request):
    members = Member.objects.all()
    domain_member = DomainMember.objects.all()
    data = {
        'members': members
    }
    return render(request, 'panel/members.html', data)

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
    domains = Domain.objects.all()
    data = {
        'domains': domains
    }
    return render(request, 'panel/domains.html', data)


