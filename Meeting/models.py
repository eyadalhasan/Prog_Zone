from django.db import models
from django.conf import settings
from Student.models import Student
from Employee.models import Employee
from BindingMeeting.models import BindingMeeting

class Meeting(models.Model):
    binding_meeting = models.OneToOneField(BindingMeeting, on_delete=models.SET_NULL, related_name='meet',null=True,blank=True)
    date_time = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_meetings')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_meetings')
    message = models.TextField()
    accepted=models.BooleanField(default=False)
    is_readed=models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    class Meta:
        ordering = ['-created_on'] 

    def __str__(self):
        return f"Meeting will be on {self.date_time} with {self.student} and {self.employee}"

