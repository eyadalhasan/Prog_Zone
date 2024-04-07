from django.db import models
from User.models import CustomUser
from ProgramingLanguage.models import ProgrammingLanguage
from Category.models import Category
class Employee(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    programming_languages = models.ManyToManyField(ProgrammingLanguage, related_name='employees',blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=None,null=True,blank=True)
    bio = models.TextField(blank=True, null=True)
    def  __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural="Employees"
    