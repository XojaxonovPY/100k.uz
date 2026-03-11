from typing import Any

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView

from apps.forms import OrderForm
from apps.models import Product, Category, Setting, Region, Order, Attribute


class HomeListView(ListView):
    queryset = Product.objects.all()
    template_name = 'market/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = super().get_queryset()
        return query.order_by('-creat_at')[:8]

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['categories'] = Category.objects.all()
        data['orders'] = Product.objects.filter(order_count__gt=0).order_by('-order_count')[:8]
        data['settings'] = Setting.objects.first()
        return data


class CategoryDetailView(DetailView):
    queryset = Category.objects.all()
    template_name = 'market/explore.html'
    context_object_name = 'index_category'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        product = self.get_object(self.queryset)

        data['products'] = Product.objects.filter(category=product)
        data['categories'] = Category.objects.all()
        return data


class ExploreListView(ListView):
    queryset = Product.objects.all()
    template_name = 'market/explore.html'
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        return data


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'market/detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        products = self.get_object(self.queryset)
        products.visit_count += 1
        products.save()
        data['attribute'] = Attribute.objects.filter(products=self.get_object(self.queryset)).all()
        data['regions'] = Region.objects.all()
        data['admin'] = Setting.objects.first()
        return data


class OfficeListView(ListView):
    queryset = Product.objects.all()
    template_name = 'market/office.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = super().get_queryset()
        return query.order_by('-creat_at')[:8]


class CommunicationTemplateView(TemplateView):
    template_name = 'market/communicate.html'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        data['communications'] = Setting.objects.all()
        return data


class AboutTemplateView(TemplateView):
    template_name = 'market/about.html'


# =======================================================Order
class OrderView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        form = OrderForm(request.POST)
        admin = Setting.objects.first()
        products = Product.objects.all()[:16]
        context: dict[str, Any] = {'products': products, 'admin': admin}
        if form.is_valid():
            data = form.cleaned_data
            product = Product.objects.filter(pk=data.get('product_id')).first()
            if not product:
                messages.error(request, "Mahsulot topilmadi!")
                return render(request, 'market/order.html', context=context)
            total_price = float(product.discount_price or 0) + float(admin.delivery_price or 0)
            try:
                order = Order.objects.create(
                    name=data.get('name'),
                    product_id=product.id,
                    phone_number=data.get('phone_number'),
                    region_id=data.get('region'),
                    owner_id=data.get('owner'),
                    stream_id=data.get('thread'),
                    total=total_price
                )
                context['order'] = order
                context['product_item'] = product
                return render(request, 'market/order.html', context=context)
            except IntegrityError:
                messages.error(request, "Ma'lumotlar bazasida xatolik (duplikatsiya bo'lishi mumkin).")
            except Exception as e:
                messages.error(request, f"Kutilmagan xatolik: {str(e)}")
        else:
            messages.error(request, 'Iltimos, shaklni to\'g\'ri to\'ldiring.')
        return render(request, 'market/order.html', context=context)
