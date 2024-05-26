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
from Video.views import LogVideoView
router = DefaultRouter()
# Registering viewsets with router
from ProgramingLanguage.views import ProgramingLanguageViewSet
from Employee.views import EmployeeRegestrationView
from Enrollments.views import EnrollmentsViewset
from Category.views import CategoryViewSet
from BindingCourse.views import BindingCourseViewSet
from Employee.views import EmployeeDataView
from Enrollments.views import EnrollmentsView
from Course.views import StudentCourseRankViewSet
from BindingMeeting.views import BindingMeetingViewSet
from Notification.views import NotificationViewSet
from Meeting.views import MeetingViewSet
from Course.views import CourseViewSet
from Video.views import check_all_videos_watched

router.register(
    r"programing-language", ProgramingLanguageViewSet, basename="ProgramingLanguage"
)

from Student.views import StudentRegisteration
from Book.views import BookViewSet
from Course.views import CourseViewSet
from Comments.views import CommentViewSet
from Certificate.views import CertificateAPI
from Quiz.views import ChoiceViewSet,QuestionViewSet,QuizViewSet
from Employee.views import delete_user
from Employee.views import delete_student
router.register(r'book',BookViewSet,basename='book')
router.register(r'course',CourseViewSet,basename='course')
router.register(r'summary',SummaryViewSet,basename='summary')
router.register(r'enrollment',EnrollmentsViewset,basename='enrollment')
# router.register(r'meeting',EnrollmentsViewset,basename='enrollment')

router.register(r'category',CategoryViewSet,basename='Category')
router.register(r'comment',CommentViewSet,basename='Comment')

# router.register(r'courses', CourseViewSet,basename='courses')

router.register(r'bindingcourses', BindingCourseViewSet,basename='BindingCourse')
router.register(r'studentcourseranks', StudentCourseRankViewSet,basename="studentcourseranks")
router.register(r'binding-meeting',BindingMeetingViewSet,basename='bindinmeeting')
router.register(r'notification',NotificationViewSet,basename='notification')
router.register(r'meeting',MeetingViewSet,basename='meeting')
# router.register(r'quizzes', QuizViewSet,basename="quizzes")
router.register(r'questions', QuestionViewSet,basename="questions")
router.register(r'choices', ChoiceViewSet,basename="choices")
router.register(r'course/(?P<course_id>\d+)/quizzes', QuizViewSet, basename='quizzes-course')

# router.register(r'quizzes/(?P<quiz_id>\d+)/questions', QuestionViewSet, basename='questions-quizees')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("User.urls")),
    path('employee-register/',EmployeeRegestrationView.as_view(),name= 'employee-register'),
    path('employee/<int:id>',EmployeeDataView.as_view(),name= 'employee-data'),
    path('add-enrollment/',EnrollmentsView.as_view(),name= 'enrollment-data'),
    path('log_video_view/<int:video_id>/', LogVideoView.as_view(), name='log_video_view'),
    path('check_all_videos_watched/<int:course_id>/', check_all_videos_watched, name='check_all_videos_watched'),
    path('delete_user/<int:instructor_id>/', delete_user, name='delete_user'),
    path('delete_student/<int:student_id>/', delete_student, name='delete_student'),

#     path('course/<int:course_id>/quizzes/', QuizViewSet.as_view({
#         'get': 'list',
#         'post': 'create'
#     }), name='course-quizzes')
# ,
#     path('quizzes/<int:quiz_id>/questions/', QuestionViewSet.as_view({
#         'get': 'list',  # To retrieve all questions for a quiz
#         'post': 'create'  # To create a new question for a quiz
#     }), name='quiz-questions'),
#     path('quizzes/<int:quiz_id>/questions/<int:pk>/', QuestionViewSet.as_view({
#         'get': 'retrieve',  # To retrieve a specific question
#         'put': 'update',    # To update a specific question
#         'delete': 'destroy' # To delete a specific question
#     }), name='quiz-question-detail'),


#     path('questions/<int:question_id>/choices/', ChoiceViewSet.as_view({
#         'get': 'list',  # To retrieve all questions for a quiz
#         'post': 'create'  # To create a new question for a quiz
#     }), name='questions-choices'),
#     path('questions/<int:question_id>/choices/<int:pk>/', ChoiceViewSet.as_view({
#         'get': 'retrieve',  # To retrieve a specific question
#         'put': 'update',    # To update a specific question
#         'delete': 'destroy' # To delete a specific question
#     }), name='questions-choices-detail'),

    # path('course/<int:course_id>/quizzes/', QuizViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create',
    #     'patch': 'partial_update'  # To partially update a specific quiz
    # }), name='course-quizzes'),


    path('quizzes/<int:quiz_id>/questions/', QuestionViewSet.as_view({
        'get': 'list',    # To retrieve all questions for a quiz
        'post': 'create', # To create a new question for a quiz
        'patch': 'partial_update'  # To partially update a specific question
    }), name='quiz-questions')
    ,

    # Specific quiz question detail
    path('quizzes/<int:quiz_id>/questions/<int:pk>/', QuestionViewSet.as_view({
        'get': 'retrieve',  # To retrieve a specific question
        'put': 'update',     # To update a specific question
        'patch': 'partial_update',  # To partially update a specific question
        'delete': 'destroy'  # To delete a specific question
    }), name='quiz-question-detail'),

 

    # Questions
    path('questions/<int:question_id>/choices/', ChoiceViewSet.as_view({
        'get': 'list',    # To retrieve all choices for a question
        'post': 'create', # To create a new choice for a question
        'patch': 'partial_update'  # To partially update a specific choice
    }), name='questions-choices'),

    path('questions/<int:question_id>/choices/<int:pk>/', ChoiceViewSet.as_view({
        'get': 'retrieve',  # To retrieve a specific choice
        'put': 'update',     # To update a specific choice
        'patch': 'partial_update',  # To partially update a specific choice
        'delete': 'destroy'  # To delete a specific choice
    }), name='questions-choices-detail'), 

    path('student-register/',StudentRegisteration.as_view(),name= 'student-register'),
    path('code_executor/', include('code_executor.urls')),  # Ensure this line is added
    path('certificate/', CertificateAPI.as_view(), name='certificate_api'),
    path('log_view/', LogVideoView.as_view(), name='log_video_view'),
    


    path("", include(router.urls)),

    
]
