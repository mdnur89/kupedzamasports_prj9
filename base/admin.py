from django.contrib import admin

# Register your models here.

from .models import Team, Project, Message, User, Incident

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Message)
admin.site.register(Incident)