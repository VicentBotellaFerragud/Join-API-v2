from django.contrib import admin
from .models import Task

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'priority', 'state', 'creation_date', 'completion_date', 'assignee', 'creator',)    
    list_display = ('title', 'description', 'priority', 'state', 'creation_date', 'completion_date', 'assignee', 'creator',)
   
admin.site.register(Task, TaskAdmin)
