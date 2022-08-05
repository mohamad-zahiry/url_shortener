from django.urls import path
from shortener.views import ShortenedUrlCreateView


app_name = "shortener"

urlpatterns = [
    path("create/", view=ShortenedUrlCreateView.as_view(), name="create"),
]
