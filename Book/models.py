from django.db import models
from ProgramingLanguage.models import ProgrammingLanguage
class Book(models.Model):
    programming_language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='books',default=None,blank=True,null=True)
    title = models.CharField(max_length=200,blank=True,null=True)
    author = models.CharField(max_length=100,blank=True,null=True)
    link = models.URLField(blank=True,null=True)
    def __str__(self):
        return   self.title or self.programming_language.name
    
    