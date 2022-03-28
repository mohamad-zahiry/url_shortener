from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from Ushort.forms import CreatorSignUpForm, CreatorLogInForm
from Ushort.models import Creator, Url

from random import choice


def home(request):
    return render(request, "Ushort/home.html", {})


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("Ushort:panel-dashboard")

    form = CreatorSignUpForm(request.POST or None)
    if form.is_valid():
        form.save()

        user = Creator.objects.get(email=form.cleaned_data.get("email")).user
        login(request, user)

        return redirect("Ushort:panel-dashboard")

    context = {"form": form}
    return render(request, "Ushort/signup.html", context)


def log_in(request):
    invalid_credentials = None

    if request.user.is_authenticated:
        return redirect("Ushort:panel-dashboard")

    form = CreatorLogInForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        username = Creator.objects.get(email=email).user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("Ushort:panel-dashboard")

        invalid_credentials = "Invalid credentials"

    context = {
        "form": form,
        "invalid_credentials": invalid_credentials,
    }
    return render(request, "Ushort/login.html", context)


def log_out(request):
    logout(request)
    return redirect("Ushort:home")


@login_required(login_url="Ushort:login")
def panel_dashboard(request):
    creator = Creator.by_request(request)
    context = {
        "all_visitors": creator.all_visitors,
        "simple_urls": creator.simple_urls_number,
        "monitored_urls": creator.monitored_urls_number,
        "active_urls": creator.active_urls_number,
    }
    return render(request, "Ushort/panel/dashboard.html", context)


@login_required(login_url="Ushort:login")
def panel_urls(request):
    creator = Creator.by_request(request)
    context = {
        "active_urls": creator.active_urls_number,
        "expired_urls": creator.expired_urls_number,
        "last_10_urls": creator.n_last_urls(10),
        "most": None,
        "least": None,
    }

    if Creator.account_type != Creator.Account.Types.FREE:
        urls = creator.url_set.order_by("-visitors")
        if urls.exists():
            context["most"] = {"visited_url": urls.first()}
            context["least"] = {"visited_url": urls.last()}

        m_urls = urls.filter(monitored=True)
        if m_urls.exists():
            max = m_urls.first()
            min = m_urls.last()

            context["most"].update({"visitors_country": max.most_country, "visiting_time": max.most_hour})
            context["least"].update({"visitors_country": min.least_country, "visiting_time": min.least_hour})

    return render(request, "Ushort/panel/urls.html", context)


def go2(request, url):
    url = Url.objects.get(url=url)
    url.add_visitor(request)
    return redirect(url.target)
