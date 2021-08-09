from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('members/', members, name='members'),
    path('view-member/<str:id>/', view_member, name='view-member'),
    path('login/', loginApp, name='login'),
    path('logout/', logoutApp, name='logout'),
    path('achievements/', achievements, name='achievements'),
    path('applications/', applications, name='applications'),
    path('announcements/', announcements, name='announcements'),
    path('tasks/', tasks, name='tasks'),
    path('profile/<str:id>/', profile, name='profile'),
    path('events/', events, name='events'),
    path('domains/', domains, name='domains'),
         path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="panel/password_reset.html"),
        name="reset_password"),   
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="panel/password_reset_sent.html"), 
        name="password_reset_done"),   
    path('reset_password/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(template_name="panel/password_reset_confirm.html"), 
        name="password_reset_confirm"),   
    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="panel/password_reset_done.html"), 
        name="password_reset_complete")
]
