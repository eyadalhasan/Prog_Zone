from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Enrollments
from .serializer import EnrollmentsSerializer
from Permissions.permission import IsEmployee,IsSuperUser,IsRelatedEmployeeOrReadOnly,IsStudentOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from Permissions.permission import IsRelatedUserOrReadOnly
class EnrollmentsViewset(ModelViewSet):
    permission_classes=[]
    authentication_classes=[TokenAuthentication]
    queryset = Enrollments.objects.all()
    serializer_class = EnrollmentsSerializer
    http_method_names=['post','get']
    def get_permissions(self):
        if(self.action=='get'):
            permission_classes = [IsAuthenticated,IsRelatedUserOrReadOnly|IsSuperUser]
        elif(self.action in ['create']):
            permission_classes=[IsAuthenticated,IsRelatedUserOrReadOnly]
            

        
            
             
                 


        

    
 


