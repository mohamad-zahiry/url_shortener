from django.urls import path
from Ushort import views

app_name = "Ushort"

urlpatterns = [
    path("", views.home, name="home")
]
