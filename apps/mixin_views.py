from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, ListView


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    pass


class BaseTemplateView(LoginRequiredMixin, TemplateView):
    pass


class BaseListView(LoginRequiredMixin, ListView):
    pass
