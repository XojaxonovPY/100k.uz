from django.urls import path

from apps.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('send-email/', SendEmailForm.as_view(), name='send_email'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]