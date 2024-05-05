from django.db import models
from Student.models import Student
from Course.models import Course
from django.db import models

class Enrollments(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enrollments"
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_enrollment')
        ]

    def __str__(self):
        return f'{self.student.user.username} enrolled in {self.course.title}'
