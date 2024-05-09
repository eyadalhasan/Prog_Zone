from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import Course, Quiz, Question, Choice
from .serializer import QuizSerializer, QuestionSerializer, ChoiceSerializer
from rest_framework.response import Response

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer

    def get_queryset(self):
        """
        This view should return a list of all quizzes for
        the course as determined by the course_id portion of the URL.
        """
        course_id = self.kwargs['course_id']  # Get course_id from URL parameters
        return Quiz.objects.filter(course__id=course_id)
    def list(self, request, *args, **kwargs):
        # Standard implementation of list action, which might include filtering logic
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    def get_queryset(self):
        """
        This view returns a list of all questions for a quiz as determined by the quiz_id part of the URL.
        """
        quiz_id = self.kwargs['quiz_id']
        return Question.objects.filter(quiz__id=quiz_id)

    def perform_create(self, serializer):
        """
        This method is called when a new question is created and ensures it is associated with the correct quiz.
        """
        quiz_id = self.kwargs['quiz_id']
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        serializer.save(quiz=quiz)
    def list(self, request, *args, **kwargs):
        # Standard implementation of list action, which might include filtering logic
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
class ChoiceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing choice instances.
    """
    serializer_class = ChoiceSerializer

    def get_queryset(self):

        queryset = Choice.objects.all()
        question_id = self.request.query_params.get('question_id')
        print(question_id)
        if question_id is not None:
            queryset = queryset.filter(question__id=question_id)
        return queryset
    
    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)