from braces.views import LoginRequiredMixin, UserPassesTestMixin, AnonymousRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import (CreateView, DeleteView, FormView,
                                  ListView, RedirectView, UpdateView, TemplateView)

from .models import Task


class LoginView(AnonymousRequiredMixin, FormView):
    """
    Handles authentication of User. Can only be accessed by user's who
    have not logged in.
    """
    template_name = 'todo/inc/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy(settings.AUTHENTICATED_REDIRECT_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.success_url


class LogoutView(RedirectView):
    """
    Simple view to handle User logout.
    """
    url = reverse_lazy(settings.AUTHENTICATED_REDIRECT_URL)

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    """
    Lists all the tasks and can only be accessed by logging in.
    """
    template_name = 'todo/inc/index.html'
    model = Task
    login_url = reverse_lazy(settings.LOGIN_URL)
    paginate_by = 5
    ordering = '-created'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Displays Task creation form which can only access by logged in user
    and displays success message on creation.
    """
    model = Task
    template_name = 'todo/inc/task_create.html'
    login_url = reverse_lazy(settings.LOGIN_URL)
    fields = ('name', 'description')
    success_url = reverse_lazy('todo:task-list', False)
    success_message = 'Successfully created task!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows Task deletion which can only be done by the author of the task.

    Implications:
        User has to be logged in.
    """
    template_name = 'todo/inc/task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('todo:task-list')
    login_url = reverse_lazy(settings.LOGIN_URL)
    redirect_unauthenticated_users = reverse_lazy('todo:task-list')

    def test_func(self, user):
        return self.get_object().user == user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Successfully deleted: %s!' % self.get_object().name)
        return super().delete(request, *args, **kwargs)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Allows the author to update a task.

    Implications:
        User has to be logged in.
    """
    template_name = 'todo/inc/task_update.html'
    model = Task
    raise_exception = True
    fields = ('name', 'description', 'status',)
    success_url = reverse_lazy('todo:task-list')
    success_message = 'Successfully updated task!'
    redirect_unauthenticated_users = reverse_lazy('todo:task-list')

    def test_func(self, user):
        return self.get_object().user == user


class APITestView(TemplateView):
    template_name = 'todo/inc/api.html'
