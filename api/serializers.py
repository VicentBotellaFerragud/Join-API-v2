from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'state', 'creation_date', 'completion_date', 'assignee', 'creator', 'time_since_its_creation',]
        