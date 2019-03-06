from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from django.core import serializers
from rest_framework.views import APIView

from api.tweets.models import Trends, Tweets
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions, status
from api.tweets.serializer import TrendSerializer, TweetSerializer


class TrendList(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        data = [TrendSerializer(trend).data for trend in Trends.objects.all()]
        return Response(data)

    def post(self, request):
        payload = request.data
        chapters = payload.pop('chapters', [])
        book_serializer = TrendSerializer(data=payload)
        return Response(book_serializer.data, status=status.HTTP_201_CREATED)


def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        uploaded_file_url = fs.url(filename)
        json_data = open('C:\\Users\\SHAHRUKH\\PycharmProjects\\awp_project\\' + filename)
        json_data = json_data.read()
        json_file = json.loads(json_data)
        file = json_file
        i = 0
        for data in file:
            data_id = data['id']
            title = data['title'].encode('utf-8', 'replace')
            trend_link = data['link'].encode('utf-8', 'replace')
            title_img = data['title_img'].encode('utf-8', 'replace')

            trend = Trends(trend_link=trend_link, id=data_id, title=title, image_link=title_img)
            trend.save()

            if data['tweets']:
                for tweet in data['tweets']:
                    i = i+1
                    profile_image = tweet['profile_img'].encode('utf-8', 'replace')
                    username = tweet['username'].encode('utf-8', 'replace')
                    tweet_data = tweet['tweet_data'].encode('utf-8', 'replace')
                    trend_id = int(tweet['trend_id'])

                    tweet = Tweets(profile_image=profile_image, id=i, username=username, tweet_data=tweet_data,
                                   trend_id=trend_id)
                    tweet.save()

        return render(request, 'tweets/upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'json_file': json_file
        })
    return render(request, 'tweets/upload.html')


def api_trends(request):
    data = Trends.objects.all().values('id', 'title')
    data = list(data)
    return JsonResponse({'trends': data})


def api_tweets(request):
    data = Tweets.objects.all().values('username', 'tweet_data')
    data = list(data)
    return JsonResponse({'tweets': data})
