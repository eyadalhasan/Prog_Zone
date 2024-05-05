from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from Student.models import Student
from Employee.models import Employee

class BindingMeeting(models.Model):
    date_time = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='binding_student_meetings')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='binding_employee_meetings')
    message = models.TextField(default="",blank=True,null=True)
    approved = models.BooleanField(default=False)
    is_readed=models.BooleanField(default=False)



    def __str__(self):
        return f"Meeting on {self.date_time} with {self.student} and {self.employee}"
