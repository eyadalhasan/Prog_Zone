from django.db import models

class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    lang_id=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.name
    
