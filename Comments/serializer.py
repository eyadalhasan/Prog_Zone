from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):


    class Meta:
        model = Comment
        fields = ['id', 'user', 'course', 'text', 'created_at']
        depth=1
        read_only_fields = ['id', 'user', 'created_at']
        
        
