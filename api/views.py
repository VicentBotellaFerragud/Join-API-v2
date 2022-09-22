from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from django.core import serializers

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer
    permission_classes = [] # permissions.IsAuthenticated

    def create(self, request):

        data = {
            'title': request.data.get('title'), 
            'description': request.data.get('description'), 
            'priority': request.data.get('priority'), 
            'state': request.data.get('state'), 
            'creation_date': request.data.get('creation_date'), 
            'completion_date': request.data.get('completion_date'), 
            'assignee': request.data.get('assignee'), 
            'creator': request.data.get('creator')
        }

        serializer = TaskSerializer(data = data)

        if serializer.is_valid():
            serializer.save() 

        return Response(serializer.data)
