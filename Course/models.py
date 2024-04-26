from django.db import models
from ProgramingLanguage.models import ProgrammingLanguage
from Employee.models import Employee
from django.core.validators import MinValueValidator
from decimal import Decimal
from Category.models import Category
from BindingCourse.models import BindingCourse
from Video.models import Video

def video_upload_location(instance, filename):
    return f'Course/course-videos/{instance.title}/{filename}'
class Course(models.Model):
    binding_course = models.OneToOneField(BindingCourse, on_delete=models.CASCADE, related_name='course',null=True,blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='created_courses')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=50.00, validators=[MinValueValidator(Decimal('0.00'))])
    imageURL = models.ImageField(upload_to='Course/course-images', null=True, blank=True)
    videoFile = models.FileField(upload_to=video_upload_location, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    demo= models.FileField(upload_to=video_upload_location, null=True, blank=True)
    videos = models.ManyToManyField(Video, related_name='courses', blank=True)
    
    
    



    def __str__(self):
        return self.title