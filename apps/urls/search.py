from django.urls import path

from apps.views import *

urlpatterns = [
    path('search/home', SearchHomeFormView.as_view(), name='search-home'),
    path('search/market', SearchMarketFormView.as_view(), name='search-market'),
    path('search/statistic', SearchStatisticFormView.as_view(), name='search-statistic')
]
