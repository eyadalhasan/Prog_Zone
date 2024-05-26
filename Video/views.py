# from django.shortcuts import render

# # Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.models import User
# from .models import Video, VideoView
# from .serializer import VideoViewSerializer

# class LogVideoView(APIView):
#     def post(self, request, format=None):
#         serializer = VideoViewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Video, VideoView
from .serializer import VideoViewSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
class LogVideoView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get(self, request, video_id, format=None):
        try:
            # Try to find a video view by the current user and specified video
            video_view = VideoView.objects.filter(user=request.user, video_id=video_id)
            if(video_view.exists()):
                last_video_view = video_view.last()
                return Response({'viewed': True, 'video_id': video_id})
        except VideoView.DoesNotExist:
            # If no video view is found, return viewed as False
            return Response({'viewed': False, 'video_id': video_id})
    def post(self, request, video_id, format=None):
        try:
            video_view = VideoView.objects.create(user=request.user, video_id=video_id)
            return Response({"message": "Video view logged successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VideoView
from Course.models import Course
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def check_all_videos_watched(request, course_id):
    try:
        # Get the course object
        course = Course.objects.get(id=course_id)
        
        # Get all videos in the course
        videos_in_course = course.videos.all()
        
        
        # Get video views for the current user and course
        video_views = VideoView.objects.filter(user=request.user, video__in=videos_in_course)
        
        # Check if all videos have been watched
        all_watched = video_views.count() >= len(videos_in_course)
        

        if len(videos_in_course)==0:
            all_watched=False

        
        return Response({'all_watched': all_watched}, status=status.HTTP_200_OK)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
