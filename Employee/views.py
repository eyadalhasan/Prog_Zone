from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .serializer import EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from Employee.models import Employee
from .serializer import EmployeeSerializerPost
class EmployeeRegestrationView(APIView):
    permission_classes = ()
    authentication_classes = ()
   
    def post(self, request, format=None):
        data=request.data
        print(data)
        serializer=EmployeeSerializerPost(data=data)
        if  serializer.is_valid():
            print(serializer.errors)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        objs=Employee.objects.all()
        serilize=EmployeeSerializer(objs, many=True)
        return Response(serilize.data,status=status.HTTP_200_OK)
    
class EmployeeDataView(APIView):
    permission_classes = ()
    authentication_classes = ()
   
    def post(self, request, format=None):
        data = request.data
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id, format=None):
        # Use 'id' as a positional argument to capture the value passed in the URL
        obj = Employee.objects.get(id=id)
        serialize = EmployeeSerializer(obj)
        return Response(serialize.data, status=status.HTTP_200_OK)




    




from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Employee
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from Student.models import Student
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_user(request, instructor_id):
    try:
        # Get the instructor by ID
        instructor = Employee.objects.get(id=instructor_id)
    
        # Get the user associated with the instructor
        user = instructor.user
        
        # Delete the user
        user.delete()
        
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Employee.DoesNotExist:
        return Response({'error': 'Instructor not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_student(request, student_id):
    try:
        # Get the instructor by ID
        student = Student.objects.get(id=student_id)
    
        # Get the user associated with the instructor
        user = student.user
        
        # Delete the user
        user.delete()
        
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Employee.DoesNotExist:
        return Response({'error': 'student not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)