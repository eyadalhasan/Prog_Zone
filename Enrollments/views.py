from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Enrollments
from .serializer import EnrollmentsSerializer
from Permissions.permission import IsEmployee,IsSuperUser,IsRelatedEmployeeOrReadOnly,IsStudentOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from Permissions.permission import IsRelatedUserOrReadOnly
from rest_framework.response import Response
from Student.models import Student
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.decorators import action
from Permissions.permission import IsStudent

# class EnrollmentsViewset(ModelViewSet):
#     authentication_classes = [TokenAuthentication]
#     queryset = Enrollments.objects.all()
#     serializer_class = EnrollmentsSerializer
#     # http_method_names = ['post', 'get']

#     def get_permissions(self):
  
#         if self.action == 'retrieve':
#             permission_classes = [IsAuthenticated,IsRelatedUserOrReadOnly|IsSuperUser]
#         elif self.action == 'create':

#             permission_classes = [IsAuthenticated]
#         elif self.action == 'list':
#             permission_classes = [IsAuthenticated]

#         return [permission() for permission in permission_classes]

#     def perform_create(self, serializer):
#         user = self.request.user
#         print(user)
#         try:
#             print("hi")
#             student = Student.objects.get(user=user)
#             serializer.save(student=student)
#         except Student.DoesNotExist:
#             print('hi')
#             raise Exception("Student does not exist for this user.")

#     @action(detail=False, methods=['get'])
#     def user_enrollments(self, request):
#         user = request.user
#         enrollments = Enrollments.objects.filter(student__user=user)
#         serializer = self.get_serializer(enrollments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)    
 


# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Enrollments
# from .serializer import EnrollmentsSerializer
# from Student.models import Student

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.decorators import action
# from django.shortcuts import get_object_or_404
# from Student.models import Student
# from Course.models import Course
# from .models import Enrollments
# from .serializer import EnrollmentsSerializer
# from Permissions.permission import IsStudent, IsRelatedUserOrReadOnly
# from rest_framework.views import APIView

# class EnrollmentsViewset(ModelViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]  # Default permission for all actions
#     queryset = Enrollments.objects.all()
#     serializer_class = EnrollmentsSerializer
#     def get_permissions(self):
#         # Override this method to apply specific permissions based on the action
#         if self.action == 'user_enrollments':
#             permission_classes = [IsAuthenticated, IsStudent]
#         elif self.action in ['retrieve', 'list']:
#             permission_classes = [IsAuthenticated, IsRelatedUserOrReadOnly | IsAdminUser]
#         else:
#             permission_classes = [IsAuthenticated]
#         return [permission() for permission in permission_classes]

#     def list(self, request, *args, **kwargs):
#         # Standard implementation of list action, which might include filtering logic
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get'])
#     def user_enrollments(self, request):
#         # Endpoint to retrieve enrollments for the logged-in student
#         student = get_object_or_404(Student, user=request.user)
#         enrollments = self.queryset.filter(student=student)
#         serializer = self.get_serializer(enrollments, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from Student.models import Student
from Course.models import Course
from .models import Enrollments
from .serializer import EnrollmentsSerializer, EnrollmentsGETSerializer, EnrollmentsPOSTSerializer
from Permissions.permission import IsStudent, IsRelatedUserOrReadOnly
from rest_framework.views import APIView


class EnrollmentsViewset(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Default permission for all actions
    queryset = Enrollments.objects.all()
    serializer_class = EnrollmentsSerializer

    def get_permissions(self):
        # Override this method to apply specific permissions based on the action
        if self.action == 'user_enrollments':
            permission_classes = [IsAuthenticated, IsStudent]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsRelatedUserOrReadOnly | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        # Standard implementation of list action, which might include filtering logic
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    def create(self, request):
        print("hii")

        serialized_data = request.data  # Get validated data from serializer
        print(serialized_data)
        new_serializer = EnrollmentsPOSTSerializer(data=serialized_data)  # Create a new instance of EnrollmentsPOSTSerializer
        if new_serializer.is_valid():
            print(new_serializer.validated_data)
            new_instance = new_serializer.save()  # Save the new instance
            # Perform any additional actions after creating the object
        else:
            # Handle the case where the data is not valid
            pass


    @action(detail=False, methods=['get'])
    def user_enrollments(self, request):
        # Endpoint to retrieve enrollments for the logged-in student
        student = get_object_or_404(Student, user=request.user)
        enrollments = self.queryset.filter(student=student)
        
        if request.method == 'GET':
            serializer = EnrollmentsGETSerializer(enrollments, many=True, context={'request': request})
        else:
            serializer = EnrollmentsPOSTSerializer(enrollments, many=True, context={'request': request})
            self.perform_create(serializer)  # Perform additional actions after creating the object

        return Response(serializer.data, status=status.HTTP_200_OK)

    





from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Enrollments
from Student.models import Student
from Course.models import Course

class EnrollmentsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        student = get_object_or_404(Student, user=user)
        course_id = request.data.get('course')

        # Check if the enrollment already exists for the student and course
        existing_enrollment = Enrollments.objects.filter(student=student, course_id=course_id).exists()
        if existing_enrollment:
            return Response({"error": "This enrollment already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            enrollment = Enrollments.objects.create(student=student, course_id=course_id)
            return Response({"message": "Enrollment created successfully."}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Failed to create enrollment due to integrity constraint violation."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
