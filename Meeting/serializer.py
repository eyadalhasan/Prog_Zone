from rest_framework import serializers
from .models import Meeting

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'date_time', 'student', 'employee', 'message','accepted','is_readed']
        depth=2
