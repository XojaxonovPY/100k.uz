from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from apps.forms import OrderModelForm
from apps.models import Category, Region, Order, Transaction


class OperatorTemplateView(ListView):
    queryset = Order.objects.order_by('-created_at').all()
    template_name = 'operator/operator-page.html'
    context_object_name = 'orders'


    def post(self,request):
        category=request.POST.get('category')
        region=request.POST.get('region')
        order=self.get_queryset()
        if category:
            order=order.filter(product__category_id=category)
        if region:
            order=order.filter(region_id=region)
        context={
            'status':Order.StatusType.values,
            'orders':order,
            'categories':Category.objects.all(),
            'regions':Region.objects.all(),
        }
        return render(request,'operator/operator-page.html',context=context)


    def get_queryset(self):
        query = super().get_queryset()
        status=self.request.GET.get('status')
        query=query.filter(status=status)
        return query

    def get_context_data(self, **kwargs):
        data=super().get_context_data(**kwargs)
        data['status']=Order.StatusType.values
        data['regions']=Region.objects.all()
        data['categories']=Category.objects.all()
        return data


class OrderDetailView(DetailView):
    queryset = Order.objects.all()
    template_name = 'operator/order-change.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        data=super().get_context_data(**kwargs)
        order = self.get_object(self.queryset)
        data['max_quantity'] = order.product.quantity
        data['regions']=Region.objects.all()
        return data


class OrderUpdateView(UpdateView):
    queryset = Order.objects.all()
    template_name = 'operator/order-change.html'
    success_url = reverse_lazy('operator')
    pk_url_kwarg = 'pk'
    form_class = OrderModelForm

    def form_valid(self, form):
        status=form.cleaned_data.get('status')
        obj=self.get_object(self.queryset)
        if obj.stream and status==Order.StatusType.COMPLETED:
            user=obj.stream.user
            user.balance+=(obj.product.seller_price*obj.quantity)
            user.save()
            Transaction.objects.create(type='+',amount=obj.product.seller_price*obj.quantity,message='Pul qoshildi',user=user)
            Region.objects.filter(id=obj.region.id).update(order_count=obj.quantity)
        return super().form_valid(form)




