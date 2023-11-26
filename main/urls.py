from django.urls import path

from main import views

app_name = "main"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("sites/create/", views.CreateSiteProxyView.as_view(), name="create-site"),
    path("sites/update/<int:pk>", views.UpdateSiteProxyView.as_view(), name="update-site"),
    path("sites/delete/<int:pk>", views.DeleteSiteProxyView.as_view(), name="delete-site"),
    path("statistics/", views.ListStatisticView.as_view(), name="statistic"),
    path("<str:proxy_name>/<path:proxy_url>", views.proxy_view, name="proxy"),
]
