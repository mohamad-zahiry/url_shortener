from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
from ipware import get_client_ip

from shortener.models import ShortenedUrl
from redirection.utils.url_data import increase_visits_or_create
from redirection.models import Country


class UrlRedirectView(RedirectView):
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        country = Country.from_ip(get_client_ip(self.request)[0])
        obj = get_object_or_404(ShortenedUrl, key=kwargs["key"])
        increase_visits_or_create(key=obj, country=country)
        return obj.url
