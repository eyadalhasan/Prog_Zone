from rest_framework import serializers
from .models import BindingMeeting

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BindingMeeting
        fields="__all__"
        

class MeetingEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BindingMeeting
        fields="__all__"
        depth=2
        

