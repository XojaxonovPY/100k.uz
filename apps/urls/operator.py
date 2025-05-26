
from django.urls import path

from apps.views import *

urlpatterns = [
    path('operator/',OperatorTemplateView.as_view(),name='operator'),
    path('order/page/<int:pk>',OrderDetailView.as_view(),name='order-detail'),
    path('order/update/<int:pk>',OrderUpdateView.as_view(),name='order-update')
]
