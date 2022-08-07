from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from shortener.models import ShortenedUrl


class ShortenedUrlCreateView(CreateView):
    model = ShortenedUrl
    fields = ("url", "active_from", "active_until")
    template_name = "shortener/shortened_url_create_view.html"


class keyAsSlugForShortenedUrlMixin:
    """A Mixin that use 'key' as slug-field for ShortenedUrl model"""

    model = ShortenedUrl
    slug_field = "key"
    slug_url_kwarg = "key"


class ShortenedUrlDetailView(keyAsSlugForShortenedUrlMixin, DetailView):
    template_name = "shortener/shortened_url_detail_view.html"


class ShortenedUrlUpdateView(keyAsSlugForShortenedUrlMixin, UpdateView):
    template_name = "shortener/shortened_url_update_view.html"
    fields = ("active_from", "active_until")


class ShortenedUrlDeleteView(keyAsSlugForShortenedUrlMixin, DeleteView):
    template_name = "shortener/shortened_url_delete_view.html"
    success_url = reverse_lazy("shortener:create")
