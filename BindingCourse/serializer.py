# Signals/serializers.py
from rest_framework import serializers
from .models import BindingCourse

from .models import Video




class BindingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BindingCourse
        fields = '__all__'
        depth=1


from rest_framework import serializers
from .models import BindingCourse, Video
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['file']

    def create(self, validated_data):
        return Video.objects.create(**validated_data)
class BindingPostCourseSerializer(serializers.ModelSerializer):
    # videos = VideoSerializer()
    class Meta:
        model = BindingCourse
        fields = ['title', 'description', 'category', 'price', 'imageURL', 'demo', 'videos']
