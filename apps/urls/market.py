from django.urls import path

from apps.views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('explore/<int:pk>', CategoryDetailView.as_view(), name='explore'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('office', OfficeListView.as_view(), name='office'),
    path('comminicate/', CommunicationTemplateView.as_view(), name='communicate'),
    path('explore', ExploreListView.as_view(), name='category'),
]

urlpatterns += [
    path('order/', OrderView.as_view(), name='order')
]



