from django.db import models
from Student.models import Student
from Course.models import Course
class Enrollments(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_students')
    date_enrolled = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural="Enrollments"

    def __str__(self):
        # Assuming Student model has a user field linking to Django's User model
        # and the Course model has a title field.
        return f'{self.student.user.username} enrolled in {self.course.title}'
