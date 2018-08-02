from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

from . import api

app_name = 'api'

router = DefaultRouter()

urlpatterns = [

    # Singular Paths
    path('', include(router.urls), name='index'),
    path('get/auth/token/', rest_framework_views.obtain_auth_token, name='get-auth-token'),

    # Task Paths
    path('user/<int:id>/tasks/', api.UserTaskListAPIHandler.as_view(), name='tasks-by-user'),
    path('task/<int:id>/delete/', api.TaskDeleteAPIHandler.as_view(), name='task-delete'),
    path('task/create/', api.TaskCreateAPIHandler.as_view(), name='task-create'),

]
