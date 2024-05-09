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
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

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
        print(username)
        print(password)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            if user.is_active:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                user_type=""
                if user.is_student():
                    user_type="student"
                elif user.is_employee():
                    user_type="employee"
                elif user.is_superuser:
                    user_type="admin"
                print(user_type)   

                return Response({"token": str(token),"role":user_type}, status=status.HTTP_200_OK)
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
    
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PasswordResetRequestMobileAPI(APIView):
    permission_classes = ()
    authentication_classes = ()
    
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email address is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        form = PasswordResetForm(data={'email': email})
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
                'email_template_name': 'user-confirm-mobile.html',
                'extra_email_context': {
                    'protocol': 'yourapp',
                    'domain': 'reset-password'
                },
                'request': request,
            }
            form.save(**opts)
            return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
# urls.py


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                # Optionally log the user in after resetting the password
                login(request, user)
                # Redirect to password reset complete page
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'reset_password_form.html', {'form': form})

    else:
        # Invalid link
        return render(request, 'reset_password_link_invalid.html')

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class UserRetrieveUpdateAPIView(APIView):
    # Apply the authentication and permissions as needed
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # You can retrieve the user from the session or use a URL parameter
        user = request.user
        # If you want to retrieve a user by a parameter, like their id, you would use:
        # user_id = kwargs.get('pk') or kwargs.get('user_id')
        # user = User.objects.get(pk=user_id)
    

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user = request.user
        # For partial updates, use 'partial=True'

    
        serializer = UserSerializer(user, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk', None)
        if not user_id:
            # Assuming you do not want to allow deleting the current authenticated user
            return Response({"error": "Cannot delete current user without specific user ID."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, pk=user_id)
        # Additional checks can be added to prevent unauthorized deletion
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)        

        


    

# In your Django views.py
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class PasswordChangeAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, uid, token, *args, **kwargs):
     
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')
        print(request.data)
       

        try:
            uid = urlsafe_base64_decode(uid).decode()
            
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            
            form = SetPasswordForm(user, request.data)

            if form.is_valid():
                form.save()
                
                return Response({"success": "Password has been reset with the new password."}, status=status.HTTP_200_OK)
            else:
                
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "The reset link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)
