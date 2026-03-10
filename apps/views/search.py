from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import FormView

from apps.forms import SearchForm
from apps.models import Product, Stream


class SearchHomeFormView(FormView):
    form_class = SearchForm
    template_name = 'base/100k.uz.html'

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        products = Product.objects.filter(Q(name__icontains=name)).all()
        return render(self.request, 'searching/home_search.html', context={'products': products})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class SearchMarketFormView(FormView):
    form_class = SearchForm
    template_name = 'profile/market.html'

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        products = Product.objects.filter(Q(name__icontains=name)).all()
        return render(self.request, 'profile/market.html', context={'products': products})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class SearchStatisticFormView(FormView):
    form_class = SearchForm
    template_name = 'profile/statistic.html'

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        stream = Stream.objects.filter(Q(name__icontains=name)).all()
        return render(self.request, 'profile/statistic.html', context={'streams': stream})

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)
