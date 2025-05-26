from django.urls import path

from apps.views import *

urlpatterns = [
    path('search/home', SearchHomeView.as_view(), name='search-home'),
    path('search/market', SearchMarketView.as_view(), name='search'),
    path('search/statistic', SearchStatisticView.as_view(), name='search-statistic')
]
