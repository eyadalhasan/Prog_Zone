from django.contrib import admin
from .models import Course
from .models import StudentCourseRank
admin.site.register(Course)
admin.site.register(StudentCourseRank)