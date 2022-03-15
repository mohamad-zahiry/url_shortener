from django.urls import path
from Ushort import views

app_name = "Ushort"

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("panel/dashboard/", views.panel_dashboard, name="panel-dashboard"),
    path("go2/<str:url>/", views.go2, name="go2"),
]
