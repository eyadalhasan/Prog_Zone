from django.db import models
from User.models import CustomUser
from Course.models import Course

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
