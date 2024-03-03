from django.db import models
from ProgramingLanguage.models import ProgrammingLanguage
from Employee.models import Employee
from django.core.validators import MinValueValidator
from decimal import Decimal

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    programming_language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='courses')
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='created_courses',editable=False)
    price = models.DecimalField(max_digits=6, decimal_places=2,default=50.00, validators=[MinValueValidator(Decimal('0.00'))],
)
    imageURL=models.ImageField(upload_to='Course/coures-images',null=True,blank=True)

    def  __str__(self):
        return self.title
