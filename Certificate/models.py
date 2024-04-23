from django.db import models
from User.models import CustomUser
class Certificate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="User",)
    username = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    date_of_issue = models.DateField(auto_now_add=True)
    certificate_image = models.ImageField(upload_to='certificates/', blank=True, null=True)  # Add this line


    def __str__(self):
        return f"{self.course_name} - {self.username}"
