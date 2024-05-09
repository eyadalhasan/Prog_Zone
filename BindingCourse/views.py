# # Signals/views.py
# from rest_framework import viewsets
# from .models import BindingCourse
# from .serializer import BindingCourseSerializer
# from Permissions.permission  import IsEmployee
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from Permissions.permission import IsEmployee
# from Permissions.permission import IsStudentOrReadOnly
# from Permissions.permission import IsSuperUser
# from Permissions.permission import IsRelatedEmployeeOrReadOnly
# from Employee.models import Employee
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework import status

# from django.contrib.auth.models import User

# class BindingCourseViewSet(viewsets.ModelViewSet):
#     queryset = BindingCourse.objects.all()
#     serializer_class = BindingCourseSerializer
#     permission_classes=[IsAuthenticated]
#     authentication_classes=[TokenAuthentication]
    
#     # def get_permissions(self):
#     #     """
#     #     Instantiates and returns the list of permissions that this view requires.
#     #     """
#     #     if self.action in ['update', 'partial_update', 'destroy']:
#     #         permission_classes = [IsAuthenticated, IsEmployee | IsSuperUser, IsRelatedEmployeeOrReadOnly]
#     #     elif self.action in ['create','update', 'partial_update', 'destroy']:
#     #         permission_classes = [IsAuthenticated, IsEmployee, IsSuperUser]
#     #     elif self.action in ['retrieve', 'list']:
#     #         permission_classes = [IsAuthenticated, IsStudentOrReadOnly | IsEmployee | IsSuperUser]
#     #     else:
#     #         permission_classes = [IsAuthenticated]
#     #     return [permission() for permission in permission_classes]
    
#     def perform_create(self, serializer):
#         user = self.request.user
#         obj = Employee.objects.get(user__id=user.id)
#         serializer.save(created_by=obj)
        
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if 'approved' in request.data and not request.user.is_superuser:
#             return Response({"error": "You do not have permission to update the 'approved' field."}, status=status.HTTP_403_FORBIDDEN)
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def partial_update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if 'approved' in request.data and not request.user.is_superuser:
#             return Response({"error": "You do not have permission to update the 'approved' field."}, status=status.HTTP_403_FORBIDDEN)
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
    



from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import BindingPostCourseSerializer
from .models import BindingCourse, Employee, Video
from .serializer import BindingCourseSerializer
from Permissions.permission import (
    IsEmployee, IsStudentOrReadOnly, IsSuperUser, IsRelatedEmployeeOrReadOnly
)

class BindingCourseViewSet(viewsets.ModelViewSet):
    queryset = BindingCourse.objects.all()
    serializer_class = BindingCourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         permission_classes = [IsAuthenticated, IsEmployee | IsSuperUser, IsRelatedEmployeeOrReadOnly]
    #     elif self.action in ['create']:
    #         permission_classes = [IsAuthenticated, IsEmployee | IsSuperUser]
    #     elif self.action in ['retrieve', 'list']:
    #         permission_classes = [IsAuthenticated, IsStudentOrReadOnly | IsEmployee | IsSuperUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        user = self.request.user
        try:
            employee = Employee.objects.get(user=user)
            course = serializer.save(created_by=employee)

            # Handle video files and titles
            videos_files = self.request.FILES.getlist('file')
            titles = self.request.data.getlist('titles')  # Assuming titles are sent as a list of text

            for video_file, title in zip(videos_files, titles):
                video = Video.objects.create(file=video_file, title=title)  # Assuming your Video model has a 'title' field
                course.videos.add(video)

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'approved' in request.data and not request.user.is_superuser:
            return Response({"error": "You do not have permission to update the 'approved' field."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def get_serializer_class(self):
        if(self.request.method=='GET'):

            return BindingCourseSerializer
        else:
            print(self.request.method)
            return BindingPostCourseSerializer
            
