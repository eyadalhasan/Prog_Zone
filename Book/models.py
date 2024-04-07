from django.db import models
from Course.models import Course
from BindingBook.models import BindingBook
class Book(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='bookscourse',default=None,blank=True,null=True)
    title = models.CharField(max_length=200,blank=True,null=True)
    author = models.CharField(max_length=100,blank=True,null=True)
    link = models.URLField(blank=True,null=True)
    binding_book = models.OneToOneField(BindingBook, on_delete=models.CASCADE, related_name='book')

    

    def __str__(self):
        return   self.title
    
    