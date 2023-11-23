from django.urls import path

from main import views
from main.views import proxy_view

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("sites/create/", views.CreateSiteProxyView.as_view(), name="create-site"),
]
