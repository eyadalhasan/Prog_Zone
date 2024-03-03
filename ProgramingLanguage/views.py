from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializer import ProgramingLanguageSerializer
from .models import ProgrammingLanguage
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from Permissions.permission import IsSuperUser
from rest_framework.response import Response


class ProgramingLanguageViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = ProgramingLanguageSerializer
    queryset = ProgrammingLanguage.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def get_permissions(self):

            if self.action in ['create', 'update', 'partial_update']:
                # For create, update, and partial_update actions, require IsAuthenticated and IsSuperUser
                permission_classes = [IsAuthenticated, IsSuperUser]
            else:
                permission_classes = [IsAuthenticated]
            return [permission() for permission in permission_classes]
    
    
    
    
        
        
        
    