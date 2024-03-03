from django.shortcuts import render

from rest_framework import viewsets
from .serializer import SummarySerializer
from .models import Summary
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class SummaryViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes=[IsAuthenticated]
    serializer_class=SummarySerializer
    queryset=Summary.objects.all()
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def by_language(self,request):
        language_name = request.query_params.get('language', None)
        print(language_name)
        if language_name is not None:
            queryset = self.queryset.filter(language__name=language_name)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Language parameter is required"}, status=400)


    
    

    
