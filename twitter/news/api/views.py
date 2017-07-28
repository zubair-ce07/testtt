from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import News
from news.api.serializers import NewsSerializer
from rest_framework import generics, status


class NewsList(APIView):
    def get(self, request, format=None):
        news =  News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serialzer = NewsSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status=status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
# class NewsList(generics.ListCreateAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#
#
# class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer