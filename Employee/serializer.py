from rest_framework import serializers
from .models import Employee
from django.contrib.auth import get_user_model
from User.serializer import UserSerializer  # Make sure this import path is correct

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):


    user = UserSerializer()
   

    class Meta:
        model = Employee
        fields = "__all__"  # This now includes the nested user serializer
        depth=1
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)


        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.set_password(user_data['password'])
            user.save()
            
            # Assuming the set_password is handled within the UserSerializer.save method

        programming_languages_data = validated_data.pop('programming_languages', [])
        employee = Employee.objects.create(user=user, **validated_data)

        if programming_languages_data:
            employee.programming_languages.set(programming_languages_data)

        return employee




class EmployeeSerializerPost(serializers.ModelSerializer):


    user = UserSerializer()
   

    class Meta:
        model = Employee
        fields = "__all__"  # This now includes the nested user serializer
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)


        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.set_password(user_data['password'])
            user.save()
            
            # Assuming the set_password is handled within the UserSerializer.save method

        programming_languages_data = validated_data.pop('programming_languages', [])
        employee = Employee.objects.create(user=user, **validated_data)

        if programming_languages_data:
            employee.programming_languages.set(programming_languages_data)

        return employee