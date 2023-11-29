import os
import shutil

import requests

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

    def post(self, request, *args, **kwargs):
        site = self.get_object()

        media_folder_path = os.path.join("media", site.name)
        if os.path.exists(media_folder_path):
            shutil.rmtree(media_folder_path)

        static_folder_path = os.path.join("static", site.name)
        if os.path.exists(static_folder_path):
            shutil.rmtree(static_folder_path)

        return super().post(request, *args, **kwargs)


class HomeView(LoginRequiredMixin, generic.ListView):
    template_name = "vpn_service/home.html"
    context_object_name = "sites"
    model = Site
    paginate_by = 15

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)


@login_required()
def proxy_view(request, proxy_name, proxy_url):
    try:
        proxy = Site.objects.get(name=proxy_name)
    except Site.DoesNotExist:
        return HttpResponse("Not find", status=404)

    response = requests.get(proxy_url)

    bytes_sent = len(request.body) if request.body else 0
    bytes_received = len(response.content)

    base_folder = os.path.join("media/", proxy_name)

    soup = utils.download_page_with_selenium(proxy_url, base_folder, proxy)

    utils.update_statistic(request, proxy, bytes_sent, bytes_received, page_views=1)

    return HttpResponse(str(soup), content_type=response.headers["content-type"])
