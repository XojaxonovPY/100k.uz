from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpRequest
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView

from apps.forms import UserModelForm, PasswordForm, PhoneNumberForm
from apps.models import User, Region, District


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    pass


class BaseTemplateView(LoginRequiredMixin, TemplateView):
    pass


class AccountUpdateView(BaseUpdateView):
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


class PasswordUpdateView(BaseUpdateView):
    queryset = User.objects.all()
    form_class = PasswordForm
    template_name = 'settings/password.html'
    success_url = reverse_lazy('login')
    pk_url_kwarg = 'pk'

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class PhoneNumberUpdateView(BaseUpdateView):
    queryset = User.objects.all()
    template_name = 'settings/phone_number.html'
    form_class = PhoneNumberForm
    success_url = reverse_lazy('main')
    pk_url_kwarg = 'pk'


class TelegramTemplateView(BaseTemplateView):
    template_name = 'settings/telegram.html'


class FacebookTemplateView(BaseTemplateView):
    template_name = 'settings/facebook.html'


def district_list(request: HttpRequest) -> JsonResponse:
    region_id = request.GET.get("region_id")
    districts = District.objects.filter(region_id=region_id)
    data = [{"id": i.pk, "name": i.name} for i in districts]
    return JsonResponse(data, safe=False)
