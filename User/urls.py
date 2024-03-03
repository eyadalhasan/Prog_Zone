from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.UserRegistrationView.as_view(),name="user_reg"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.SignOutView.as_view(), name="logout"),
    path("reset-password/", views.PasswordResetRequestAPI.as_view(), name="reset-password"),

  
]
