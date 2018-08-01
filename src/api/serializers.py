from django.contrib.auth.models import User
from rest_framework import serializers

from todo.models import Task


class UserSerializer(serializers.ModelSerializer):
    """ Serializes the User model """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class TaskSerializer(serializers.ModelSerializer):
    """ Serializes the Task model """
    user = UserSerializer()

    class Meta:
        model = Task
        fields = ('id', 'created', 'name', 'description', 'status', 'user', 'done_by')
