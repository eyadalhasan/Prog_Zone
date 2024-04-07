from rest_framework import serializers
from .models import BindingBook
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BindingBook
        fields="__all__"
    
    