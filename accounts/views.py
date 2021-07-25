from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView, LoginView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from .forms import RegisterForm, CustomPasswordChangeForm, EmailForm, NewPasswordForm, UserLoginForm


class UserCreateView(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'registration/register_form.html'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return redirect(reverse('profiles:profile_details', kwargs={'pk': user.pk}))
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    authentication_form = UserLoginForm


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/custom_password_change_form.html'

    def get_success_url(self):
        user = self.request.user
        success_url = reverse_lazy('profiles:profile_details', kwargs={'pk': user.pk})
        return success_url


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('accounts:password_reset_done')
    form_class = EmailForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = NewPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
