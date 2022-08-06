from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404

from shortener.models import ShortenedUrl


class UrlRedirectView(RedirectView):
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(ShortenedUrl, key=kwargs["key"]).url
        return url
