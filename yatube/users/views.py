from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class ChangePassword(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/change_password-form.html'


class PasswordReset(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/password_reset_form.html'
