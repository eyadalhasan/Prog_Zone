from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import Course, Quiz, Question, Choice
from .serializer import QuizSerializer, QuestionSerializer, ChoiceSerializer
from rest_framework.response import Response


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned quizzes to those associated with a specific course,
        by filtering against a 'course_id' query parameter in the URL.
        """
        course_id = self.kwargs.get('course_id')
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


# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

#     def get_queryset(self):
#         """
#         Optionally restricts the returned questions to those associated with a specific quiz,
#         by filtering against a 'quiz_id' query parameter in the URL.
#         """
        
#         quiz_id = self.kwargs.get('quiz_id')
#         print("Quiz_id",quiz_id)
#         if quiz_id is not None:
#             return self.queryset.filter(quiz_id=quiz_id)
#         return self.queryset
#     def list(self, request, *args, **kwargs):

#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing choice instances.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    lookup_field = 'pk'  # Ensure this matches your URL conf if using a different field

    def get_queryset(self):
        """
        Optionally restricts the returned choices to a given question,
        by filtering against a `question_id` query parameter in the URL.
        """

        queryset = super().get_queryset()
        question_id = self.request.query_params.get('question_id')
        print("Question iddd",question_id)
        if question_id:
            queryset = queryset.filter(question__id=question_id)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific choice. Override if necessary to add extra context or functionality.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a choice. Can handle PATCH requests.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        Perform the update on the serializer.
        """
        
        serializer.save()

    def list(self, request, *args, **kwargs):
        """
        List all choices, or those related to a specific question.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

# class ChoiceViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing choice instances.
#     """
#     serializer_class = ChoiceSerializer

#     def get_queryset(self):

#         queryset = Choice.objects.all()
#         question_id = self.request.query_params.get('question_id')
#         print(question_id)
#         if question_id is not None:
#             queryset = queryset.filter(question__id=question_id)
#         return queryset
    
#     def list(self, request, *args, **kwargs):

#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)