from django.urls import path, include
from Ushort import views

app_name = "Ushort"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("panel/dashboard/", views.panel_dashboard, name="panel-dashboard"),
    path("panel/urls/", views.panel_urls, name="panel-urls"),
    path("go2/<str:url>/", views.go2, name="go2"),
    path("api/", include("Ushort.api.urls")),
]
