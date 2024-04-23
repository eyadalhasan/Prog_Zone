from django.shortcuts import render
from rest_framework import viewsets
from .models import Course
from .serializer import CourseSerializer
from Permissions.permission  import IsEmployee
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from Permissions.permission import IsEmployee
from Permissions.permission import IsStudentOrReadOnly
from Permissions.permission import IsSuperUser
from Permissions.permission import IsRelatedEmployeeOrReadOnly
from Employee.models import Employee
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes=[]
    authentication_classes=[TokenAuthentication]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            
            permission_classes = [IsAuthenticated, IsEmployee |IsSuperUser,IsRelatedEmployeeOrReadOnly]
        elif self.action in ['create']:
        # Only allow certain users (e.g., employees) to create courses
            permission_classes = [IsAuthenticated, IsEmployee,IsSuperUser]
    
        elif self.action  in ['retrive',"list"]:
            permission_classes = [IsAuthenticated, IsStudentOrReadOnly | IsEmployee|IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    

    def perform_create(self, serializer):
        user=self.request.user
        print(user.id)
        
        obj=Employee.objects.get(user__id=user.id)
        serializer.save(created_by=obj)
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'])
    def by_category(self, request,pk=None):
        """
        Retrieve courses by category.
        """
        print(pk)
        category_id =pk
        if category_id is None:
            return Response({"error": "Please provide a category_id parameter."}, status=status.HTTP_400_BAD_REQUEST)
        
        courses = Course.objects.filter(category_id=category_id)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'])
    def search_filter(self, request,pk=None):
        """
        Retrieve courses by category.
        """
        print(pk)
        category_id =pk
        if category_id is None:
            return Response({"error": "Please provide a category_id parameter."}, status=status.HTTP_400_BAD_REQUEST)
        
        courses = Course.objects.filter(category_id=category_id)        
        """
        Apply search filters to the queryset based on query parameters.

        """
        search_by = request.query_params.get('searchBy', None)
        search_query = request.query_params.get('searchQuery', None)
        
        if search_by and search_query:
            if search_by == 'title':
                queryset = courses.filter(title__icontains=search_query)
            if search_by == 'description':
                queryset = courses.filter(description__icontains=search_query)
            if search_by == 'created_by':
                queryset = Course.objects.filter(
            created_by__user__username__icontains=search_query
            )
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


