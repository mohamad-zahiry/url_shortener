from django.urls import path
from Ushort import views

app_name = "Ushort"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("panel/", views.panel, name="panel"),
]
