from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.models import Site, Statistic


def home(request):
    sites = Site.objects.all()
    statistics = Statistic.objects.all()

    context = {
        "sites": sites,
        "statistics": statistics,
    }

    return render(request, "vpn_service/home.html", context)

