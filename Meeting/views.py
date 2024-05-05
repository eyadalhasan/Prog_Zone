from rest_framework import viewsets
from .models import Meeting
from .serializer import MeetingSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from Employee.models import Employee

class MeetingViewSet(viewsets.ModelViewSet):
    permission_classes=[]
    authentication_classes=[TokenAuthentication]
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    def create(self, request, *args, **kwargs):
        # Assuming the 'student' field should be set to the current user
        request.data['student'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=False, methods=['get'], url_path='my-meetings')
    def my_meetings(self, request):
        """
        Retrieve all meetings for the currently authenticated user assumed to be an employee.
        """

        employee =Employee.objects.get(user=request.user)
        meetings = self.queryset.filter(employee=employee)
        serializer = self.get_serializer(meetings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @action(detail=True,methods=['get'], url_path='by-employee')
    def by_employee(self,request,pk):
        """
        Retrieve all meetings for the currently authenticated user assumed to be an employee.
        """

        meetings = self.queryset.filter(employee=pk)
        serializer = self.get_serializer(meetings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

