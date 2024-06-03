
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import BindingPostCourseSerializer
from .models import BindingCourse, Employee, Video
from .serializer import BindingCourseSerializer
from Permissions.permission import (
    IsEmployee, IsStudentOrReadOnly, IsSuperUser, IsRelatedEmployeeOrReadOnly
)
from .serializer import BindingPatchCourseSerializer
class BindingCourseViewSet(viewsets.ModelViewSet):
    queryset = BindingCourse.objects.all()
    serializer_class = BindingCourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsEmployee | IsSuperUser|IsRelatedEmployeeOrReadOnly]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated, IsEmployee | IsSuperUser]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsStudentOrReadOnly | IsEmployee | IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def perform_create(self, serializer):
        user = self.request.user
        try:
            employee = Employee.objects.get(user=user)
            course = serializer.save(created_by=employee)
            videos_files = self.request.FILES.getlist('file')
            titles = self.request.data.getlist('titles')
            for video_file, title in zip(videos_files, titles):
                video = Video.objects.create(file=video_file, title=title) 
                course.videos.add(video)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not exist "}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def get_serializer_class(self):
        if(self.request.method=='GET'):
            return BindingCourseSerializer
        elif(self.request.method=="POST"):
            return BindingPostCourseSerializer
        else:
            return BindingPatchCourseSerializer

        
    
            
# pagination.py
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    # The number of items to be displayed per page
    page_size = 10
    # The query parameter used to specify the page number
    page_query_param = 'page'
    # The query parameter used to specify the page size
    page_size_query_param = 'page_size'
    # The maximum allowed page size
    max_page_size = 1000
