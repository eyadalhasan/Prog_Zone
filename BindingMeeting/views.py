from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from .models import BindingMeeting
from .serializer import MeetingSerializer
from Student.models import Student
from django.http import QueryDict
from rest_framework.decorators import action
from Employee.models import Employee
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .serializer import MeetingEmployeeSerializer
# class BindingMeetingViewSet(viewsets.ModelViewSet):
#     permission_classes = []  # Ensure you configure permissions properly
#     authentication_classes = [TokenAuthentication]
#     queryset = BindingMeeting.objects.all()
#     serializer_class = MeetingSerializer

#     def create(self, request, *args, **kwargs):
#         student = Student.objects.get(user=request.user)  # Get the student object

#         # Create a mutable copy of request.data
#         data = request.data.copy()
#         data['student'] = student.id  # Assuming the serializer expects a student ID

#         serializer = self.get_serializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
    
#     @action(detail=False, methods=['get'])
#     def my_meetings(self, request):
#         """
#         Retrieve all meetings for the currently authenticated user assumed to be an employee.
#         """

#         employee =Employee.objects.get(user=request.user)
#         meetings = self.queryset.filter(employee=employee)
#         serializer = self.get_serializer(meetings, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)




class BindingMeetingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access methods
    authentication_classes = [TokenAuthentication]
    queryset = BindingMeeting.objects.all()
    serializer_class = MeetingSerializer
    # http_method_names=[
    #     'get',
    #     'post',
    #     'patch',
    #     'delete'
    
    # ]

    def create(self, request, *args, **kwargs):
        # Since you require authentication, it's assumed 'request.user' is not Anonymous
        student = Student.objects.get(user=request.user)  # May raise DoesNotExist if no student matches

        data = request.data.copy()
        data['student'] = student.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_meetings(self, request):
        """
        Retrieve all meetings for the currently authenticated user assumed to be an employee.
        """
        try:
            employee = Employee.objects.get(user=request.user)
            meetings = self.queryset.filter(employee=employee)
            serializer = self.get_serializer(meetings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": "Employee not found or not logged in."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get_serializer_class(self):
        print(self.request.method)
        if(self.request.method=='GET'):
            return MeetingEmployeeSerializer
        else:
            return MeetingSerializer



        