from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from shortener.models import ShortenedUrl


class keyAsSlugMixin:
    """A Mixin that use 'key' as slug-field for ShortenedUrl model"""

    model = ShortenedUrl
    slug_field = "key"
    slug_url_kwarg = "key"


class ShortenedUrlCreateView(LoginRequiredMixin, CreateView):
    model = ShortenedUrl
    fields = ("url", "active_from", "active_until")
    template_name = "shortener/shortened_url_create_view.html"


class ShortenedUrlDetailView(LoginRequiredMixin, keyAsSlugMixin, DetailView):
    template_name = "shortener/shortened_url_detail_view.html"


class ShortenedUrlUpdateView(LoginRequiredMixin, keyAsSlugMixin, UpdateView):
    template_name = "shortener/shortened_url_update_view.html"
    fields = ("active_from", "active_until")


class ShortenedUrlDeleteView(LoginRequiredMixin, keyAsSlugMixin, DeleteView):
    template_name = "shortener/shortened_url_delete_view.html"
    success_url = reverse_lazy("shortener:create")
