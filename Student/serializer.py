from rest_framework import serializers
from .models import Student
from User.serializer import UserSerializer
from .models import Student
class StudentSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Student
        fields="__all__"
    

    def  create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            user.set_password(user_data['password'])
            user.save()
            
        enorlled_courses = validated_data.pop('enrolled_courses', [])
        student = Student.objects.create(user=user, **validated_data)

        if enorlled_courses:
            Student.enrolled_courses.set(enorlled_courses)

        return student
