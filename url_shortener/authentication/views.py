from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "authentication/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        urls = self.request.user.shortenedurl_set.all()
        context["urls"] = urls
        return context

    def get_object(self, queryset=None):
        user = self.request.user
        if user.is_authenticated:
            return user
        return redirect("authentication:login")


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("authentication:login")


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "authentication/signup_view.html"
