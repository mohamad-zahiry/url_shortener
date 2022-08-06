from urllib.request import urlretrieve
from django.urls import path
from redirection.views import UrlRedirectView

app_name = "redirection"

urlpatterns = [
    path("<str:key>/", view=UrlRedirectView.as_view(), name="url_redirect"),
]
