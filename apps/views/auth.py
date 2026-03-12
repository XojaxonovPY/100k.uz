import random

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from apps.forms import LoginForm, EmailForm, RegisterForm
from apps.models import User
from apps.tasks import send_email


class SendEmailForm(FormView):
    form_class = EmailForm
    template_name = 'auth/send_code.html'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        email: str = form.cleaned_data.get('email')
        code: str = str(random.randrange(10 ** 5, 10 ** 6))
        cache.set(email, code, timeout=300)
        send_email(
            message=code,
            recipient_list=[email],
        )
        send_email.delay(message=code, recipient_list=[email])
        return render(self.request, 'auth/register.html', context={'email': email, 'code': code})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class RegisterView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        code = form.cleaned_data.get('code')
        check_code = cache.get(email)
        if not check_code or str(check_code) != str(code):
            messages.error(self.request, 'Kod hatto!')
            return redirect('register')
        users = User.objects.create_user(email=email)
        login(self.request, users)
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        logout(request)
        return redirect('login')
