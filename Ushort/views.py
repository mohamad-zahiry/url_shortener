import email
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from django.contrib.auth import login, logout

from Ushort.forms import CreatorSignUpForm
from Ushort.models import Creator


def home(request):
    return render(request, "Ushort/home.html", {})


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("Ushort:home")  # ! fix: redirect to "user panel"

    form = CreatorSignUpForm(request.POST or None)
    if form.is_valid():
        form.save()

        user = Creator.objects.get(email=form.cleaned_data.get("email")).user
        login(request, user)

        return redirect("Ushort:home")  # ! fix: redirect to "user panel"

    context = {"form": form}
    return render(request, "Ushort/signup.html", context)


def log_out(request):
    logout(request)
    return redirect("Ushort:home")
