from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("shortener:create")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("authentication:login")


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "authentication/signup_view.html"
