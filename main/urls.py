from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("sites/create/", views.CreateSiteProxyView.as_view(), name="create-site"),
    path("<str:proxy_name>/<path:proxy_url>", views.proxy_view, name="proxy"),
]
