from django.contrib import admin
from .models import *

admin.site.register(Member)
admin.site.register(Domain)
admin.site.register(DomainMember)
admin.site.register(Role)
admin.site.register(Token)
admin.site.register(Position)
admin.site.register(Application)
admin.site.register(Achievement)
admin.site.register(Department)
admin.site.register(Task)
admin.site.register(Submission)