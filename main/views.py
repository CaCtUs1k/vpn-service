from urllib.parse import urlparse, urlunparse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from main.forms import UserRegistrationForm
from main.models import Site, Statistic


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


@login_required
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


class CreateSiteProxyView(LoginRequiredMixin, generic.CreateView):
    model = Site
    fields = "__all__"
    success_url = reverse_lazy("main:home")
    template_name = "vpn_service/site_form.html"
