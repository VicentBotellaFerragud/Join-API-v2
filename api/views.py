from django.shortcuts import render
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

# Create your views here.

class UserViewSet(viewsets.GenericViewSet):

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    @action(detail = False, methods = ['post'])
    def login(self, request):

        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user, token = serializer.save()
        
        data = {
            'user': UserSerializer(user).data,
            'access_token': token
        }

        return Response(data, status = status.HTTP_201_CREATED)

    @action(detail = False, methods = ['post'])
    def register(self, request):

        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        data = UserSerializer(user).data

        return Response(data, status = status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):

        queryset = User.objects.all().order_by('id')
        serializer = UserSerializer(queryset, many = True)

        return Response(serializer.data)

    def retrieve(self, request, pk = None):

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk = pk)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        
        user_to_delete = self.get_object()
        user_to_delete.delete()

        return Response('User deleted')

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def create(self, request):

        data = {
            'title': request.data.get('title'), 
            'description': request.data.get('description'), 
            'priority': request.data.get('priority'), 
            'state': request.data.get('state'), 
            'creation_date': request.data.get('creation_date'), 
            'completion_date': request.data.get('completion_date'), 
            'assignee': request.data.get('assignee') if request.data.get('assignee') else '', 
            'creator': request.data.get('creator') if request.data.get('creator') else ''
        }

        serializer = TaskSerializer(data = data)

        if serializer.is_valid():
            serializer.save()

        else: 
            return Response(serializer.errors)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):

        task_to_edit = self.get_object()
        
        data = {
            'title': request.data.get('title'), 
            'description': request.data.get('description'), 
            'priority': request.data.get('priority'), 
            'state': request.data.get('state'), 
            'creation_date': request.data.get('creation_date'), 
            'completion_date': request.data.get('completion_date'), 
            'assignee': request.data.get('assignee') if request.data.get('assignee') else '', 
            'creator': request.data.get('creator') if request.data.get('creator') else ''
        }

        serializer = TaskSerializer(instance = task_to_edit, data = data)

        if serializer.is_valid():
            serializer.save()

        else: 
            return Response(serializer.errors)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        
        task_to_delete = self.get_object()
        task_to_delete.delete()

        return Response('Task deleted')

"""
    DON'T DELETE IT YET PLEASE

    def list(self, request, *args, **kwargs):

        header_token = request.headers['Authorization']
        token = header_token[6:]
        user = Token.objects.get(key = token).user
        print(user)
        queryset = User.objects.filter(username = user.username).order_by('id')
        serializer = UserSerializer(queryset, many = True)
        return Response(serializer.data)
"""
