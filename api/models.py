from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

class IntegerRangeField(models.IntegerField):
    
    def __init__(self, verbose_name = None, name = None, min_value = None, max_value = None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Task(models.Model):
    title = models.CharField(max_length = 30)
    description = models.CharField(max_length = 60)
    priority = IntegerRangeField(min_value = 1, max_value = 3, default = 1)
    state = IntegerRangeField(min_value = 1, max_value = 4, default = 1)
    creation_date = models.DateField(default = datetime.date.today)
    completion_date = models.DateField(null = True, blank = True)
    assignee = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True, default = None, related_name = 'assignee')
    creator = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True, default = None, related_name = 'creator')

    def time_since_its_creation(self):
        currentDay = datetime.date.today()
        passedTime = currentDay - self.creation_date
        return str(passedTime.days) + ' ' + 'days.'
        