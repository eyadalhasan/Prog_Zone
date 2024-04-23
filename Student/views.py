from django.shortcuts import render

# Create your views here.

from rest_framework import serializers
from rest_framework.views import APIView
from .serializer import StudentSerializer
from rest_framework import status
from rest_framework .response import Response
class StudentRegisteration(APIView):
    permission_classes = ()
    authentication_classes = ()
    def post(self, request, format=None):
        data=request.data
        serializer=StudentSerializer(data=data)
        if  serializer.is_valid():
            serializer.save()
        if not serializer.is_valid():
            print(serializer.errors)  # Output errors to console for debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)