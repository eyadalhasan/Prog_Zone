from rest_framework import serializers
from .models import  Quiz, Question, Choice
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'course']
class QuizGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'course']
        depth=4



class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'quiz', 'choices']
        read_only_fields = ['quiz']  # Make quiz a read-only field
        

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct', 'question']

        