from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .serializer import EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
class EmployeeRegestrationView(APIView):
    permission_classes = ()
    authentication_classes = ()
   
    def post(self, request, format=None):
        data=request.data
        serializer=EmployeeSerializer(data=data)
        if  serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    