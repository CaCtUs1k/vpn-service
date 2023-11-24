from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/<int:pk>", views.AccountView.as_view(), name="profile"),
]