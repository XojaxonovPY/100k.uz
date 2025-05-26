from django.urls import path

from apps.views import *

urlpatterns = [
    path('account/<int:pk>', AccountUpdateView.as_view(), name='account'),
    path('password/<int:pk>', PasswordUpdateView.as_view(), name='password'),
    path('phone-number/<int:pk>', PhoneNumberUpdateView.as_view(), name='number'),
    path('telegram/', TelegramTemplateView.as_view(), name='telegram'),
    path('facbook/', FacebookTemplateView.as_view(), name='facebook'),
    path("district/list", district_list, name='district_list'),
]


urlpatterns += [
    path('order/', OrderView.as_view(), name='order'),]