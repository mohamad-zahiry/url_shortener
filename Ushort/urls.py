from django.urls import path
from Ushort import views

appname = "Ushort"

urlpatterns = [
    path("", views.home, name="home")
]
