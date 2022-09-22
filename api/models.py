from django.conf import settings
from django.db import models
import datetime

# Create your models here.

class Task(models.Model):

    priority_choices = [('Low', 'Low'), ('Medium', 'Medium'), ('Urgent', 'Urgent')]
    state_choices = [('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Awaiting Feedback', 'Awaiting Feedback'), ('Done', 'Done')]

    title = models.CharField(max_length = 30)
    description = models.CharField(max_length = 60)
    priority = models.CharField(max_length = 6, choices = priority_choices, default = 'Low')
    state = models.CharField(max_length = 17, choices = state_choices, default = 'To Do')
    creation_date = models.DateField(default = datetime.date.today)
    completion_date = models.DateField(null = True, blank = True)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'assignee')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'creator')

    def time_since_its_creation(self):
        currentDay = datetime.date.today()
        passedTime = currentDay - self.creation_date
        return str(passedTime.days) + ' ' + 'days.'

    def __str__(self):
        return self.title
        