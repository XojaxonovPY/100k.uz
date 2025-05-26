from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView
from apps.forms import UserModelForm, PasswordForm, PhoneNumberForm
from apps.models import User, Region, District


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    form_class = UserModelForm
    template_name = 'settings/account.html'
    success_url = reverse_lazy('account')
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('account', kwargs={"pk": self.request.user.pk})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['regions'] = Region.objects.all()
        return data


class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    form_class = PasswordForm
    template_name = 'settings/password.html'
    success_url = reverse_lazy('login')
    pk_url_kwarg = 'pk'


class PhoneNumberUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    template_name = 'settings/phone_number.html'
    form_class = PhoneNumberForm
    success_url = reverse_lazy('main')
    pk_url_kwarg = 'pk'


class TelegramTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'settings/telegram.html'


class FacebookTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'settings/facebook.html'


def district_list(request):
    region_id = request.GET.get("region_id")
    districts = District.objects.filter(region_id=region_id)
    data = [{"id": i.pk, "name": i.name} for i in districts]
    return JsonResponse(data, safe=False)