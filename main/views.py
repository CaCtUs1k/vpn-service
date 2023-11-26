from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from main.models import Site, Statistic


class ListStatisticView(LoginRequiredMixin, generic.ListView):
    model = Statistic
    fields = "__all__"
    template_name = "vpn_service/statistic_list.html"

    def get_queryset(self):
        return Statistic.objects.filter(user=self.request.user)


class CreateSiteProxyView(LoginRequiredMixin, generic.CreateView):
    model = Site
    fields = "__all__"
    success_url = reverse_lazy("main:home")
    template_name = "vpn_service/site_form.html"


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

    soup = BeautifulSoup(response.content, 'html.parser')

    css_link = soup.find('link', {'rel': 'stylesheet'})

    if css_link:
        css_url = urljoin(proxy_url, css_link['href'])
        css_response = requests.get(css_url)

        if css_response.status_code == 200:
            css_content = css_response.text

            style_tag = soup.new_tag('style')
            style_tag.string = css_content
            soup.head.append(style_tag)
        else:
            print(f"Failed to fetch CSS. Status code: {css_response.status_code}")

    script_tags = soup.find_all('script', {'src': True})

    for script_tag in script_tags:
        script_src = script_tag['src']
        script_url = urljoin(proxy_url, script_src)

        script_response = requests.get(script_url)

        if script_response.status_code == 200:
            script_content = script_response.text
            new_script_tag = soup.new_tag('script')
            new_script_tag.string = script_content
            script_tag.replace_with(new_script_tag)
        else:
            print(f"Failed to fetch script. Status code: {script_response.status_code}")

    for a_tag in soup.find_all("a", href=True):
        if "https://" not in a_tag["href"]:
                a_tag["href"] = f"/{proxy_name}/{proxy.url}{a_tag['href']}"

    return HttpResponse(str(soup), content_type=response.headers["content-type"])
