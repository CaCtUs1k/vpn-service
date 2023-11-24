from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from main.forms import UserRegistrationForm
from main.models import Site, Statistic


class CreateSiteProxyView(LoginRequiredMixin, generic.CreateView):
    model = Site
    fields = "__all__"
    success_url = reverse_lazy("main:home")
    template_name = "vpn_service/site_form.html"


class AccountView(LoginRequiredMixin, generic.DetailView):
    model = User
    fields = ("username", "email", "first_name", "last_name")
    template_name = "vpn_service/account.html"


@login_required
def home(request):
    user = request.user
    sites = Site.objects.filter(user=user)
    statistics = Statistic.objects.filter(user=user)

    context = {
        "sites": sites,
        "statistics": statistics,
    }

    return render(request, "vpn_service/home.html", context)


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(
                request,
                "registration/register_done.html",
                {"new_user": new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request, "registration/register.html", {"user_form": user_form}
    )


@login_required
def proxy_view(request, proxy_name, proxy_url):
    try:
        proxy = Site.objects.get(name=proxy_name)
    except Site.DoesNotExist:
        return HttpResponse("Not find", status=404)

    response = requests.get(proxy_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Получаем ссылку на CSS-файл
    css_link = soup.find('link', {'rel': 'stylesheet'})

    if css_link:
        css_url = urljoin(proxy_url, css_link['href'])  # Склеиваем базовый URL с относительным путем
        css_response = requests.get(css_url)

        if css_response.status_code == 200:
            css_content = css_response.text

            # Добавляем CSS-содержимое к HTML-супу
            style_tag = soup.new_tag('style')
            style_tag.string = css_content
            soup.head.append(style_tag)
        else:
            print(f"Failed to fetch CSS. Status code: {css_response.status_code}")

    script_tags = soup.find_all('script', {'src': True})

    for script_tag in script_tags:
        script_src = script_tag['src']
        script_url = urljoin(proxy_url, script_src)  # Склеиваем базовый URL с относительным путем

        script_response = requests.get(script_url)

        if script_response.status_code == 200:
            script_content = script_response.text

            # Создаем новый тег <script> и добавляем его содержимое
            new_script_tag = soup.new_tag('script')
            new_script_tag.string = script_content
            script_tag.replace_with(new_script_tag)
        else:
            print(f"Failed to fetch script. Status code: {script_response.status_code}")

    # Обновляем ссылки на странице
    for a_tag in soup.find_all("a", href=True):
        a_tag["href"] = f"/{proxy_name}/{proxy.url}{a_tag['href']}"

    return HttpResponse(str(soup), content_type=response.headers["content-type"])
