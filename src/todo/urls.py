from django.urls import path

from . import views

app_name = 'todo'

urlpatterns = [

    # Singular Paths
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Task URLS
    path('', views.TaskListView.as_view(), name='task-list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),

]
