from django.shortcuts import render
from rest_framework import viewsets
from .serializer import BookSerializer
from .models import Book
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from Permissions.permission import IsEmployee
from Permissions.permission import IsStudentOrReadOnly
from Permissions.permission import IsSuperUser
from rest_framework.response import Response
from Permissions.permission import IsRelatedEmployeeOrReadOnly
class BookViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication,]
    queryset = Book.objects.all()
    serializer_class=BookSerializer
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSuperUser|IsRelatedEmployeeOrReadOnly]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated, IsEmployee|IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)