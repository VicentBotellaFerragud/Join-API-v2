from django.shortcuts import render
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('creation_date')
    serializer_class = TaskSerializer
    permission_classes = [] # permissions.IsAuthenticated
