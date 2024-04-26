from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Video, VideoView

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'file', 'duration']

class VideoViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoView
        fields = ['video', 'user', 'viewed_on']
