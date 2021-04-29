from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('members/', members, name='members'),
    path('login/', login, name='login'),
    path('achievements/', achievements, name='achievements'),
    path('applications/', applications, name='applications'),
    path('announcements/', announcements, name='announcements'),
    path('tasks/', tasks, name='tasks'),
    path('profile/', profile, name='profile'),
    path('events/', events, name='events'),
    path('domains/', domains, name='domains'),
    
]
