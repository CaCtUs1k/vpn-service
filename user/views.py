from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from user.forms import UserRegistrationForm


def account(request):
    if request.method == "GET":
        user = request.user
        return render(request, "user/account.html", context={"user": user})


class UpdateUserView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    template_name = "user/user_form.html"
    fields = ("first_name", "last_name", "email", "username")
    success_url = reverse_lazy("main:home")


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
