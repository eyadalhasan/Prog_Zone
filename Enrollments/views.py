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

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from Student.models import Student
from .models import Enrollments
from .serializer import EnrollmentsSerializer
from Permissions.permission import IsStudent, IsRelatedUserOrReadOnly

class EnrollmentsViewset(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # Default permission for all actions

    queryset = Enrollments.objects.all()
    serializer_class = EnrollmentsSerializer
    http_method_names = ['get', 'post']  # Allow GET and POST requests

    def get_permissions(self):
        if self.action == 'user_enrollments':
            permission_classes = [IsAuthenticated, IsStudent]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, IsRelatedUserOrReadOnly | IsSuperUser]
        else:
            permission_classes = self.permission_classes  # Use default permissions for other actions

        return [permission() for permission in permission_classes]
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)    
 
    @action(detail=False, methods=['get'])
    def user_enrollments(self, request):
        try:
            # Retrieve the authenticated user (current user making the request)
            user = request.user

            # Retrieve the associated Student instance for the user
            student = Student.objects.get(user=user)

            # Query enrollments filtered by the student
            enrollments = Enrollments.objects.filter(student=student)

            # Serialize enrollments data
            serializer = self.get_serializer(enrollments, many=True)

            # Return serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Student.DoesNotExist:
            # Handle case where no Student record is found for the user
            return Response({"error": "No Student record found for this user."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle other unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        # Retrieve the authenticated user (current user making the request)
        user = request.user

        try:
            # Retrieve the Student instance associated with the authenticated user
            student = Student.objects.get(user=user)

        except Student.DoesNotExist:
            # If no Student is associated with this user, return an error response
            return Response({"error": "No Student record found for this user."}, status=status.HTTP_404_NOT_FOUND)

        # Make a mutable copy of the request data
        mutable_data = request.data.copy()

        # Add the student instance to the mutable data before creating the serializer
        mutable_data['student'] = student.id  # Assuming 'student' is the field name in the serializer

        # Create a serializer instance with the updated mutable data
        serializer = self.get_serializer(data=mutable_data)

        if serializer.is_valid():
            # Save the serializer to create the Enrollments instance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
