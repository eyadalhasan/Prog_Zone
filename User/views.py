from django.shortcuts import render
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
class UserRegistrationView(APIView):
    permission_classes = ()
    authentication_classes = ()
    def post(self, request, format=None):
        data=request.data
        
        serializer=UserSerializer(data=data)
        if  serializer.is_valid():
            user=serializer.save()
            user.set_password(request.data["password"])
            user.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        # Get the username and password from the request
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            if user.is_active:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": str(token)}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Account is not active"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"message": "Invalid login credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class SignOutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the user's token
        user_token = request.auth

 
        if user_token:
            # Delete the user's token
            user_token.delete()
            
            # logout(request.user)

            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "No authentication token provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    

class PasswordResetRequestAPI(APIView):
    
    permission_classes=()
    authentication_classes=()
    def post(self, request, *args, **kwargs):
        email = request.data.get("email","not-found")
        form = PasswordResetForm(data=request.data)

        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
                'email_template_name': 'user-confirm.html',
                'request': request,
            }
            form.save(**opts)
            return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

