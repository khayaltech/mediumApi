from django.urls import path

from .views import loginView, registerView, verifyView

urlpatterns = [
    path("register/", registerView, name="register"),
    path("login/", loginView, name="login"),
    path("email-verify/", verifyView, name="email-verify"),
]
