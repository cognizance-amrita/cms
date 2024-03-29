from django.http.response import HttpResponse
from cms.settings.base import DISCORD_CHANNEL, DISCORD_GUILD, DISCORD_TOKEN
from django.shortcuts import render, redirect
from .models import Member, Domain, Task, Application, DomainMember, Role, Position
from panel.utils.discord import Discord
from django.contrib.auth.models import User
from notifications.email import SendMail
from django.template.loader import render_to_string
from .decorators import unAuthenticated_user
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
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

@login_required(login_url='login')
def applications(request):
    return render(request, 'panel/applications.html')

@login_required(login_url='login')
def members(request):
    members = Member.objects.all()
    domain_member = DomainMember.objects.all()
    data = {
        'members': members
    }
    return render(request, 'panel/members.html', data)

@login_required(login_url='login')
def view_member(request, id):

    if request.method == 'POST':
        role = request.POST.get('role')
        selected_positions = request.POST.getlist('position []')
        revoke = str(request.POST['revoke'])
        reason = request.POST.get('revoke-reason')

        if revoke == 'Yes' and reason == '':
            print('No reason provided')
        elif revoke == 'Yes' and reason != '':
            html_message = render_to_string('panel/messages/revoke.html', {'reason': reason})
            member = Member.objects.get(github_username=id)  
            fullname = member.first_name + ' ' + member.last_name 
            SendMail(
                subject='Cognizance Membership',
                name=fullname,
                message=html_message,
                recipient=[member.email]
            )
            Member.objects.filter(github_username=id).delete()
            return redirect('members')
        else:
            member = Member.objects.get(github_username=id)
            member.role = Role.objects.get(name=role)
            member.positions.clear()
            for p in selected_positions:
                member.positions.add(Position.objects.get(name=p))
            return redirect('members')
    member = Member.objects.get(github_username=id)
    user_id = User.objects.get(email=member.email).id
    domain_member = DomainMember.objects.get(member=member)
    domains = [domain.name for domain in domain_member.domain.all()]
    domains = ', '.join(domains)
    roles = Role.objects.all()
    current_positions = [position.name for position in member.positions.all()]
    current_positions = ', '.join(current_positions)
    current_role = member.role
    positions = Position.objects.all()

    return render(request, 'panel/view-member.html', {'member':member, 'domains':domains, 
    'roles':roles, 'current_positions': current_positions, 'current_role': current_role, 
    'positions': positions, 'user_id':user_id})

@login_required(login_url='login')
def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'panel/tasks.html', {'tasks': tasks})

@login_required(login_url='login')
def achievements(request):
    return render(request, 'panel/achievements.html')

@login_required(login_url='login')
def announcements(request):
    if request.method == 'POST':
        notifications = request.POST.getlist('notifications []')
        if 'Discord' in  notifications:
            message = request.POST.get('message')
            obj = []
            obj.append(DISCORD_TOKEN) #Token
            obj.append(DISCORD_GUILD) #Guild
            obj.append(DISCORD_CHANNEL) #Channel
            client = Discord(obj=obj, message=message)
            client.sendMessage()
            print('Notification sent')
        if 'Email' in notifications:
            message = request.POST.get('message')
            user = request.user
            member = Member.objects.get(email=user.email) 
            SendMail(
                subject='Announcement',
                name=member.first_name,
                message=message,
                recipient=['cognizance-club@googlegroups.com']
            )
    return render(request, 'panel/announcements.html')

@login_required(login_url='login')
def events(request):
    return render(request, 'panel/events.html')

@unAuthenticated_user
def loginApp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            return render(request, 'panel/login.html', {'message': 'Invalid credentials'})
    return render(request, 'panel/login.html')

@login_required(login_url='login')
def profile(request, id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        github_username = request.POST.get('github_username')
        academic_year = request.POST.get('academic_year')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        discord_id = request.POST.get('discord_id')
        domains = request.POST.getlist('domains []')
        user = User.objects.get(id=id)
        member = Member.objects.get(email=user.email)
        dm = DomainMember.objects.get(member=member)
        dm.domain.clear()
        for d in domains:
            dm.domain.add(Domain.objects.get(name=str(d)))
        member.first_name = first_name
        member.last_name = last_name
        member.github_username = github_username
        member.academic_year = academic_year
        member.username = username
        member.phone = phone_number
        member.discord_id = discord_id
        Member.objects.filter(email=user.email).update(first_name=first_name, last_name=last_name,academic_year=academic_year,github_username=github_username,phone=phone_number,discord_id=discord_id,email=email)
        return redirect('home')
    elif request.user.is_staff:
        user = User.objects.get(id=id)
        member = Member.objects.get(email=user.email)
        current_username = user.username
        domains = Domain.objects.all()
        return render(request, 'panel/profile.html', {'member':member, 'username':current_username, 'domains': domains})
    else:
        return HttpResponse('<h1>You are not permitted to do this operation. Please contact the administrator for support.</h1>')

@login_required(login_url='login')
def domains(request):
    domains = Domain.objects.all()
    data = {
        'domains': domains
    }
    return render(request, 'panel/domains.html', data)

def logoutApp(request):
    logout(request)
    return redirect(loginApp)