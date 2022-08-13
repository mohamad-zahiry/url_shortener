from django.urls import path

from authentication.views import CustomLoginView, CustomLogoutView, SignupView

app_name = "authentication"

urlpatterns = [
    path("login/", view=CustomLoginView.as_view(), name="login"),
    path("logout/", view=CustomLogoutView.as_view(), name="logout"),
    path("signup/", view=SignupView.as_view(), name="signup"),
]
