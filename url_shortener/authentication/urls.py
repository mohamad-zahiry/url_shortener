from django.urls import path

from authentication.views import (
    CustomLoginView,
    CustomLogoutView,
    SignupView,
    ProfileView,
)

app_name = "authentication"

urlpatterns = [
    path("login/", view=CustomLoginView.as_view(), name="login"),
    path("logout/", view=CustomLogoutView.as_view(), name="logout"),
    path("signup/", view=SignupView.as_view(), name="signup"),
    path("profile/", view=ProfileView.as_view(), name="profile"),
]
