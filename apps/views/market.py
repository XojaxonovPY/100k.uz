from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView

from apps.models import Product, Category, Settings, Region, Order, Attribute


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
        data['orders'] = Product.objects.filter(order_count__gt=0)[:8]
        data['settings'] = Settings.objects.first()

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
        products=self.get_object(self.queryset)
        products.visit_count+=1
        products.save()
        data['attribute'] = Attribute.objects.filter(products=self.get_object(self.queryset)).all()
        data['regions'] = Region.objects.all()
        data['admin'] = Settings.objects.first()
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
        data['communications'] = Settings.objects.all()
        return data


class AboutTemplateView(TemplateView):
    template_name = 'market/about.html'


# =======================================================Order
class OrderView(View):
    def post(self, request):
        order = {
            'name': request.POST.get('name'),
            'product_id': request.POST.get('product_id'),
            'phone_number': request.POST.get('phone_number'),
            'region_id': request.POST.get('region'),
            'owner_id': request.POST.get('owner'),
            'stream_id': request.POST.get('thread'),
        }
        admin = Settings.objects.first()
        products = Product.objects.all()[:16]
        product = Product.objects.filter(pk=order['product_id']).first()
        order['total'] = float(product.discount_price) + float(admin.delivery_price)
        Order.objects.create(**order)
        context = {'order': order, 'products': products, 'product_item': product, 'admin': admin}
        return render(request, 'market/order.html', context=context)



