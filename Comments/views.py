# from rest_framework import viewsets
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from .models import Comment
# from .serializer import CommentSerializer

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     def perform_create(self, serializer):
#         # Set the user of the comment to the authenticated user
#         serializer.save(user=self.request.user)

#     @action(detail=True, methods=['get'])
#     def comments_by_course(self, request, pk=None):
#         comments = Comment.objects.filter(course__id=pk) 
#         serializer = self.get_serializer(comments, many=True)
        
        
#         return Response(serializer.data)


from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Comment
from .serializer import CommentGetSerializer, CommentPostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def get_serializer_class(self):
        # Use CommentGetSerializer for GET requests
        if self.request.method == 'GET':
            return CommentGetSerializer
        # Use CommentPostSerializer for POST requests
        return CommentPostSerializer

    @action(detail=True, methods=['get'])
    def comments_by_course(self, request, pk=None):
        comments = Comment.objects.filter(course__id=pk) 
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Set the user of the comment to the authenticated user
        serializer.save(user=self.request.user)
