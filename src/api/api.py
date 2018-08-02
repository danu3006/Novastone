from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

import todo.models as todo_models
from .serializers import TaskSerializer


class UserTaskListAPIHandler(generics.ListAPIView):
    """ Handles all API functionality for listing all tasks for a given user. """
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = todo_models.User.objects.get(id=self.kwargs['id'])
        return todo_models.Task.objects.filter(user=user)


class TaskDeleteAPIHandler(generics.DestroyAPIView):
    """ Handles all API functionality for deleting tasks. """
    queryset = todo_models.Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)


class TaskCreateAPIHandler(generics.CreateAPIView):
    """ Handles all API functionality for creating tasks. """
    queryset = todo_models.Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
