from django.urls import path

from Ushort.api import views


urlpatterns = [
    path("url/add/", views.url_add, name="api_url-add"),
]
