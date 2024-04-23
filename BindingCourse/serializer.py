# Signals/serializers.py
from rest_framework import serializers
from .models import BindingCourse

class BindingCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BindingCourse
        fields = '__all__'
        depth=1
