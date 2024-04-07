from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from .views import PasswordChangeAPI

urlpatterns = [
    path("register/",views.UserRegistrationView.as_view(),name="user_reg"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.SignOutView.as_view(), name="logout"),
    path("forgot-password/", views.PasswordResetRequestAPI.as_view(), name="forgot-password"),
    path("forgot-password-mobile/", views.PasswordResetRequestMobileAPI.as_view(), name="forgot-password-mobile"),

    path("forgot-password-mobile/", views.PasswordResetRequestMobileAPI.as_view(), name="forgot-password-mobile"),
    path('user-details/',views.UserRetrieveUpdateAPIView.as_view(),name='user-details'),
    path('password-change/<str:uid>/<str:token>/', PasswordChangeAPI.as_view(), name='password_change_api'),
 

    
]
