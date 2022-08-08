from django.urls import path

from authentication.views import CustomLoginView

app_name = "authentication"

urlpatterns = [
    path("login/", view=CustomLoginView.as_view(), name="login"),
]
