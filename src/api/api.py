from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

import todo.models as todo_models
from .serializers import TaskSerializer


class UserTaskListAPIHandler(generics.ListAPIView):
    """ Handles all API functionality for listing all tasks for a given user. """
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return todo_models.User.objects.get(id=self.kwargs['id']).task_set
