from rest_framework import serializers
from .models import Course
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields="__all__"
        depth=2

    

from .models import StudentCourseRank

from rest_framework import serializers
from .models import StudentCourseRank

class StudentCourseRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseRank
        fields = ['id', 'course', 'rank', 'student']
        extra_kwargs = {
            'student': {'read_only': True}  # Make student read-only
        }

    def create(self, validated_data):
        # 'student' will be added in the viewset before calling save
        return StudentCourseRank.objects.create(**validated_data)
