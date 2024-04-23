from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .serializer import EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from Employee.models import Employee
class EmployeeRegestrationView(APIView):
    permission_classes = ()
    authentication_classes = ()
   
    def post(self, request, format=None):
        data=request.data
        print(data)
        serializer=EmployeeSerializer(data=data)
        if  serializer.is_valid():
            print(serializer.errors)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        objs=Employee.objects.all()
        serilize=EmployeeSerializer(objs, many=True)
        return Response(serilize.data,status=status.HTTP_200_OK)

    




    