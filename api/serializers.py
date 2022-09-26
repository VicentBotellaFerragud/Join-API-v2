from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import password_validation, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(write_only = True, required = True)
    password = serializers.CharField(write_only = True, required = True)

    def validate(self, attrs):

        user = authenticate(username = attrs["username"], password = attrs["password"])

        if not user:
            raise serializers.ValidationError('User credentials not valid.')

        self.context["user"] = user

        return attrs

    def create(self, data):
        
        token, created = Token.objects.get_or_create(user = self.context['user'])

        return self.context['user'], token.key

class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(min_length = 4, max_length = 20, validators = [UniqueValidator(queryset = User.objects.all())])
    password = serializers.CharField(min_length = 8, max_length = 64)
    password_confirmation = serializers.CharField(min_length = 8, max_length = 64)

    def validate(self, attrs):

        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError("Passwords didn't match.")

        password_validation.validate_password(attrs['password'])

        return attrs

    def create(self, data):

        data.pop('password_confirmation')
        user = User.objects.create_user(**data)

        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username",]

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'state', 'creation_date', 'completion_date', 'assignee', 'creator', 'time_since_its_creation',]
        