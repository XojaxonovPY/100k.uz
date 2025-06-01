import random
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from redis import Redis
from DjangoMarket.settings import EMAIL_HOST_USER
from apps.forms import LoginForm, EmailForm
from apps.models import User
from apps.tasks import send_email


class SendEmailForm(FormView):
    form_class = EmailForm
    template_name = 'login-register/send_code.html'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        code = random.randrange(10 ** 5, 10 ** 6)
        redis = Redis()
        redis.set(email, code)
        send_email.delay(
            subject="Verification Code !!!",
            message=f"{code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        redis.expire(email, time=timedelta(2))
        return render(self.request, 'login-register/register.html', context={'email': email})

    def form_invalid(self, form):
        for i in form.errors:
            messages.error(self.request, i)
        return super().form_invalid(form)


class RegisterView(View):
    def post(self, request):
        email = request.POST.get('email')
        code = request.POST.get('code')
        query = User.objects.filter(email=email)
        if query.exists():
            user = query.first()
            login(request, user)
            return redirect('main')
        redis = Redis(decode_responses=True)
        check_code = redis.get(email)
        if not check_code or str(check_code) != str(code):
            messages.error(request, 'Kod hatto!')
        users = User.objects.create_user(email=email)
        login(request, users)
        return redirect('main')


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'login-register/login.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for i in form.errors:
            messages.error(self.request, i)
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')