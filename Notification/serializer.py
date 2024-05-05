from rest_framework.serializers import Serializer

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'user', 'created_at']  # These fields should not be modified directly by the API

    def create(self, validated_data):
        # Assuming the user is set based on the request and not through the API directly
        user = self.context['request'].user
        notification = Notification.objects.create(user=user, **validated_data)
        return notification
