import requests

from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from main import utils
from main.models import Site, Statistic


class ListStatisticView(LoginRequiredMixin, generic.ListView):
    model = Statistic
    fields = "__all__"
    template_name = "vpn_service/statistic_list.html"
    context_object_name = "statistics"

    def get_queryset(self):
        return Statistic.objects.filter(user=self.request.user)


class CreateSiteProxyView(LoginRequiredMixin, generic.CreateView):
    model = Site
    fields = "__all__"
    success_url = reverse_lazy("main:home")
    template_name = "vpn_service/site_form_create.html"


class UpdateSiteProxyView(LoginRequiredMixin, generic.UpdateView):
    model = Site
    fields = "__all__"
    success_url = reverse_lazy("main:home")
    template_name = "vpn_service/site_form_update.html"


class DeleteSiteProxyView(LoginRequiredMixin, generic.DeleteView):
    model = Site
    fields = "__all__"
    success_url = reverse_lazy("main:home")
    template_name = "vpn_service/site_delete.html"


class HomeView(LoginRequiredMixin, generic.ListView):
    template_name = 'vpn_service/home.html'
    context_object_name = 'sites'
    model = Site
    paginate_by = 15

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)


@login_required
def proxy_view(request, proxy_name, proxy_url):
    try:
        proxy = Site.objects.get(name=proxy_name)
    except Site.DoesNotExist:
        return HttpResponse("Not find", status=404)

    response = requests.get(proxy_url)

    bytes_sent = len(request.body) if request.body else 0
    bytes_received = len(response.content)

    soup = BeautifulSoup(response.content, 'html.parser')

    utils.get_css(soup, proxy_url)
    utils.get_scripts(soup, proxy_url)
    utils.reformat_href(soup, proxy)

    utils.update_statistic(request, proxy, bytes_sent, bytes_received, page_views=1)

    return HttpResponse(str(soup), content_type=response.headers["content-type"])
