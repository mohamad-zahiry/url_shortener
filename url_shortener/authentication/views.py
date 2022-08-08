from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("shortener:create")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("authentication:login")
