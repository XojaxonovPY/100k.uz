from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Sum
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView

from apps.forms import PaymentModelForm, StreamModelForm
from apps.mixin_views import BaseTemplateView, BaseListView
from apps.models import Payment, Transaction
from apps.models import Product, Category, Setting, Region, News, Tag, Seller, Stream, Order, Charity, Penalty


class MainTemplateView(BaseTemplateView):
    template_name = 'profile/main.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['news'] = News.objects.all()[:3]
        data['admin'] = Setting.objects.first()
        return data


class NewsTemplateView(BaseTemplateView):
    template_name = 'profile/news.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['news'] = News.objects.all()
        return data


class MarketListView(BaseListView):
    queryset = Product.objects.all()
    template_name = 'profile/market.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = super().get_queryset()

        seller = self.request.GET.get('seller')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')
        if tag:
            return query.filter(tags=tag)
        if seller and seller != 'all':
            query = query.filter(seller_id=seller)
        if category and category != 'all':
            query = query.filter(category_id=category)
        return query

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['categories'] = Category.objects.all()
        data['tags'] = Tag.objects.all()
        data['sellers'] = Seller.objects.all()
        data['admin'] = Setting.objects.get()
        return data


class StreamListView(BaseListView):
    queryset = Stream.objects.all()
    context_object_name = 'streams'
    template_name = 'profile/stream.html'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user=self.request.user)
        return query


class StatisticTemplateView(BaseListView):
    queryset = Stream.objects.all()
    template_name = 'profile/statistic.html'
    context_object_name = 'streams'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user=self.request.user.pk).select_related('product').annotate(
            new_count=Count('orders', filter=Q(orders__status=Order.StatusType.NEW)),
            redy_count=Count('orders', filter=Q(orders__status=Order.StatusType.REDY_TO_DELIVER)),
            delivering_count=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERING)),
            delivered_count=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERED)),
            come_count=Count('orders', filter=Q(orders__status=Order.StatusType.COME_BACK)),
            archive_count=Count('orders', filter=Q(orders__status=Order.StatusType.ARCHIVE)),
            hold_count=Count('orders', filter=Q(orders__status=Order.StatusType.HOLD)),
        ).values(
            'name',
            'new_count',
            'redy_count',
            'delivering_count',
            'delivered_count',
            'come_count',
            'archive_count',
            'hold_count',
            'created_at',
            'visit_count',
            'product__seller_price'
        )
        return query

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['delivered'] = Order.StatusType.DELIVERED
        return data


class PenaltyListView(BaseListView):
    queryset = Penalty.objects.all()
    template_name = 'profile/penalty.html'
    context_object_name = 'penalties'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(stream__user=self.request.user)
        return query


class DonatListView(BaseListView):
    queryset = Charity.objects.all()
    template_name = 'profile/donat.html'
    context_object_name = 'donations'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['total_amount'] = Charity.objects.aggregate(total=Sum('amount')).get('total', 0)
        data['admin'] = Setting.objects.get()
        return data


class PaymentCreatView(LoginRequiredMixin, CreateView):
    queryset = Payment.objects.all()
    template_name = 'profile/payment.html'
    success_url = reverse_lazy('payment')
    form_class = PaymentModelForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        payment = Payment.objects.filter(user=self.request.user).order_by('-created_at')
        data['payments'] = payment
        data['amount'] = payment.order_by('-created_at').first().amount if payment else 0

        return data

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        Transaction.objects.create(type='-', amount=amount, message='Pul yechildi', user=self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class RequestsListView(BaseListView):
    queryset = Order.objects.all()
    context_object_name = 'requests'
    template_name = 'profile/requests.html'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(stream__user=self.request.user)
        return query

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data['status'] = Order.StatusType.values
        return data


class BalanceListView(BaseListView):
    queryset = Transaction.objects.all()
    template_name = 'profile/balance.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user=self.request.user)
        status = self.request.GET.get('status')
        if status:
            query = query.filter(status=status)
        return query


def chart_view(request: HttpRequest):
    orders = Order.objects.filter(owner=request.user).order_by('region')
    labels = list(orders.values_list('region__name', flat=True))
    data = list(orders.values_list('region__order_count', flat=True))
    return render(request, 'profile/diagram.html', {
        'labels': labels,
        'data': data
    })


# ============================================== Stream

class StreamCreateView(CreateView):
    model = Stream
    form_class = StreamModelForm
    template_name = 'profile/market.html'
    success_url = reverse_lazy('stream')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


class StreamDeleteView(DeleteView):
    model = Stream
    success_url = reverse_lazy('stream')
    template_name = 'profile/stream.html'
    pk_url_kwarg = 'pk'


class StreamDetailView(DetailView):
    queryset = Stream.objects.all()
    context_object_name = 'thread'
    template_name = 'market/detail.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        stream = self.get_object(self.queryset)
        stream.visit_count += 1
        stream.save()
        product = self.get_object(self.queryset).product
        product.visit_count += 1
        product.save()
        data['product'] = product
        data['regions'] = Region.objects.all()
        data['admin'] = Setting.objects.first()
        return data
