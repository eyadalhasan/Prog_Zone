from django.db import models
from User.models import CustomUser
class Student(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    level = models.CharField(max_length=50, default='Beginner')  # Example: Beginner, Intermediate, Expert
    
    def  __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural="Students"
