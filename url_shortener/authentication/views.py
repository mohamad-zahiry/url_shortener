from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("shortener:create")
