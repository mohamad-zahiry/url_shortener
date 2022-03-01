import email
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate

from Ushort.forms import CreatorSignUpForm, CreatorLogInForm
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


def log_in(request):
    invalid_credentials = None

    if request.user.is_authenticated:
        return redirect("Ushort:home")  # ! fix: redirect to "user panel"

    form = CreatorLogInForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        username = Creator.objects.get(email=email).user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("Ushort:home")  # ! fix: redirect to "user panel"

        invalid_credentials = "Invalid credentials"

    context = {
        "form": form,
        "invalid_credentials": invalid_credentials,
    }
    return render(request, "Ushort/login.html", context)


def log_out(request):
    logout(request)
    return redirect("Ushort:home")
