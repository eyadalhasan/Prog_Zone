from rest_framework import serializers
from .models import Enrollments

class EnrollmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollments
        fields ="__all__"
        depth=1

class EnrollmentsPOSTSerializer(EnrollmentsSerializer):
    class Meta(EnrollmentsSerializer.Meta):
        pass

class EnrollmentsGETSerializer(EnrollmentsSerializer):
    class Meta(EnrollmentsSerializer.Meta):
        depth = 4