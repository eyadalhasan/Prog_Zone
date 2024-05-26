from django.shortcuts import get_object_or_404, render
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
from Video.models import Video
class CourseViewSet(viewsets.ModelViewSet):
    permission_classes=[]
    authentication_classes=[TokenAuthentication]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action in ['update', 'partial_update', 'destroy']:
            
    #         permission_classes = [IsAuthenticated, IsEmployee &IsRelatedEmployeeOrReadOnly |IsSuperUser]
    #     elif self.action in ['create']:
    #     # Only allow certain users (e.g., employees) to create courses
    #         permission_classes = [IsAuthenticated, IsEmployee,IsSuperUser]
    
    #     elif self.action  in ['retrive',"list"]:
    #         permission_classes = [IsAuthenticated, IsStudentOrReadOnly | IsEmployee|IsSuperUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Handle the custom saving logic
        user = self.request.user
        try:
            employee = Employee.objects.get(user=user)
            # Ensure the updated_by field is handled if necessary
            course = serializer.save(updated_by=employee)
            
            # Handle adding or updating videos
            videos_files = request.FILES.getlist('file', [])
            titles = request.data.getlist('titles', [])
            for video_file, title in zip(videos_files, titles):
                video_data = {'file': video_file, 'title': title}
                if video_data.get('id'):
                    video = Video.objects.get(id=video_data['id'], course=course)
                    video.file = video_data.get('file', video.file)
                    video.title = video_data.get('title', video.title)
                    video.save()
                else:
                    Video.objects.create(course=course, **video_data)

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)


    

    def perform_create(self, serializer):
        user=self.request.user
        print(user.id)
        
        obj=Employee.objects.get(user__id=user.id)
        serializer.save(created_by=obj)
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @action (detail=False,methods=['get'])
    def employeeCourses(self,request,*args,**kargs):
        employee=Employee.objects.get(user=request.user)
        courses=Course.objects.filter(created_by=employee);
        serializer=CourseSerializer(courses,many=True)
        return Response(serializer.data)
    @action (detail=True,methods=['get'])
    def get_employee_courses(self, request,pk=None):
        employee=Employee.objects.get(id=pk)
        courses=Course.objects.filter(created_by=employee);
        serializer=CourseSerializer(courses,many=True)
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
        category_id = request.query_params.get('category', None)

        
        if search_by and search_query:
            if search_by == 'title':
                queryset = courses.filter(title__icontains=search_query,category__id=category_id)
            if search_by == 'description':
                queryset = courses.filter(description__icontains=search_query,category__id=category_id)
            if search_by == 'created_by':
                queryset = Course.objects.filter(
            created_by__user__username__icontains=search_query,category_id=category_id
            )
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import StudentCourseRank
from .serializer import StudentCourseRankSerializer
from Student.models import Student

# class StudentCourseRankViewSet(viewsets.ModelViewSet):
#     queryset = StudentCourseRank.objects.all()
#     serializer_class = StudentCourseRankSerializer
#     permission_classes = [IsAuthenticated]  # Ensure only authenticated users can use this viewset
#     authentication_classes=[TokenAuthentication]
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             student = get_object_or_404(Student, user=request.user)
#             serializer.save(student=student)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def list(self, request, *args, **kwargs):
#         # Standard implementation of list action, which might include filtering logic
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)


from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count

class StudentCourseRankViewSet(viewsets.ModelViewSet):
    queryset = StudentCourseRank.objects.all()
    serializer_class = StudentCourseRankSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can use this viewset
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = get_object_or_404(Student, user=request.user)
            serializer.save(student=student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_APIRequest)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='student-count')
    def get_student_count(self, request, pk=None):
        """
        Returns the number of students who have ranked the specified course.
        """
        student_count = StudentCourseRank.objects.filter(course=pk).values('student').distinct().count()
        return Response({"student_count": student_count}, status=status.HTTP_200_OK)


