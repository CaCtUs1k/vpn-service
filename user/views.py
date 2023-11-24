from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from user.forms import UserRegistrationForm
from vpn_service import settings


class AccountView(LoginRequiredMixin, generic.DetailView):
    model = settings.AUTH_USER_MODEL
    fields = ("username", "email", "first_name", "last_name")
    template_name = "vpn_service/../templates/user/account.html"


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