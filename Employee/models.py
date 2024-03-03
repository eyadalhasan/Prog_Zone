from django.db import models
from User.models import CustomUser
from ProgramingLanguage.models import ProgrammingLanguage
class Employee(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    programming_languages = models.ManyToManyField(ProgrammingLanguage, related_name='employees')
    # Employee-specific fields
    bio = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, default='Instructor')
    def  __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural="Employees"
