from django.db import models
from  Course.models import Course
from django.db import models
from ProgramingLanguage.models import ProgrammingLanguage

class Summary(models.Model):
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE, related_name='summaries',default=None,blank=True,null=True)
    file = models.FileField(upload_to='Summary/summary_files/',default=None)

    class Meta:
        verbose_name_plural = "Summaries"


    def __str__(self):
        return self.language.name
    
    
    