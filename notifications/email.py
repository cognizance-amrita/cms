from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import global_settings

def SendMail(subject='Cognizance', name='User', message='This is sample message', recipient=[None]):
    # Email notification
    html_message = render_to_string('notifications/email_template.html', {'name': name, 'message':message})
    plain_message = strip_tags(html_message)
    from_email = global_settings.EMAIL_HOST_USER
    to = recipient
    mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)