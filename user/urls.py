from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.account, name="profile"),
    path(
        "update/<int:pk>", views.UpdateUserView.as_view(), name="user-update"
    ),
]
