from django.db import models
from User.models import CustomUser
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='videos/', null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    viewers = models.ManyToManyField(CustomUser, through='VideoView', related_name='viewed_videos')

    def __str__(self):
        return self.title

class VideoView(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    viewed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} viewed {self.video.title}'
