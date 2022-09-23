from django.shortcuts import render
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

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

class Login(FormView):

    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('api:task-list')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())

        else:
            return super(Login, self).dispatch(request, *args, *kwargs)

    def form_valid(self, form):

        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)

        if token:
            login(self.request, form.get_user())
            return super(Login, self).form_valid(form)

class Logout(APIView):

    def get(self, request, format = None):

        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)
