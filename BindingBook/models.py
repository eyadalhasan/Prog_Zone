
# Create your models here.
from django.db import models
from Course.models import Course
class BindingBook(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='bindingbooksscourse',default=None,blank=True,null=True)
    title = models.CharField(max_length=200,blank=True,null=True)
    author = models.CharField(max_length=100,blank=True,null=True)
    link = models.URLField(blank=True,null=True)
    approved=models.BooleanField(default=False)

    

    def __str__(self):
        return   self.title
    
    