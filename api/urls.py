"""
URL configuration for progplatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Book.views import BookViewSet
from rest_framework.routers import DefaultRouter
from Summary.views import SummaryViewSet
router = DefaultRouter()
# Registering viewsets with router
from ProgramingLanguage.views import ProgramingLanguageViewSet
from Employee.views import EmployeeRegestrationView
from Enrollments.views import EnrollmentsViewset
router.register(
    r"programing-language", ProgramingLanguageViewSet, basename="ProgramingLanguage"
)
from Student.views import StudentRegisteration
from Book.views import BookViewSet
from Course.views import CourseViewSet
router.register(r'book',BookViewSet,basename='book')
router.register(r'course',CourseViewSet,basename='course')
router.register(r'summary',SummaryViewSet,basename='summary')
router.register(r'enrollment',EnrollmentsViewset,basename='enrollment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("User.urls")),
    path('employee-register/',EmployeeRegestrationView.as_view(),name= 'employee-register'),
    path('student-register/',StudentRegisteration.as_view(),name= 'student-register'),
    path('code_executor/', include('code_executor.urls')),  # Ensure this line is added
    path("", include(router.urls)),

    
]
