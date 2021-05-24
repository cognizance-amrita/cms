from cms.settings.base import DISCORD_CHANNEL, DISCORD_GUILD, DISCORD_TOKEN
from django.shortcuts import render, redirect
from .models import Member, Domain, Task, Application, DomainMember, Role, Position
from panel.utils.discord import Discord

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

def view_member(request, id):

    if request.method == 'POST':
        role = request.POST.get('role')
        selected_positions = request.POST.getlist('position []')
        revoke = str(request.POST['revoke'])
        reason = request.POST.get('revoke-reason')

        if revoke == 'Yes' and reason == '':
            print('No reason provided')
        elif revoke == 'Yes' and reason != '':
            Member.objects.filter(github_username=id).delete()
            return redirect('members')
        else:
            member = Member.objects.get(github_username=id)
            member.role = Role.objects.get(name=role)
            for p in selected_positions:
                member.positions.add(Position.objects.get(name=p))
            return redirect('members')
    member = Member.objects.get(github_username=id)
    domain_member = DomainMember.objects.get(member=member)
    domains = [domain.name for domain in domain_member.domain.all()]
    domains = ', '.join(domains)
    roles = Role.objects.all()
    current_positions = [position.name for position in member.positions.all()]
    current_positions = ', '.join(current_positions)
    current_role = member.role
    positions = Position.objects.all()

    return render(request, 'panel/view-member.html', {'member':member, 'domains':domains, 
    'roles':roles, 'current_positions': current_positions, 'current_role': current_role, 'positions': positions})

def tasks(request):
    return render(request, 'panel/tasks.html')

def achievements(request):
    return render(request, 'panel/achievements.html')

def announcements(request):
    if request.method == 'POST':
        notifications = request.POST.getlist('notifications []')
        message = request.POST.get('message')
        obj = []
        obj.append(DISCORD_TOKEN) #Token
        obj.append(DISCORD_GUILD) #Guild
        obj.append(DISCORD_CHANNEL) #Channel
        client = Discord(obj=obj, message=message)
        client.sendMessage()
        print('Notification sent')
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


