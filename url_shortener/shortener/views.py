from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from shortener.models import ShortenedUrl


class ShortenedUrlCreateView(CreateView):
    model = ShortenedUrl
    fields = ("url", "active_from", "active_until")
    template_name = "shortener/shortened_url_create_view.html"


class ShortenedUrlDetailView(DetailView):
    model = ShortenedUrl
    template_name = "shortener/shortened_url_detail_view.html"
    slug_field = "key"
    slug_url_kwarg = "key"


class ShortenedUrlUpdateView(UpdateView):
    model = ShortenedUrl
    template_name = "shortener/shortened_url_update_view.html"
    fields = ("active_from", "active_until")
    slug_field = "key"
    slug_url_kwarg = "key"
