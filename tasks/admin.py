from django.contrib import admin
from .models import Task,Chat,Message

admin.site.register(Task)
admin.site.register(Chat)
admin.site.register(Message)