from django.urls import path

from apps.views import *

urlpatterns = [
    path('main/', MainTemplateView.as_view(), name='main'),
    path('news/', NewsTemplateView.as_view(), name='news'),
    path('market/', MarketListView.as_view(), name='market'),
    path('requests/', RequestsListView.as_view(), name='request'),
    path('statistics', StatisticTemplateView.as_view(), name='statistic'),
    path('stream/', StreamListView.as_view(), name='stream'),
    path('balance/', BalanceListView.as_view(), name='balance'),
    path('penalty/', PenaltyListView.as_view(), name='penalty'),
    path('donatbox/', DonatListView.as_view(), name='donat'),
    path('payment', PaymentCreatView.as_view(), name='payment'),
    path('chart/', chart_view, name='chart')
]

urlpatterns += [
    path('stream/save', StreamView.as_view(), name='stream-save'),
    path('oqim/<int:pk>', StreamDetailView.as_view(), name='thread'),
    path('delete/stream/<int:pk>', StreamDeleteView.as_view(), name='delete-stream'),
]
