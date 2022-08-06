from django.urls import path
from shortener.views import ShortenedUrlCreateView, ShortenedUrlDetailView


app_name = "shortener"

urlpatterns = [
    path("create/", view=ShortenedUrlCreateView.as_view(), name="create"),
    path("detail/<str:key>/", view=ShortenedUrlDetailView.as_view(), name="url_detail"),
]
