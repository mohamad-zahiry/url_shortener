from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView

from shortener.models import ShortenedUrl


class ShortenedUrlCreateView(CreateView):
    model = ShortenedUrl
    fields = ("url", "active_from", "active_until")
    template_name = "shortener/shortened_url_create_view.html"

    def get_success_url(self):
        return reverse("shortener:create")
