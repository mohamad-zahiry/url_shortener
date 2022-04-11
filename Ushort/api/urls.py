from django.urls import path

from Ushort.api import views


urlpatterns = [
    path("url/add/", views.url_add, name="api_url-add"),
    path("url/list/", views.url_list_view, name="api_url-list"),
]
