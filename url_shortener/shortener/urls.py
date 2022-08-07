from django.urls import path
from shortener.views import (
    ShortenedUrlCreateView,
    ShortenedUrlDetailView,
    ShortenedUrlUpdateView,
    ShortenedUrlDeleteView,
)


app_name = "shortener"

urlpatterns = [
    path("create/", view=ShortenedUrlCreateView.as_view(), name="create"),
    path("detail/<str:key>/", view=ShortenedUrlDetailView.as_view(), name="url_detail"),
    path("update/<str:key>/", view=ShortenedUrlUpdateView.as_view(), name="url_update"),
    path("delete/<str:key>/", view=ShortenedUrlDeleteView.as_view(), name="url_delete"),
]
