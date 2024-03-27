from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from .models import Category
from .serializer import CategorySerializer
from Permissions.permission import IsEmployee
from rest_framework.permissions import IsAuthenticated
from Permissions.permission import IsStudentOrReadOnly
from Permissions.permission import IsSuperUser
from Permissions.permission import IsRelatedEmployeeOrReadOnly
from Employee.models import Employee
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = []

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSuperUser]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsSuperUser]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated,IsEmployee|IsStudentOrReadOnly|IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
