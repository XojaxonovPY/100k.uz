from django.db.models import Q
from django.shortcuts import render
from django.views import View
from apps.models import Product, Stream


class SearchHomeView(View):
    def post(self, request):
        name = request.POST.get('search')
        products = Product.objects.filter(Q(name__icontains=name)).all()
        return render(request, 'searching/home_search.html', context={'products': products})

class SearchMarketView(View):
    def post(self, request):
        name = request.POST.get('name')
        products = Product.objects.filter(Q(name__icontains=name) | Q(seller__name__icontains=name)).all()
        return render(request, 'profile/market.html', context={'products': products})


class SearchStatisticView(View):
    def post(self, request):
        name = request.POST.get('search')
        stream = Stream.objects.filter(Q(name__icontains=name)).all()
        return render(request, 'profile/statistic.html', context={'streams': stream})