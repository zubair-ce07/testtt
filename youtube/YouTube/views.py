from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from YouTube.permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from YouTube.models import Video
from YouTube.serializers import UserSerializer, VideoSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'videos': reverse('video-list', request=request, format=format)
    })


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VideoList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'YouTube/video_list.html'

    def get(self, request, format=None):
        queryset = Video.objects.all()
        return Response({'videos': queryset})

    def post(self, request, format=None):
        Video.objects.create(name=request.POST.get('name'),
                             owner=self.request.user)
        return redirect('video-list')


class VideoDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'YouTube/video_detail.html'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get(self, request, pk, format=None):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoSerializer(video)
        return Response({'serializer': serializer, 'video': video})

    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoSerializer(video, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'video': video})
        serializer.save()
        return redirect('video-list')
